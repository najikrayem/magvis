#include <gtest/gtest.h>
#include <Wire.hpp>

TEST(WireTest, wire_awg_to_diam_mm) {
    // conversion correct to 4 decimal places.
    EXPECT_NEAR(wire_awg_to_diam_mm(1), 7.3481, 1e-4);
    EXPECT_NEAR(wire_awg_to_diam_mm(5), 4.6213, 1e-4);
    EXPECT_NEAR(wire_awg_to_diam_mm(10), 2.5882, 1e-4);
    EXPECT_NEAR(wire_awg_to_diam_mm(15), 1.4495, 1e-4);
    EXPECT_NEAR(wire_awg_to_diam_mm(20), 0.8118, 1e-4);
    EXPECT_NEAR(wire_awg_to_diam_mm(25), 0.4547, 1e-4);
    EXPECT_NEAR(wire_awg_to_diam_mm(30), 0.2546, 1e-4);
    EXPECT_NEAR(wire_awg_to_diam_mm(35), 0.1426, 1e-4);
    EXPECT_NEAR(wire_awg_to_diam_mm(40), 0.0799, 1e-4);
}

TEST(WireTest, add_point){
    Vec3 v = Vec3(0,0,0);
    Vec3 u = Vec3(0,0,6);
    Wire wire;

    ASSERT_EQ(wire.points.size(), 0);
    ASSERT_EQ(wire.qps.size(), 0);
    ASSERT_EQ(wire.segments.size(), 0);

    wire.add_point(v);

    ASSERT_EQ(wire.points.size(), 1);
    ASSERT_EQ(wire.qps.size(), 0);
    ASSERT_EQ(wire.segments.size(), 0);

    wire.add_point(u);

    ASSERT_EQ(wire.points.size(), 2);
    ASSERT_EQ(wire.qps.size(), 1);
    ASSERT_EQ(wire.segments.size(), 1);

    EXPECT_FLOAT_EQ(wire.points[0].x, 0);
    EXPECT_FLOAT_EQ(wire.points[0].y, 0);
    EXPECT_FLOAT_EQ(wire.points[0].z, 0);

    EXPECT_FLOAT_EQ(wire.points[1].x, 0);
    EXPECT_FLOAT_EQ(wire.points[1].y, 0);
    EXPECT_FLOAT_EQ(wire.points[1].z, 6);

    EXPECT_FLOAT_EQ(wire.qps[0].x, 0);
    EXPECT_FLOAT_EQ(wire.qps[0].y, 0);
    EXPECT_FLOAT_EQ(wire.qps[0].z, 3);

    EXPECT_FLOAT_EQ(wire.segments[0].x, 0);
    EXPECT_FLOAT_EQ(wire.segments[0].y, 0);
    EXPECT_FLOAT_EQ(wire.segments[0].z, 6);

    Vec3 w = Vec3(0,0,9);
    wire.add_point(w);

    EXPECT_FLOAT_EQ(wire.segments[1].x, 0);
    EXPECT_FLOAT_EQ(wire.segments[1].y, 0);
    EXPECT_FLOAT_EQ(wire.segments[1].z, 3);
}