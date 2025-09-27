#include <gtest/gtest.h>
#include <Biot-Savart.hpp>


// TEST(BiotSavartTest, biot_savart_analytic_basic){
//     float current = 1;
    
//     Vec3 p = Vec3(0,0.05,0);

//     Vec3 a = Vec3(-1,0,0);
//     Vec3 b = Vec3(1,0,0);

//     Wire wire;
//     wire.add_point(a); wire.add_point(b);

//     auto field1 = biot_savart(p, wire, current);

//     EXPECT_NEAR(field1.z, 3.9950, 1e-4);
// }

TEST(BiotSavartTest, biot_savart_analytic_basic){
    // Geometry: segment from (-1,0,0) to (+1,0,0), current along +x
    // Field point: (0, 0.05, 0)
    // Expected: B points in -z, magnitude ≈ 3.99500935e-6 T

    const float I   = 1.0f;
    const float L   = 1.0f;          // half-length
    const float rho = 0.05f;

    const Vec3 p(0.0f, rho, 0.0f);
    const Vec3 a(-L, 0.0f, 0.0f);
    const Vec3 b( L, 0.0f, 0.0f);

    // Build a polyline with many small segments so midpoint Biot–Savart converges
    Wire wire;
    const int N = 1000; // increase if you need even tighter tolerance
    for (int k = 0; k <= N; ++k) {
        float t  = static_cast<float>(k) / static_cast<float>(N);
        Vec3 pt( a.x*(1.0f - t) + b.x*t,
                 a.y*(1.0f - t) + b.y*t,
                 a.z*(1.0f - t) + b.z*t );
        wire.add_point(pt);
    }

    Vec3 B = biot_savart(p, wire, I);

    // Analytic finite-segment result on perpendicular bisector:
    // B = (mu0 / (2π ρ)) * (L / sqrt(L^2 + ρ^2)), direction -z
    const float mu0_over_2pi = 2.0e-7f;
    const float expected_mag = (mu0_over_2pi / rho) * (L / std::sqrt(L*L + rho*rho));
    const float expected_Bz  = -expected_mag;

    // Tight absolute tolerances work because |B| is ~4e-6
    EXPECT_NEAR(B.x, 0.0f,          5e-8f);
    EXPECT_NEAR(B.y, 0.0f,          5e-8f);
    EXPECT_NEAR(B.z, expected_Bz,   2e-8f);
}
