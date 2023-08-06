// Copyright 2020 The TensorStore Authors
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#include "tensorstore/internal/http/curl_transport.h"

#ifdef _WIN32

#undef UNICODE
#define WIN32_LEAN_AND_MEAN

#include <windows.h>
#include <winsock2.h>
#include <ws2tcpip.h>

#pragma comment(lib, "ws2_32.lib")

#else  // _WIN32

#include <arpa/inet.h>
#include <fcntl.h>
#include <ifaddrs.h>
#include <netdb.h>
#include <netinet/in.h>
#include <netinet/tcp.h>  // for TCP_NODELAY
#include <sys/select.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <unistd.h>

#endif  // _WIN32

#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>

#include <cstring>
#include <thread>

#include <gmock/gmock.h>
#include <gtest/gtest.h>
#include "absl/base/thread_annotations.h"
#include "absl/container/flat_hash_map.h"
#include "absl/strings/escaping.h"
#include "absl/strings/str_cat.h"
#include "absl/strings/string_view.h"
#include "tensorstore/internal/http/http_request.h"
#include "tensorstore/internal/logging.h"
#include "tensorstore/internal/mutex.h"
#include "tensorstore/util/executor.h"

// Platform specific defines.
#ifdef _WIN32

// nghttp2 may not have ssize_t defined correctly,
using ssize_t = ptrdiff_t;
using socket_t = SOCKET;
int get_socket_errno() { return WSAGetLastError(); }

#else  // _WIN32

using socket_t = int;
constexpr socket_t INVALID_SOCKET = -1;
int closesocket(socket_t fd) { return close(fd); }
int get_socket_errno() { return errno; }

#endif  // _WIN32

#include <nghttp2/nghttp2.h>

using tensorstore::internal_http::HttpRequestBuilder;

namespace {

socket_t CreateBoundSocket() {
  auto try_open_socket = [](struct addrinfo* rp) -> socket_t {
    // Create a socket
    //
    // NOTE: On WIN32 we could use WSASocket to prevent the socket from being
    // inherited and to enable overlapped io, but for now we skip that and stick
    // with the standard C interface.
    socket_t sock = socket(rp->ai_family, rp->ai_socktype, rp->ai_protocol);
    if (sock < 0) return INVALID_SOCKET;

    // Make 'reuse address' option available
    int yes = 1;
    setsockopt(sock, SOL_SOCKET, SO_REUSEADDR, reinterpret_cast<char*>(&yes),
               sizeof(yes));
#ifdef SO_REUSEPORT
    setsockopt(sock, SOL_SOCKET, SO_REUSEPORT, reinterpret_cast<char*>(&yes),
               sizeof(yes));
#endif

    // Ensure port is set to 0.
    if (rp->ai_family == AF_INET) {
      ((struct sockaddr_in*)rp->ai_addr)->sin_port = 0;
    } else if (rp->ai_family == AF_INET6) {
      ((struct sockaddr_in6*)rp->ai_addr)->sin6_port = 0;
    }

    // bind and listen
    if (::bind(sock, rp->ai_addr, static_cast<socklen_t>(rp->ai_addrlen))) {
      closesocket(sock);
      return INVALID_SOCKET;
    }
    if (::listen(sock, 5)) {  // Listen through 5 channels
      closesocket(sock);
      return INVALID_SOCKET;
    }
    return sock;
  };

  // Get address info
  struct addrinfo hints;

  memset(&hints, 0, sizeof(struct addrinfo));
  hints.ai_family = AF_UNSPEC;
  hints.ai_socktype = SOCK_STREAM;
  hints.ai_flags = AI_PASSIVE;
  hints.ai_protocol = 0;

  struct addrinfo* result;
  if (getaddrinfo("localhost", nullptr, &hints, &result)) {
    return INVALID_SOCKET;
  }

  // Loop over the address families twice. On the first pass try and open
  // ipv4 sockets, and on the second pass try and open ipv6 sockets.
  for (auto* rp = result; rp; rp = rp->ai_next) {
    if (rp->ai_family == AF_INET) {
      auto sock = try_open_socket(rp);
      if (sock != INVALID_SOCKET) {
        freeaddrinfo(result);
        return sock;
      }
    }
  }
  for (auto* rp = result; rp; rp = rp->ai_next) {
    if (rp->ai_family == AF_INET6) {
      auto sock = try_open_socket(rp);
      if (sock != INVALID_SOCKET) {
        freeaddrinfo(result);
        return sock;
      }
    }
  }

  freeaddrinfo(result);
  return INVALID_SOCKET;
}

std::string FormatSocketAddress(socket_t sock) {
  struct sockaddr_storage peer_addr;
  socklen_t peer_len = sizeof(peer_addr);

  // Get the bound address.
  if (getsockname(sock, (struct sockaddr*)&peer_addr, &peer_len)) {
    return {};
  }

  const bool is_ipv6 = ((struct sockaddr*)&peer_addr)->sa_family == AF_INET6;
  char hbuf[1025], sbuf[32];
  if (0 == getnameinfo((struct sockaddr*)&peer_addr, peer_len, hbuf,
                       sizeof(hbuf), sbuf, sizeof(sbuf),
                       NI_NUMERICHOST | NI_NUMERICSERV)) {
    return absl::StrCat(is_ipv6 ? "[" : "", hbuf, is_ipv6 ? "]:" : ":", sbuf);
  }
  return {};
}

bool SetSocketNonBlocking(socket_t sock) {
  // Disable NAGLE by using TCP_NODELAY.
  int yes = 1;
  setsockopt(sock, IPPROTO_TCP, TCP_NODELAY, reinterpret_cast<char*>(&yes),
             sizeof(yes));

  // Also set the fd/ioctl as non-blocking.
#ifdef _WIN32
  unsigned long mode = 1;
  return (ioctlsocket(sock, FIONBIO, &mode) == 0) ? true : false;
#else
  int flags = fcntl(sock, F_GETFL, 0);
  if (flags == -1) return false;
  return (fcntl(sock, F_SETFL, flags | O_NONBLOCK) == 0) ? true : false;
#endif
}

// Waits up to 200ms for a read.
bool WaitForRead(socket_t sock) {
  fd_set read;
  struct timeval tv;
  tv.tv_sec = 0;
  tv.tv_usec = 200000;

  for (;;) {
    FD_ZERO(&read);
    FD_SET(sock, &read);

    int sel = select(sock + 1, &read, nullptr, nullptr, &tv);
    if (sel < 0) continue;
    if (FD_ISSET(sock, &read)) return true;
    return false;
  }
}

socket_t AcceptNonBlocking(socket_t server_fd) {
  struct sockaddr_storage peer_addr;
  socklen_t peer_len = sizeof(peer_addr);

  socket_t client_fd =
      accept(server_fd, (struct sockaddr*)&peer_addr, &peer_len);
  assert(client_fd >= 0);

  SetSocketNonBlocking(client_fd);
  return client_fd;
}

std::string ReceiveAvailable(socket_t client_fd) {
  constexpr size_t kBufferSize = 4096;
  char buf[kBufferSize];
  std::string data;

  // Read as long as there is data available.
  for (; WaitForRead(client_fd);) {
    int r = recv(client_fd, buf, kBufferSize, 0);
    if (r < 0) {
      // WaitForRead calls select() on the socket, so we
      // should not see EAGAIN nor EWOULDBLOCK.
      TENSORSTORE_LOG("recv error: ", get_socket_errno());
      break;
    }
    // No data here would be unexpected since WaitForRead calls select().
    TENSORSTORE_CHECK(r > 0);
    data.append(buf, r);
  }
  TENSORSTORE_LOG("recv ", data.size(), ": ", data);
  return data;
}

int AssertSend(socket_t client_fd, absl::string_view data) {
  TENSORSTORE_LOG("send ", data.size(), ":", data);
  int err = send(client_fd, data.data(), data.size(), 0);
  if (err < 0) {
    TENSORSTORE_LOG("send error:", get_socket_errno());
  }
  assert(err == data.size());
  return err;
}

class CurlTransportTest : public ::testing::Test {
 public:
  static void SetUpTestCase() {
#ifdef _WIN32
    WSADATA wsaData;
    TENSORSTORE_CHECK(WSAStartup(MAKEWORD(2, 2), &wsaData) == 0);
#endif
  }
  static void TearDownTestCase() {
#ifdef _WIN32
    WSACleanup();
#endif
  }
};

TEST_F(CurlTransportTest, Http1) {
  auto transport = ::tensorstore::internal_http::GetDefaultHttpTransport();

  // This test sets up a simple single-request tcp/ip service which allows
  // us to mock a simple http server.
  // NOTE: It would be nice to expand this to provide, e.g. HTTP2 functionality.

  socket_t socket = CreateBoundSocket();
  TENSORSTORE_CHECK(socket != INVALID_SOCKET);

  auto hostport = FormatSocketAddress(socket);
  TENSORSTORE_CHECK(!hostport.empty());

  static constexpr char kResponse[] =  //
      "HTTP/1.1 200 OK\r\n"
      "Content-Type: text/html\r\n"
      "\r\n"
      "<html>\n<body>\n<h1>Hello, World!</h1>\n</body>\n</html>\n";

  // Start a thread to handle a single request.
  std::string initial_request;
  std::thread serve_thread = std::thread([&] {
    auto client_fd = AcceptNonBlocking(socket);
    initial_request = ReceiveAvailable(client_fd);
    AssertSend(client_fd, kResponse);
    closesocket(client_fd);
  });

  // Issue a request.
  auto response = transport->IssueRequest(
      HttpRequestBuilder(absl::StrCat("http://", hostport, "/"))
          .AddUserAgentPrefix("test")
          .AddHeader("X-foo: bar")
          .AddQueryParameter("name", "dragon")
          .AddQueryParameter("age", "1234")
          .EnableAcceptEncoding()
          .BuildRequest(),
      absl::Cord("Hello"));

  serve_thread.join();
  std::cout << GetStatus(response);

  using ::testing::HasSubstr;
  EXPECT_THAT(initial_request, HasSubstr("/?name=dragon&age=1234"));
  EXPECT_THAT(initial_request,
              HasSubstr(absl::StrCat("Host: ", hostport, "\r\n")));

  // User-Agent versions change based on zlib, nghttp2, and curl versions.
  EXPECT_THAT(initial_request, HasSubstr("User-Agent: testtensorstore/0.1 "));

  EXPECT_THAT(initial_request, HasSubstr("Accept: */*\r\n"));
  EXPECT_THAT(initial_request, HasSubstr("Accept-Encoding: deflate, gzip\r\n"));
  EXPECT_THAT(initial_request, HasSubstr("X-foo: bar\r\n"));
  EXPECT_THAT(initial_request, HasSubstr("Content-Length: 5"));
  EXPECT_THAT(initial_request,
              HasSubstr("Content-Type: application/x-www-form-urlencoded\r\n"));
  EXPECT_THAT(initial_request, HasSubstr("Hello"));

  EXPECT_EQ(200, response.value().status_code);
  EXPECT_EQ("<html>\n<body>\n<h1>Hello, World!</h1>\n</body>\n</html>\n",
            response.value().payload);
}

// Tests that resending (using CURL_SEEKFUNCTION) works correctly.
TEST_F(CurlTransportTest, Http1Resend) {
  auto transport = ::tensorstore::internal_http::GetDefaultHttpTransport();

  socket_t socket = CreateBoundSocket();
  TENSORSTORE_CHECK(socket != INVALID_SOCKET);

  auto hostport = FormatSocketAddress(socket);
  TENSORSTORE_CHECK(!hostport.empty());

  // Include content-length to allow connection reuse.
  static constexpr char kResponse[] =  //
      "HTTP/1.1 200 OK\r\n"
      "Content-Type: text/html\r\n"
      "Connection: Keep-Alive\r\n"
      "Content-Length: 53\r\n"
      "\r\n"
      "<html>\n<body>\n<h1>Hello, World!</h1>\n</body>\n</html>\n";

  // The client sends 2 requests; the server sees 3 requests because
  // it closes the connection after the second request before sending
  // the response.

  std::string seen_requests[3];
  std::thread serve_thread = std::thread([&] {
    socket_t client_fd = -1;

    for (int i = 0; i < 3; i++) {
      if (client_fd == -1) {
        std::cout << "Waiting on listen" << std::endl;
        client_fd = AcceptNonBlocking(socket);
      }

      while (seen_requests[i].empty()) {
        seen_requests[i] = ReceiveAvailable(client_fd);
      }
      std::cout << "server: request " << i
                << " size=" << seen_requests[i].size() << std::endl;

      if (i == 1) {
        // Terminate the connection after receiving the second request
        // (simulates the race condition under which the server closes the
        // connection due to a timeout just the client is reusing the connection
        // to send another request).
        closesocket(client_fd);
        client_fd = -1;
        continue;
      }

      AssertSend(client_fd, kResponse);
    }

    // cleanup.
    closesocket(client_fd);
    closesocket(socket);
  });

  // Issue 2 requests.
  for (int i = 0; i < 2; ++i) {
    auto response = transport->IssueRequest(
        HttpRequestBuilder(absl::StrCat("http://", hostport, "/"))
            .AddUserAgentPrefix("test")
            .AddHeader("X-foo: bar")
            .AddQueryParameter("name", "dragon")
            .AddQueryParameter("age", "1234")
            .EnableAcceptEncoding()
            .BuildRequest(),
        absl::Cord("Hello"));

    std::cout << GetStatus(response) << std::endl;

    EXPECT_EQ(200, response.value().status_code);
    EXPECT_EQ("<html>\n<body>\n<h1>Hello, World!</h1>\n</body>\n</html>\n",
              response.value().payload);
  }
  serve_thread.join();

  for (auto& request : seen_requests) {
    using ::testing::HasSubstr;
    EXPECT_THAT(request, HasSubstr("/?name=dragon&age=1234"));
    EXPECT_THAT(request, HasSubstr(absl::StrCat("Host: ", hostport, "\r\n")));

    // User-Agent versions change based on zlib, nghttp2, and curl versions.
    EXPECT_THAT(request, HasSubstr("User-Agent: testtensorstore/0.1 "));

    EXPECT_THAT(request, HasSubstr("Accept: */*\r\n"));
    EXPECT_THAT(request, HasSubstr("Accept-Encoding: deflate, gzip\r\n"));
    EXPECT_THAT(request, HasSubstr("X-foo: bar\r\n"));
    EXPECT_THAT(request, HasSubstr("Content-Length: 5"));
    EXPECT_THAT(
        request,
        HasSubstr("Content-Type: application/x-www-form-urlencoded\r\n"));
    EXPECT_THAT(request, HasSubstr("Hello"));
  }
}

// See nghttp2_frame_type
static constexpr const char* kFrameName[] = {
    "NGHTTP2_DATA",           // 0
    "NGHTTP2_HEADERS",        // 0x01,
    "NGHTTP2_PRIORITY",       // 0x02,
    "NGHTTP2_RST_STREAM",     // 0x03,
    "NGHTTP2_SETTINGS",       // 0x04,
    "NGHTTP2_PUSH_PROMISE",   // 0x05,
    "NGHTTP2_PING",           // 0x06,
    "NGHTTP2_GOAWAY",         // 0x07,
    "NGHTTP2_WINDOW_UPDATE",  // 0x08,
    "NGHTTP2_CONTINUATION",   // 0x09,
    "NGHTTP2_ALTSVC",         // 0x0a,
    "",                       // 0x0b
    "NGHTTP2_ORIGIN",         // 0x0c
};

class Http2Session {
  socket_t client_fd_;
  nghttp2_session* session_;
  int32_t last_stream_id_;

 public:
  struct Stream {
    std::vector<std::pair<std::string, std::string>> headers;
    std::string data;
  };

  absl::flat_hash_map<int32_t, Stream> streams;
  absl::flat_hash_map<int32_t, Stream> completed;

  void OnStreamHeader(int32_t stream_id, std::string key, std::string value) {
    TENSORSTORE_LOG("http2 header <", stream_id, ">: ", key, " ", value);
    streams[stream_id].headers.emplace_back(std::move(key), std::move(value));
  }

  void OnStreamData(int32_t stream_id, const char* data, size_t len) {
    streams[stream_id].data.append(data, len);
  }

  void OnStreamDone(int32_t stream_id) {
    if (streams.count(stream_id) != 0) {
      last_stream_id_ = stream_id;
      completed[stream_id] = std::move(streams[stream_id]);
      streams.erase(stream_id);
    }
  }

  size_t Send(const char* data, size_t length) {
    int err = send(client_fd_, data, length, 0);
    if (err < 0) {
      TENSORSTORE_LOG("send error:", get_socket_errno());
      return NGHTTP2_ERR_CALLBACK_FAILURE;
    }
    TENSORSTORE_CHECK(err > 0);
    return err;
  }

  // Callbacks for nghttp2_session:
  static ssize_t Send(nghttp2_session* session, const uint8_t* data,
                      size_t length, int flags, void* user_data) {
    TENSORSTORE_LOG("http2 send ", length, ":",
                    absl::BytesToHexString(absl::string_view(
                        reinterpret_cast<const char*>(data), length)));
    return static_cast<Http2Session*>(user_data)->Send(
        reinterpret_cast<const char*>(data), length);
  }

  static int OnFrameSend(nghttp2_session* session, const nghttp2_frame* frame,
                         void* user_data) {
    const auto stream_id = frame->hd.stream_id;
    const auto type = frame->hd.type;
    TENSORSTORE_LOG("http2 frame send <", stream_id, ">: ", kFrameName[type]);
    return 0;
  }

  static int OnFrameRecv(nghttp2_session* session, const nghttp2_frame* frame,
                         void* user_data) {
    const auto stream_id = frame->hd.stream_id;
    const auto type = frame->hd.type;
    TENSORSTORE_LOG("http2 frame recv <", stream_id, ">: ", kFrameName[type]);

    if ((type == NGHTTP2_DATA || type == NGHTTP2_HEADERS) &&
        (frame->hd.flags & NGHTTP2_FLAG_END_STREAM)) {
      // The request is done.
      TENSORSTORE_LOG("http2 stream done <", stream_id, ">");

      // Update local stream tracking.
      static_cast<Http2Session*>(user_data)->OnStreamDone(stream_id);
    }
    return 0;
  }

  static int OnInvalidFrameRecv(nghttp2_session* session,
                                const nghttp2_frame* frame, int lib_error_code,
                                void* user_data) {
    const auto stream_id = frame->hd.stream_id;
    const auto type = frame->hd.type;
    TENSORSTORE_LOG("http2 frame recv invalid <", stream_id,
                    ">: ", kFrameName[type], " code=", lib_error_code);
    return 0;
  }

  static int OnHeader(nghttp2_session* session, const nghttp2_frame* frame,
                      const uint8_t* name, size_t namelen, const uint8_t* value,
                      size_t valuelen, uint8_t flags, void* user_data) {
    static_cast<Http2Session*>(user_data)->OnStreamHeader(
        frame->hd.stream_id,
        std::string(reinterpret_cast<const char*>(name), namelen),
        std::string(reinterpret_cast<const char*>(value), valuelen));
    return 0;
  }

  static int OnDataChunkRecv(nghttp2_session* session, uint8_t flags,
                             int32_t stream_id, const uint8_t* data, size_t len,
                             void* user_data) {
    TENSORSTORE_LOG("http2 recv chunk <", stream_id, ">");
    static_cast<Http2Session*>(user_data)->OnStreamData(
        stream_id, reinterpret_cast<const char*>(data), len);
    return 0;
  }

  static int OnStreamClose(nghttp2_session* session, int32_t stream_id,
                           uint32_t error_code, void* user_data) {
    TENSORSTORE_LOG("http2 stream close  <", stream_id, ">");
    return 0;
  }

  struct StringViewDataSource {
    absl::string_view view;
  };

  static ssize_t StringViewRead(nghttp2_session* session, int32_t stream_id,
                                uint8_t* buf, size_t length,
                                uint32_t* data_flags,
                                nghttp2_data_source* source, void*) {
    auto my_data = reinterpret_cast<StringViewDataSource*>(source->ptr);
    if (length > my_data->view.size()) {
      length = my_data->view.size();
      memcpy(buf, my_data->view.data(), length);
      *data_flags |= NGHTTP2_DATA_FLAG_EOF;
      delete my_data;
      return length;
    }
    memcpy(buf, my_data->view.data(), length);
    my_data->view.remove_prefix(length);
    return length;
  }

  Http2Session(socket_t client, absl::string_view settings)
      : client_fd_(client) {
    nghttp2_session_callbacks* callbacks;
    TENSORSTORE_CHECK(0 == nghttp2_session_callbacks_new(&callbacks));
    nghttp2_session_callbacks_set_send_callback(callbacks, &Http2Session::Send);
    nghttp2_session_callbacks_set_on_header_callback(callbacks,
                                                     &Http2Session::OnHeader);
    nghttp2_session_callbacks_set_on_data_chunk_recv_callback(
        callbacks, &Http2Session::OnDataChunkRecv);
    nghttp2_session_callbacks_set_on_stream_close_callback(
        callbacks, &Http2Session::OnStreamClose);
    nghttp2_session_callbacks_set_on_frame_recv_callback(
        callbacks, &Http2Session::OnFrameRecv);
    nghttp2_session_callbacks_set_on_frame_send_callback(
        callbacks, &Http2Session::OnFrameSend);
    nghttp2_session_callbacks_set_on_invalid_frame_recv_callback(
        callbacks, &Http2Session::OnInvalidFrameRecv);

    nghttp2_session_server_new2(&session_, callbacks, this, nullptr);
    nghttp2_session_callbacks_del(callbacks);

    // The initial stream id is 1.
    auto result = nghttp2_session_upgrade2(
        session_, reinterpret_cast<const uint8_t*>(settings.data()),
        settings.size(), false, nullptr);
    TENSORSTORE_CHECK(0 == result);

    // Queue a settings
    result = nghttp2_submit_settings(session_, NGHTTP2_FLAG_NONE, nullptr, 0);
    TENSORSTORE_CHECK(0 == result);
  }

  ~Http2Session() { nghttp2_session_del(session_); }

  void GoAway() { nghttp2_session_terminate_session(session_, 0); }

  bool Done() {
    return !nghttp2_session_want_write(session_) &&
           !nghttp2_session_want_read(session_);
  }

  bool TrySendReceive() {
    constexpr size_t kBufferSize = 4096;
    char buf[kBufferSize];

    nghttp2_session_send(session_);

    // Read as long as there is data available.
    for (; WaitForRead(client_fd_);) {
      int r = recv(client_fd_, buf, kBufferSize, 0);
      if (r < 0) {
        // WaitForRead calls select() on the socket, so we
        // should not see EAGAIN nor EWOULDBLOCK.
        TENSORSTORE_LOG("recv error: ", get_socket_errno());
        return false;
      }
      // No data here would be unexpected since WaitForRead calls select().
      TENSORSTORE_CHECK(r > 0);
      TENSORSTORE_LOG("socket recv: ", r);
      auto result = nghttp2_session_mem_recv(
          session_, reinterpret_cast<const uint8_t*>(buf), r);
      TENSORSTORE_CHECK(result >= 0);
    }
    return true;
  }

  void SendResponse(int32_t stream_id,
                    std::vector<std::pair<std::string, std::string>> headers,
                    absl::string_view data) {
    TENSORSTORE_CHECK(stream_id >= 0);
    TENSORSTORE_LOG("http2 respond <", stream_id,
                    ">: ", absl::BytesToHexString(data));

    const size_t num_headers = headers.size();
    std::unique_ptr<nghttp2_nv[]> nvs(new nghttp2_nv[num_headers]);
    for (size_t i = 0; i < num_headers; ++i) {
      auto& header = headers[i];
      nghttp2_nv* nv = &nvs[i];
      nv->name = reinterpret_cast<uint8_t*>(header.first.data());
      nv->value = reinterpret_cast<uint8_t*>(header.second.data());
      nv->namelen = header.first.size();
      nv->valuelen = header.second.size();
      nv->flags = NGHTTP2_NV_FLAG_NONE;
    }
    nghttp2_data_provider data_provider;
    if (!data.empty()) {
      data_provider.source.ptr = new StringViewDataSource{data};
      data_provider.read_callback = &Http2Session::StringViewRead;
    }
    auto result =
        nghttp2_submit_response(session_, stream_id, nvs.get(), num_headers,
                                data.empty() ? nullptr : &data_provider);
    TENSORSTORE_CHECK(0 == result);
  }
};

TEST_F(CurlTransportTest, Http2) {
  auto transport = ::tensorstore::internal_http::GetDefaultHttpTransport();

  // This test sets up a simple single-request tcp/ip service which allows
  // us to mock a simple HTTP/2 server.
  socket_t socket = CreateBoundSocket();
  TENSORSTORE_CHECK(socket != INVALID_SOCKET);

  auto hostport = FormatSocketAddress(socket);
  TENSORSTORE_CHECK(!hostport.empty());

  static constexpr char kSwitchProtocols[] =  // 69
      "HTTP/1.1 101 Switching Protocols\r\n"  // 35
      "Connection: Upgrade\r\n"               //
      "Upgrade: h2c\r\n"                      //
      "\r\n";

  // AAMAAABkAAQCAAAAAAIAAAAA
  static constexpr char kSettings[] = "\0\3\0\0\0\x64\0\4\2\0\0\0\0\2\0\0\0\0";

  std::string initial_request;
  std::string second_request;

  std::thread serve_thread = std::thread([&] {
    auto client_fd = AcceptNonBlocking(socket);
    initial_request = ReceiveAvailable(client_fd);

    // Manually upgrade the h2c to HTTP/2
    AssertSend(client_fd, kSwitchProtocols);

    Http2Session session(client_fd, absl::string_view(kSettings, 18));
    session.SendResponse(
        1, {{":status", "200"}, {"content-type", "text/html"}},
        "<html>\n<body>\n<h1>Hello, World!</h1>\n</body>\n</html>\n");
    session.TrySendReceive();

    // After that has been sent, we have an additional request to
    // handle,, but it is sent asynchronously on another thread,
    // so loop here. 10 is somewhat arbitrary, though several send/recv
    // calls are required to transmit various frames, since each stream
    // likely needs to send/recv HEADER, DATA, & WINDOW, and then the
    // GOAWAY is triggered below.
    for (int i = 0; i < 10; i++) {
      if (!session.TrySendReceive()) {
        // fd closed prematurely.
        closesocket(client_fd);
        return;
      }

      if (!session.completed.empty()) {
        auto it = session.completed.begin();
        session.SendResponse(
            session.completed.begin()->first,
            {{":status", "200"}, {"content-type", "text/html"}}, "McFly");
        session.completed.erase(it);
      }
    }
    session.TrySendReceive();
    session.GoAway();
    session.TrySendReceive();

    // We have not sent a shutdown message.
    closesocket(client_fd);
  });

  // Issue request 1.
  {
    auto response = transport->IssueRequest(
        HttpRequestBuilder(absl::StrCat("http://", hostport, "/"))
            .AddUserAgentPrefix("test")
            .AddHeader("X-foo: bar")
            .AddQueryParameter("name", "dragon")
            .AddQueryParameter("age", "1234")
            .EnableAcceptEncoding()
            .BuildRequest(),
        absl::Cord("Hello"));

    // Waits for the response.
    TENSORSTORE_LOG(GetStatus(response));

    using ::testing::HasSubstr;
    EXPECT_THAT(initial_request, HasSubstr("/?name=dragon&age=1234"));
    EXPECT_THAT(initial_request,
                HasSubstr(absl::StrCat("Host: ", hostport, "\r\n")));

    // User-Agent versions change based on zlib, nghttp2, and curl versions.
    EXPECT_THAT(initial_request, HasSubstr("User-Agent: testtensorstore/0.1 "));

    EXPECT_THAT(initial_request, HasSubstr("Accept: */*\r\n"));
    EXPECT_THAT(initial_request,
                HasSubstr("Accept-Encoding: deflate, gzip\r\n"));
    EXPECT_THAT(initial_request, HasSubstr("X-foo: bar\r\n"));
    EXPECT_THAT(initial_request, HasSubstr("Content-Length: 5"));
    EXPECT_THAT(
        initial_request,
        HasSubstr("Content-Type: application/x-www-form-urlencoded\r\n"));
    EXPECT_THAT(initial_request, HasSubstr("Hello"));

    EXPECT_EQ(200, response.value().status_code);
    EXPECT_EQ("<html>\n<body>\n<h1>Hello, World!</h1>\n</body>\n</html>\n",
              response.value().payload);
  }

  {
    auto response = transport->IssueRequest(
        HttpRequestBuilder(absl::StrCat("http://", hostport, "/boo"))
            .BuildRequest(),
        absl::Cord());

    // Waits for the response.
    TENSORSTORE_LOG(GetStatus(response));
  }

  serve_thread.join();
}

}  // namespace
