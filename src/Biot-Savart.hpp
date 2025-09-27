#pragma once

#include "Vec3.hpp"
#include "Wire.hpp"

// p: Field evaluation 3D point
// w: Wire geometry (polyline)
// i: Current in Amps
// 
Vec3 biot_savart(const Vec3& p, const Wire& w, float i);
