#pragma once

#include <vector>
#include "Vec3.hpp"

// helper function
float wire_awg_to_diam_mm(float awg);


class Wire {
public:
    // these points represent the polyline path. 
    std::vector<Vec3> points;

    // quadrature points, i.e midpoints of each edge
    std::vector<Vec3> qps;

    // segments
    std::vector<Vec3> segments;

    Wire();
    void add_point(Vec3 point);     //TODO optimize this

    

};


