#include "Biot-Savart.hpp"

Vec3 biot_savart(const Vec3& p, const Wire& w, float current){

    //biot-savart accumulator
    Vec3 b;

    for (auto i = 0; i < w.segments.size(); i++){
        const Vec3& m = w.qps[i];
        const Vec3& seg = w.segments[i];

        Vec3 R = p - m;
        float r = R.norm();
        float denominator = r*r*r;
        Vec3 numerator = (seg.cross(R) * current);
        b = b + (numerator / denominator);
    }

    return (b * 1e-7); 
    
};
