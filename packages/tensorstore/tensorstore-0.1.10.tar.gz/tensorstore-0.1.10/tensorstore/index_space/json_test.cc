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

#include "tensorstore/index_space/json.h"

#include <gmock/gmock.h>
#include <gtest/gtest.h>
#include "tensorstore/index_space/dim_expression.h"
#include "tensorstore/index_space/index_domain_builder.h"
#include "tensorstore/index_space/index_transform_builder.h"
#include "tensorstore/internal/json.h"
#include "tensorstore/internal/json_gtest.h"
#include "tensorstore/util/result.h"
#include "tensorstore/util/status.h"
#include "tensorstore/util/status_testutil.h"

namespace {

using tensorstore::DimensionIndex;
using tensorstore::dynamic_rank;
using tensorstore::Index;
using tensorstore::IndexInterval;
using tensorstore::IndexTransform;
using tensorstore::IndexTransformBuilder;
using tensorstore::IndexTransformSpec;
using tensorstore::kInfIndex;
using tensorstore::kInfSize;
using tensorstore::MatchesJson;
using tensorstore::MatchesStatus;
using tensorstore::Result;
using tensorstore::internal::ParseJson;

IndexTransform<> MakeExampleTransform() {
  return tensorstore::IndexTransformBuilder<4, 3>()
      .input_origin({-kInfIndex, 7, -kInfIndex, 8})
      .input_exclusive_max({kInfIndex + 1, 10, kInfIndex + 1, 17})
      .implicit_lower_bounds({0, 0, 1, 1})
      .implicit_upper_bounds({0, 0, 1, 1})
      .input_labels({"x", "y", "z", "t"})
      .output_constant(0, 3)
      .output_single_input_dimension(1, 0, 2, 2)
      .output_index_array(2, 7, 1,
                          tensorstore::MakeArray<Index>({{
                              {{1}},
                              {{2}},
                              {{3}},
                          }}))
      .Finalize()
      .value();
}

IndexTransform<> MakeUnlabeledExampleTransform() {
  return tensorstore::IndexTransformBuilder<4, 3>()
      .input_origin({-kInfIndex, 7, -kInfIndex, 8})
      .input_exclusive_max({kInfIndex + 1, 10, kInfIndex + 1, 17})
      .implicit_lower_bounds({0, 0, 1, 1})
      .implicit_upper_bounds({0, 0, 1, 1})
      .output_constant(0, 3)
      .output_single_input_dimension(1, 0, 2, 2)
      .output_index_array(2, 7, 1,
                          tensorstore::MakeArray<Index>({{
                              {{1}},
                              {{2}},
                              {{3}},
                          }}),
                          IndexInterval::Closed(1, 2))
      .Finalize()
      .value();
}

::nlohmann::json MakeUnlabeledExampleJson() {
  return ParseJson(R"(
{
    "input_inclusive_min": ["-inf", 7, ["-inf"], [8]],
    "input_exclusive_max": ["+inf", 10, ["+inf"], [17]],
    "output": [
        {"offset": 3},
        {"stride": 2, "input_dimension": 2},
        {
            "offset": 7,
            "index_array": [[ [[1]], [[2]], [[3]] ]],
            "index_array_bounds": [1, 2]
        }
    ]
}
)");
}

::nlohmann::json MakeLabeledExampleJson() {
  return ParseJson(R"(
{
    "input_inclusive_min": ["-inf", 7, ["-inf"], [8]],
    "input_exclusive_max": ["+inf", 10, ["+inf"], [17]],
    "input_labels": ["x", "y", "z", "t"],
    "output": [
        {"offset": 3},
        {"stride": 2, "input_dimension": 2},
        {"offset": 7, "index_array": [[ [[1]], [[2]], [[3]] ]]}
    ]
}
)");
}

TEST(ToJsonTest, Unlabeled) {
  EXPECT_EQ(MakeUnlabeledExampleJson(),
            ::nlohmann::json(MakeUnlabeledExampleTransform()));
}

TEST(ToJsonTest, Labeled) {
  EXPECT_EQ(MakeLabeledExampleJson(), ::nlohmann::json(MakeExampleTransform()));
}

TEST(IndexTransformJsonBinderTest, IndexArrayOutOfBounds) {
  tensorstore::TestJsonBinderRoundTrip<IndexTransform<>>({
      // Index array does not contain out-of-bounds index.
      {IndexTransformBuilder(1, 1)
           .input_shape({3})
           .output_index_array(0, 0, 1,
                               tensorstore::MakeArray<Index>({1, 2, 3}))
           .Finalize()
           .value(),
       {
           {"input_inclusive_min", {0}},
           {"input_exclusive_max", {3}},
           {"output",
            {
                {{"index_array", {1, 2, 3}}},
            }},
       }},
      // Index array contains out-of-bounds index and `index_range` is
      // bounded.
      {IndexTransformBuilder(1, 1)
           .input_shape({3})
           .output_index_array(0, 0, 1,
                               tensorstore::MakeArray<Index>({1, 2, 3}),
                               IndexInterval::UncheckedClosed(1, 2))
           .Finalize()
           .value(),
       {
           {"input_inclusive_min", {0}},
           {"input_exclusive_max", {3}},
           {"output",
            {
                {{"index_array", {1, 2, 3}}, {"index_array_bounds", {1, 2}}},
            }},
       }},
      // Index array contains out-of-bounds index, but `index_range` is
      // unbounded anyway.
      {IndexTransformBuilder(1, 1)
           .input_shape({3})
           .output_index_array(
               0, 0, 1, tensorstore::MakeArray<Index>({1, kInfIndex + 1, 3}))
           .Finalize()
           .value(),
       {
           {"input_inclusive_min", {0}},
           {"input_exclusive_max", {3}},
           {"output",
            {
                {{"index_array", {1, kInfIndex + 1, 3}}},
            }},
       }},
  });
  tensorstore::TestJsonBinderToJson<IndexTransform<>>({
      // Because index array does not contain an out-of-bounds index, the
      // `index_range` of `[1, 3]` is not encoded.
      {IndexTransformBuilder(1, 1)
           .input_shape({3})
           .output_index_array(0, 0, 1,
                               tensorstore::MakeArray<Index>({1, 2, 3}),
                               IndexInterval::Closed(1, 3))
           .Finalize()
           .value(),
       ::testing::Optional(MatchesJson(::nlohmann::json{
           {"input_inclusive_min", {0}},
           {"input_exclusive_max", {3}},
           {"output",
            {
                {{"index_array", {1, 2, 3}}},
            }},
       }))},
  });
}

TEST(ToJsonTest, NullTransform) {
  EXPECT_TRUE(::nlohmann::json(tensorstore::IndexTransform<>()).is_discarded());
}

TEST(ToJsonTest, IdentityTransform) {
  EXPECT_EQ(ParseJson(R"(
{
    "input_inclusive_min": [1, 2],
    "input_exclusive_max": [4, 6]
}
)")
                .dump(),
            ::nlohmann::json(tensorstore::IdentityTransform(
                                 tensorstore::BoxView({1, 2}, {3, 4})))
                .dump());
}

TEST(ToJsonTest, Translation) {
  EXPECT_EQ(
      ::nlohmann::json({
          {"input_inclusive_min", {1, 2}},
          {"input_exclusive_max", {4, 6}},
          {"output",
           {
               {{"offset", -1}, {"input_dimension", 0}},
               {{"offset", -2}, {"input_dimension", 1}},
           }},
      }),
      ::nlohmann::json(ChainResult(tensorstore::IdentityTransform(
                                       tensorstore::BoxView({3, 4})),
                                   tensorstore::AllDims().TranslateTo({1, 2}))
                           .value()));
}

void TestRoundTripJson(const ::nlohmann::json& json) {
  SCOPED_TRACE(json.dump());
  auto parse_result = tensorstore::ParseIndexTransform(json);
  ASSERT_EQ(absl::OkStatus(), GetStatus(parse_result));
  EXPECT_EQ(json, ::nlohmann::json(*parse_result));
}

TEST(RoundTripJsonTest, Labels) {
  TestRoundTripJson({
      {"input_inclusive_min", {1}},
      {"input_exclusive_max", {3}},
      {"input_labels", {"x"}},
  });
  TestRoundTripJson({
      {"input_inclusive_min", {1}},
      {"input_exclusive_max", {3}},
  });
}

TEST(ParseIndexTransformTest, Null) {
  EXPECT_EQ(IndexTransform<>(),
            tensorstore::ParseIndexTransform(
                ::nlohmann::json(::nlohmann::json::value_t::discarded)));
}

TEST(ParseIndexTransformTest, DynamicFromLabeled) {
  EXPECT_EQ(MakeExampleTransform(),
            tensorstore::ParseIndexTransform(MakeLabeledExampleJson()));
}

TEST(ParseIndexTransformTest, DynamicFromUnlabeled) {
  EXPECT_EQ(MakeUnlabeledExampleTransform(),
            tensorstore::ParseIndexTransform(MakeUnlabeledExampleJson()));
}

TEST(ParseIndexTransformTest, Static) {
  auto t = tensorstore::ParseIndexTransform<4, 3>(MakeLabeledExampleJson());
  static_assert(std::is_same<decltype(t),
                             Result<tensorstore::IndexTransform<4, 3>>>::value,
                "");
  EXPECT_EQ(MakeExampleTransform(), t);
}

// Tests that omitting the `"output"` member results in an identity transform.
TEST(ParseIndexTransformTest, IdentityTransformExclusiveMax) {
  EXPECT_EQ(tensorstore::IndexTransformBuilder<>(2, 2)
                .input_origin({1, 2})
                .input_exclusive_max({5, kInfIndex + 1})
                .output_identity_transform()
                .Finalize()
                .value(),
            tensorstore::ParseIndexTransform(ParseJson(R"(
{
    "input_inclusive_min": [1, 2],
    "input_exclusive_max": [5, "+inf"]
}
)")));
}

TEST(ParseIndexTransformTest, IdentityTransformInclusiveMax) {
  EXPECT_EQ(tensorstore::IndexTransformBuilder<>(2, 2)
                .input_origin({1, 2})
                .input_inclusive_max({5, kInfIndex})
                .output_identity_transform()
                .Finalize()
                .value(),
            tensorstore::ParseIndexTransform(ParseJson(R"(
{
    "input_inclusive_min": [1, 2],
    "input_inclusive_max": [5, "+inf"]
}
)")));
}

TEST(ParseIndexTransformTest, IdentityTransformShape) {
  EXPECT_EQ(tensorstore::IndexTransformBuilder<>(2, 2)
                .input_origin({1, 2})
                .input_shape({5, kInfSize})
                .output_identity_transform()
                .Finalize()
                .value(),
            tensorstore::ParseIndexTransform(ParseJson(R"(
{
    "input_inclusive_min": [1, 2],
    "input_shape": [5, "+inf"]
}
)")));
}

TEST(ParseIndexTransformTest, IdentityTransformInputRank) {
  EXPECT_EQ(tensorstore::IndexTransformBuilder<>(2, 2)
                .output_identity_transform()
                .Finalize()
                .value(),
            tensorstore::ParseIndexTransform(ParseJson(R"(
{
    "input_rank": 2
}
)")));
}

TEST(ParseIndexTransformTest, StaticInputRankMismatch) {
  EXPECT_THAT(
      (tensorstore::ParseIndexTransform<3, 3>(MakeLabeledExampleJson())),
      MatchesStatus(absl::StatusCode::kInvalidArgument,
                    "Error parsing index transform from JSON: "  //
                    "Expected input_rank to be 3, but is: 4"));
}

TEST(ParseIndexTransformTest, StaticOutputRankMismatch) {
  EXPECT_THAT(
      (tensorstore::ParseIndexTransform<4, 2>(MakeLabeledExampleJson())),
      MatchesStatus(absl::StatusCode::kInvalidArgument,
                    "Error parsing index transform from JSON: "  //
                    "Expected output rank to be 2, but is: 3"));
}

TEST(ParseIndexTransformTest, MissingInputRank) {
  EXPECT_THAT(
      tensorstore::ParseIndexTransform(ParseJson(R"(
{
    "output": [
        {"offset": 3},
        {"stride": 2, "input_dimension": 2},
        {"offset": 7, "index_array": [[ [[1]], [[2]], [[3]] ]]}
    ]
}
)")),
      MatchesStatus(
          absl::StatusCode::kInvalidArgument,
          "Error parsing index transform from JSON: "  //
          "At least one of \"input_rank\", \"input_inclusive_min\", "
          "\"input_shape\", \"input_inclusive_max\", \"input_exclusive_max\", "
          "or \"input_labels\" must be specified"));
}

TEST(ParseIndexTransformTest, InvalidInputRank) {
  EXPECT_THAT(tensorstore::ParseIndexTransform(ParseJson(R"(
{
    "input_rank": -3
}
)")),
              MatchesStatus(absl::StatusCode::kInvalidArgument,
                            "Error parsing index transform from JSON: "  //
                            "Error parsing object member \"input_rank\": "
                            "Expected integer .*, but received: -3"));
}

TEST(ParseIndexTransformTest, InvalidShape) {
  EXPECT_THAT(tensorstore::ParseIndexTransform(ParseJson(R"(
{
    "input_inclusive_min": [1, 2],
    "input_shape": [1, 2, 3]
}
)")),
              MatchesStatus(absl::StatusCode::kInvalidArgument,
                            "Error parsing index transform from JSON: "  //
                            "Error parsing object member \"input_shape\": "
                            "Array has length 3 but should have length 2"));
}

TEST(ParseIndexTransformTest, ExclusiveMaxAndInclusiveMax) {
  EXPECT_THAT(
      tensorstore::ParseIndexTransform(ParseJson(R"(
{
    "input_inclusive_min": [1, 2],
    "input_exclusive_max": [5, 10],
    "input_inclusive_max": [5, 10]
}
)")),
      MatchesStatus(absl::StatusCode::kInvalidArgument,
                    "Error parsing index transform from JSON: "  //
                    "Error parsing object member "
                    "\"input_(exclusive_max|inclusive_max)\": "  //
                    "At most one of \"input_shape\", \"input_inclusive_max\", "
                    "and \"input_exclusive_max\" members must be specified"));
}

TEST(ParseIndexTransformTest, ExclusiveMaxAndShape) {
  EXPECT_THAT(
      tensorstore::ParseIndexTransform(ParseJson(R"(
{
    "input_inclusive_min": [1, 2],
    "input_exclusive_max": [5, 10],
    "input_shape": [5, 10]
}
)")),
      MatchesStatus(
          absl::StatusCode::kInvalidArgument,
          "Error parsing index transform from JSON: "                      //
          "Error parsing object member \"input_(exclusive_max|shape)\": "  //
          "At most one of \"input_shape\", \"input_inclusive_max\", and "
          "\"input_exclusive_max\" members must be specified"));
}

TEST(ParseIndexTransformTest, InclusiveMaxAndShape) {
  EXPECT_THAT(
      tensorstore::ParseIndexTransform(ParseJson(R"(
{
    "input_inclusive_min": [1, 2],
    "input_inclusive_max": [5, 10],
    "input_shape": [5, 10]
}
)")),
      MatchesStatus(
          absl::StatusCode::kInvalidArgument,
          "Error parsing index transform from JSON: "                      //
          "Error parsing object member \"input_(inclusive_max|shape)\": "  //
          "At most one of \"input_shape\", \"input_inclusive_max\", and "
          "\"input_exclusive_max\" members must be specified"));
}

// Tests that omitting the `"output"` member when `output_rank` is specified
// and does not match the input rank leads to an error.
TEST(ParseIndexTransformTest, MissingOutputs) {
  auto json = ParseJson(R"(
{
    "input_inclusive_min": [1, 2],
    "input_exclusive_max": [5, 10]
}
)");

  // Test successful case.
  EXPECT_EQ((tensorstore::IndexTransformBuilder<2, 2>()
                 .input_origin({1, 2})
                 .input_exclusive_max({5, 10})
                 .output_identity_transform()
                 .Finalize()
                 .value()),
            (tensorstore::ParseIndexTransform<dynamic_rank, 2>(json)));

  // Test failure case.
  EXPECT_THAT((tensorstore::ParseIndexTransform<dynamic_rank, 3>(json)),
              MatchesStatus(absl::StatusCode::kInvalidArgument,
                            "Error parsing index transform from JSON: "  //
                            "Missing \"output\" member"));
}

TEST(ParseIndexTransformTest, InvalidInterval) {
  EXPECT_THAT(tensorstore::ParseIndexTransform(ParseJson(R"(
{
    "input_inclusive_min": [1, 11],
    "input_exclusive_max": [5, 10]
}
)")),
              MatchesStatus(absl::StatusCode::kInvalidArgument));
}

TEST(ParseIndexTransformTest, UnexpectedTopLevelMember) {
  EXPECT_THAT((tensorstore::ParseIndexTransform(ParseJson(R"(
{
    "input_inclusive_min": [1, 2],
    "input_exclusive_max": [5, 10],
    "extra": "value"
}
)"))),
              MatchesStatus(absl::StatusCode::kInvalidArgument,
                            "Error parsing index transform from JSON: "
                            "Object includes extra members: \"extra\""));
}

TEST(ParseIndexTransformTest, UnexpectedOutputMember) {
  EXPECT_THAT((tensorstore::ParseIndexTransform(ParseJson(R"(
{
    "input_inclusive_min": [1],
    "input_exclusive_max": [2],
    "output": [
        {"extra": "value"}
    ]
}
)"))),
              MatchesStatus(absl::StatusCode::kInvalidArgument,
                            "Error parsing index transform from JSON: "
                            "Error parsing object member \"output\": "
                            "Error parsing value at position 0: "
                            "Object includes extra members: \"extra\""));
}

TEST(ParseIndexTransformTest, InvalidLabel) {
  EXPECT_THAT(tensorstore::ParseIndexTransform(ParseJson(R"(
{
    "input_inclusive_min": [1, 2],
    "input_exclusive_max": [5, 10],
    "input_labels": [1, 2]
}
)")),
              MatchesStatus(absl::StatusCode::kInvalidArgument,
                            "Error parsing index transform from JSON: "       //
                            "Error parsing object member \"input_labels\": "  //
                            "Error parsing value at position 0: "             //
                            "Expected string, but received: 1"));
}

TEST(ParseIndexTransformTest, InvalidBound) {
  EXPECT_THAT(
      tensorstore::ParseIndexTransform(ParseJson(R"(
{
    "input_inclusive_min": [1, "a"],
    "input_exclusive_max": [5, 10]
}
)")),
      MatchesStatus(absl::StatusCode::kInvalidArgument,
                    "Error parsing index transform from JSON: "              //
                    "Error parsing object member \"input_inclusive_min\": "  //
                    "Error parsing value at position 1: "                    //
                    "Expected 64-bit signed integer or \"-inf\", "
                    "but received: \"a\""));
}

TEST(ParseIndexTransformTest, InvalidBoundPositiveInfinity) {
  EXPECT_THAT(
      tensorstore::ParseIndexTransform(ParseJson(R"(
{
    "input_inclusive_min": [1, "+inf"],
    "input_exclusive_max": [5, 10]
}
)")),
      MatchesStatus(absl::StatusCode::kInvalidArgument,
                    "Error parsing index transform from JSON: "              //
                    "Error parsing object member \"input_inclusive_min\": "  //
                    "Error parsing value at position 1: "                    //
                    "Expected 64-bit signed integer or \"-inf\", "
                    "but received: \"\\+inf\""));
}

TEST(ParseIndexTransformTest, InvalidBoundNegativeInfinity) {
  EXPECT_THAT(
      tensorstore::ParseIndexTransform(ParseJson(R"(
{
    "input_inclusive_min": [1, "-inf"],
    "input_exclusive_max": [5, "-inf"]
}
)")),
      MatchesStatus(absl::StatusCode::kInvalidArgument,
                    "Error parsing index transform from JSON: "              //
                    "Error parsing object member \"input_exclusive_max\": "  //
                    "Error parsing value at position 1: "                    //
                    "Expected 64-bit signed integer or \"\\+inf\", "
                    "but received: \"-inf\""));
}

TEST(ParseIndexTransformTest, InvalidOutputOffset) {
  EXPECT_THAT(
      tensorstore::ParseIndexTransform(ParseJson(R"(
{
    "input_inclusive_min": [1],
    "input_exclusive_max": [5],
    "output": [
        {"offset": "a"}
    ]
}
)")),
      MatchesStatus(absl::StatusCode::kInvalidArgument,
                    "Error parsing index transform from JSON: "  //
                    "Error parsing object member \"output\": "   //
                    "Error parsing value at position 0: "        //
                    "Error parsing object member \"offset\": "   //
                    "Expected 64-bit signed integer, but received: \"a\""));
}

TEST(ParseIndexTransformTest, InvalidOutputStride) {
  EXPECT_THAT(
      tensorstore::ParseIndexTransform(ParseJson(R"(
{
    "input_inclusive_min": [1],
    "input_exclusive_max": [5],
    "output": [
        {"stride": "a", "input_dimension": 0}
    ]
}
)")),
      MatchesStatus(absl::StatusCode::kInvalidArgument,
                    "Error parsing index transform from JSON: "  //
                    "Error parsing object member \"output\": "   //
                    "Error parsing value at position 0: "        //
                    "Error parsing object member \"stride\": "   //
                    "Expected 64-bit signed integer, but received: \"a\""));
}

TEST(ParseIndexTransformTest, UnexpectedStride) {
  EXPECT_THAT(
      tensorstore::ParseIndexTransform(ParseJson(R"(
{
    "input_inclusive_min": [1],
    "input_exclusive_max": [5],
    "output": [
        {"stride": 1}
    ]
}
)")),
      MatchesStatus(absl::StatusCode::kInvalidArgument,
                    "Error parsing index transform from JSON: "  //
                    "Error parsing object member \"output\": "   //
                    "Error parsing value at position 0: "        //
                    "Error parsing object member \"stride\": "   //
                    "Either \"input_dimension\" or \"index_array\" must be "
                    "specified in conjunction with \"stride\""));
}

TEST(ParseIndexTransformTest, InvalidOutputInput) {
  EXPECT_THAT(
      tensorstore::ParseIndexTransform(ParseJson(R"(
{
    "input_inclusive_min": [1],
    "input_exclusive_max": [5],
    "output": [
        {"input_dimension": "a"}
    ]
}
)")),
      MatchesStatus(absl::StatusCode::kInvalidArgument,
                    "Error parsing index transform from JSON: "          //
                    "Error parsing object member \"output\": "           //
                    "Error parsing value at position 0: "                //
                    "Error parsing object member \"input_dimension\": "  //
                    "Expected 64-bit signed integer, but received: \"a\""));
}

TEST(ParseIndexTransformTest, InvalidOutputArray) {
  EXPECT_THAT(
      tensorstore::ParseIndexTransform(ParseJson(R"(
{
    "input_inclusive_min": [1],
    "input_exclusive_max": [5],
    "output": [
        {"index_array": "a"}
    ]
}
)")),
      MatchesStatus(absl::StatusCode::kInvalidArgument,
                    "Error parsing index transform from JSON: "         //
                    "Error parsing object member \"output\": "          //
                    "Error parsing value at position 0: "               //
                    "Error parsing object member \"index_array\": "     //
                    "Error parsing array element at position \\{\\}: "  //
                    "Expected 64-bit signed integer, but received: \"a\""));
}

TEST(ParseIndexTransformTest, InvalidOutputInputAndArray) {
  EXPECT_THAT(
      tensorstore::ParseIndexTransform(ParseJson(R"(
{
    "input_inclusive_min": [1],
    "input_exclusive_max": [5],
    "output": [
        {"input_dimension": 0, "index_array": [1]}
    ]
}
)")),
      MatchesStatus(
          absl::StatusCode::kInvalidArgument,
          "Error parsing index transform from JSON: "                        //
          "Error parsing object member \"output\": "                         //
          "Error parsing value at position 0: "                              //
          "Error parsing object member \"(index_array|input_dimension)\": "  //
          "At most one of \"input_dimension\" and \"index_array\" "
          "must be specified"));
}

TEST(ParseIndexTransformTest, DuplicateLabels) {
  EXPECT_THAT(tensorstore::ParseIndexTransform(ParseJson(R"(
{
    "input_labels": ["x", "x"]
}
)")),
              MatchesStatus(absl::StatusCode::kInvalidArgument,
                            "Error parsing index transform from JSON: "  //
                            "Dimension label.*"));
}

TEST(IndexTransformSpecTest, JsonBinding) {
  const auto binder = tensorstore::internal::json_binding::Object(
      tensorstore::IndexTransformSpecBinder);
  tensorstore::TestJsonBinderRoundTrip<IndexTransformSpec>(
      {
          {IndexTransformSpec(), ::nlohmann::json::object()},
          {IndexTransformSpec(3), {{"rank", 3}}},
          {IndexTransformSpec(0), {{"rank", 0}}},
          {IndexTransformSpec(32), {{"rank", 32}}},
          {IndexTransformSpec(IndexTransformBuilder<>(2, 1)
                                  .input_shape({2, 3})
                                  .output_identity_transform()
                                  .Finalize()
                                  .value()),
           {{"transform",
             {
                 {"input_exclusive_max", {2, 3}},
                 {"input_inclusive_min", {0, 0}},
                 {"output", {{{"input_dimension", 0}}}},
             }}}},
      },
      binder);
  tensorstore::TestJsonBinderFromJson<IndexTransformSpec>(
      {
          {{{"rank", 33}}, MatchesStatus(absl::StatusCode::kInvalidArgument)},
      },
      binder);
}

TEST(IndexDomainJsonBinderTest, Simple) {
  tensorstore::TestJsonBinderRoundTrip<tensorstore::IndexDomain<>>({
      {tensorstore::IndexDomainBuilder<4>()
           .origin({-kInfIndex, 7, -kInfIndex, 8})
           .exclusive_max({kInfIndex + 1, 10, kInfIndex + 1, 17})
           .implicit_lower_bounds({0, 0, 1, 1})
           .implicit_upper_bounds({0, 0, 1, 1})
           .labels({"x", "y", "z", "t"})
           .Finalize()
           .value(),
       {
           {"inclusive_min", {"-inf", 7, {"-inf"}, {8}}},
           {"exclusive_max", {"+inf", 10, {"+inf"}, {17}}},
           {"labels", {"x", "y", "z", "t"}},
       }},
  });
  tensorstore::TestJsonBinderFromJson<tensorstore::IndexDomain<>>({
      {{
           {"rank", 33},
       },
       MatchesStatus(
           absl::StatusCode::kInvalidArgument,
           "Error parsing index domain from JSON: "
           "Error parsing object member \"rank\": "
           "Expected integer in the range \\[0, 32\\], but received: 33")},
      {{
           {"shape", {1, 1, 1, 1, 1, 1, 1, 1, 1, 1,  //
                      1, 1, 1, 1, 1, 1, 1, 1, 1, 1,  //
                      1, 1, 1, 1, 1, 1, 1, 1, 1, 1,  //
                      1, 1, 1}},
       },
       MatchesStatus(absl::StatusCode::kInvalidArgument,
                     "Error parsing index domain from JSON: "
                     "Error parsing object member \"shape\": "
                     "Rank 33 is outside valid range \\[0, 32\\]")},
      {{
           {"labels", {"", "", "", "", "", "", "", "", "", "",  //
                       "", "", "", "", "", "", "", "", "", "",  //
                       "", "", "", "", "", "", "", "", "", "",  //
                       "", "", ""}},
       },
       MatchesStatus(absl::StatusCode::kInvalidArgument,
                     "Error parsing index domain from JSON: "
                     "Error parsing object member \"labels\": "
                     "Rank 33 is outside valid range \\[0, 32\\]")},
      {{
           {"inclusive_min", {"-inf", 7, {"-inf"}, {8}}},
           {"exclusive_max", {"+inf", 10, {"+inf"}, {17}}},
           {"labels", {"x", "y", "z", "t"}},
           {"output", "abc"},
       },
       MatchesStatus(absl::StatusCode::kInvalidArgument,
                     "Error parsing index domain from JSON: "
                     "Object includes extra members: \"output\"")},
  });
}

TEST(IndexBinderTest, Basic) {
  using tensorstore::kMaxFiniteIndex;
  tensorstore::TestJsonBinderRoundTrip<Index>(
      {
          {-kInfIndex, "-inf"},
          {+kInfIndex, "+inf"},
          {-kMaxFiniteIndex, -kMaxFiniteIndex},
          {0, 0},
          {5, 5},
          {+kMaxFiniteIndex, +kMaxFiniteIndex},
      },
      tensorstore::internal::json_binding::IndexBinder);
  tensorstore::TestJsonBinderFromJson<Index>(
      {
          {"abc", MatchesStatus(absl::StatusCode::kInvalidArgument)},
          {-kInfIndex, ::testing::Optional(MatchesJson(-kInfIndex))},
          {+kInfIndex, ::testing::Optional(MatchesJson(+kInfIndex))},
          {-kInfIndex - 1, MatchesStatus(absl::StatusCode::kInvalidArgument)},
          {kInfIndex + 1, MatchesStatus(absl::StatusCode::kInvalidArgument)},
      },
      tensorstore::internal::json_binding::IndexBinder);
}

TEST(IndexIntervalBinderTest, Basic) {
  using tensorstore::IndexInterval;
  tensorstore::TestJsonBinderRoundTrip<IndexInterval>({
      {IndexInterval::UncheckedClosed(5, 10), {5, 10}},
      {IndexInterval(), {"-inf", "+inf"}},
      {IndexInterval::UncheckedClosed(5, 4), {5, 4}},
      {IndexInterval::UncheckedClosed(-kInfIndex, 20), {"-inf", 20}},
      {IndexInterval::UncheckedClosed(20, +kInfIndex), {20, "+inf"}},
  });
  tensorstore::TestJsonBinderFromJson<IndexInterval>({
      {"abc", MatchesStatus(absl::StatusCode::kInvalidArgument)},
      {{-kInfIndex - 1, 10}, MatchesStatus(absl::StatusCode::kInvalidArgument)},
      {{10, 5}, MatchesStatus(absl::StatusCode::kInvalidArgument)},
  });
}

}  // namespace
