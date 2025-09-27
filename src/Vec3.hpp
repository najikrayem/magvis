#pragma once

#include <cmath>


// 16 byte alignment necessary for SIMD in the future
struct alignas(16) Vec3 {
    float x;
    float y;
    float z;

    constexpr Vec3() noexcept : x(0), y(0), z(0) {}
    constexpr Vec3(float x, float y, float z) noexcept : x(x), y(y), z(z) {}

    constexpr Vec3 operator+(const Vec3& other) const noexcept{
        return Vec3(x + other.x, y + other.y, z + other.z);
    }

    constexpr Vec3 operator-(const Vec3& other) const noexcept{
        return Vec3(x - other.x, y - other.y, z - other.z);
    }

    constexpr Vec3 operator/(float other) const noexcept{
        return Vec3(x / other, y / other, z / other);
    }

    constexpr Vec3 operator*(float other) const noexcept{
        return Vec3(x * other, y * other, z * other);
    }

    constexpr Vec3 cross(const Vec3& o) const noexcept {
        return Vec3((y*o.z) - (z*o.y), (z*o.x) - (x*o.z), (x*o.y) - (y*o.x));
    }

    float norm() const noexcept {
        return sqrt(x*x + y*y + z*z);
    }
};