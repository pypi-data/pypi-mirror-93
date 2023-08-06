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

#include "tensorstore/internal/http/http_request.h"

#include <gmock/gmock.h>
#include <gtest/gtest.h>

using tensorstore::internal_http::HttpRequestBuilder;

namespace {

TEST(HttpRequestBuilder, BuildRequest) {
  auto request = HttpRequestBuilder("http://127.0.0.1:0/")
                     .AddUserAgentPrefix("test")
                     .AddHeader("X-foo: bar")
                     .AddQueryParameter("name", "dragon")
                     .AddQueryParameter("age", "1234")
                     .SetMethod("CUSTOM")
                     .EnableAcceptEncoding()
                     .BuildRequest();

  EXPECT_EQ("http://127.0.0.1:0/?name=dragon&age=1234", request.url());
  EXPECT_TRUE(request.accept_encoding());
  EXPECT_EQ("test", request.user_agent());
  EXPECT_EQ("CUSTOM", request.method());
  EXPECT_THAT(request.headers(), testing::ElementsAre("X-foo: bar"));
}

}  // namespace
