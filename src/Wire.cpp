#include "Wire.hpp"
#include <cmath>

Wire::Wire(){};

void Wire::add_point(Vec3 point){
    auto& pts = this->points;
    auto& qps = this->qps;
    auto& seg = this->segments; 

    pts.push_back(point);

    auto len = pts.size();

    if (len > 1){
        // add quadrature point m=(a+b)/2
        Vec3 m = pts[len - 2] + point;
        m = m / 2.0;
        qps.push_back(m);

        // add segment vector
        Vec3 seg_vec = point - pts[len - 2];
        seg.push_back(seg_vec);
    }
}

float wire_awg_to_diam_mm(float awg) {
    return 0.127 * (std::pow(92, ((36.0f - awg) / 39.0f)));
}
