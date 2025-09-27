#include <gtest/gtest.h>
#include <Vec3.hpp>

TEST(Vec3Test, constructor_default) {
    Vec3 v;
    ASSERT_FLOAT_EQ(v.x, 0);
    ASSERT_FLOAT_EQ(v.y, 0);
    ASSERT_FLOAT_EQ(v.z, 0);
}

TEST(Vec3Test, constructor_assign) {
    Vec3 v = Vec3(1.1,2.2,3.3);
    ASSERT_FLOAT_EQ(v.x, 1.1);
    ASSERT_FLOAT_EQ(v.y, 2.2);
    ASSERT_FLOAT_EQ(v.z, 3.3);
}


TEST(Vec3Test, addition) {
    Vec3 v = Vec3(1.1,2.2,3.3);
    Vec3 u = Vec3(4.5,6.7,8.9);
    Vec3 w = v+u;
    ASSERT_FLOAT_EQ(w.x, 5.6);
    ASSERT_FLOAT_EQ(w.y, 8.9);
    ASSERT_FLOAT_EQ(w.z, 12.2);
}

TEST(Vec3Test, subtraction) {
    Vec3 v = Vec3(4.5,6.7,8.9);
    Vec3 u = Vec3(1.1,2.2,3.3);
    Vec3 w = v-u;
    ASSERT_FLOAT_EQ(w.x, 3.4);
    ASSERT_FLOAT_EQ(w.y, 4.5);
    ASSERT_FLOAT_EQ(w.z, 5.6);
}

TEST(Vec3Test, multiplication) {
    Vec3 v = Vec3(1,5,8);
    float u = 2;
    Vec3 w = v*u;
    ASSERT_FLOAT_EQ(w.x, 2);
    ASSERT_FLOAT_EQ(w.y, 10);
    ASSERT_FLOAT_EQ(w.z, 16);
}

TEST(Vec3Test, division) {
    Vec3 v = Vec3(1,5,8);
    float u = 2;
    Vec3 w = v/u;
    ASSERT_FLOAT_EQ(w.x, 0.5);
    ASSERT_FLOAT_EQ(w.y, 2.5);
    ASSERT_FLOAT_EQ(w.z, 4);
}

TEST(Vec3Test, cross){
    Vec3 v = Vec3(1,2,3);
    Vec3 u = Vec3(1,5,7);
    Vec3 w = v.cross(u);
    ASSERT_FLOAT_EQ(w.x, -1);
    ASSERT_FLOAT_EQ(w.y, -4);
    ASSERT_FLOAT_EQ(w.z, 3);

    v = Vec3(-1,-2,3);
    u = Vec3(4,0,-8);
    w = v.cross(u);
    ASSERT_FLOAT_EQ(w.x, 16);
    ASSERT_FLOAT_EQ(w.y, 4);
    ASSERT_FLOAT_EQ(w.z, 8);
}


TEST(Vec3Test, norm){
    Vec3 v = Vec3(2,4,-2);
    EXPECT_NEAR(v.norm(), 4.8989, 1e-4);
    v = Vec3(1,0,-3);
    EXPECT_NEAR(v.norm(), 3.1622, 1e-4);
}