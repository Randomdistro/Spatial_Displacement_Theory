#include "sdt/solar_system/camera_controller.hpp"
#include <cmath>

namespace sdt::solar_system {

    CameraController::CameraController()
        : focus_(Vec3d::Zero())
        , azimuth_(0.0)
        , elevation_(M_PI / 6.0)  // 30 degrees
        , distance_(1e12)  // 1 AU default
    {
    }
    
    void CameraController::setFocus(const Vec3d& focus) {
        focus_ = focus;
    }
    
    void CameraController::orbit(double deltaAzimuth, double deltaElevation) {
        azimuth_ += deltaAzimuth;
        elevation_ += deltaElevation;
        
        // Clamp elevation
        if (elevation_ < MIN_ELEVATION) elevation_ = MIN_ELEVATION;
        if (elevation_ > MAX_ELEVATION) elevation_ = MAX_ELEVATION;
        
        // Normalize azimuth
        while (azimuth_ < 0) azimuth_ += 2.0 * M_PI;
        while (azimuth_ >= 2.0 * M_PI) azimuth_ -= 2.0 * M_PI;
    }
    
    void CameraController::setOrbit(double azimuth, double elevation) {
        azimuth_ = azimuth;
        elevation_ = elevation;
        
        // Clamp elevation
        if (elevation_ < MIN_ELEVATION) elevation_ = MIN_ELEVATION;
        if (elevation_ > MAX_ELEVATION) elevation_ = MAX_ELEVATION;
        
        // Normalize azimuth
        while (azimuth_ < 0) azimuth_ += 2.0 * M_PI;
        while (azimuth_ >= 2.0 * M_PI) azimuth_ -= 2.0 * M_PI;
    }
    
    void CameraController::pan(double deltaX, double deltaY) {
        // Pan in camera's right/up plane
        Vec3d right = getRight();
        Vec3d up = getUp();
        
        focus_ += right * deltaX + up * deltaY;
    }
    
    void CameraController::zoom(double factor) {
        distance_ *= factor;
        
        // Clamp distance
        if (distance_ < MIN_DISTANCE) distance_ = MIN_DISTANCE;
        if (distance_ > MAX_DISTANCE) distance_ = MAX_DISTANCE;
    }
    
    void CameraController::setDistance(double distance) {
        distance_ = distance;
        
        // Clamp distance
        if (distance_ < MIN_DISTANCE) distance_ = MIN_DISTANCE;
        if (distance_ > MAX_DISTANCE) distance_ = MAX_DISTANCE;
    }
    
    Vec3d CameraController::getPosition() const {
        // Calculate camera position from spherical coordinates
        const double cos_el = std::cos(elevation_);
        const double sin_el = std::sin(elevation_);
        const double cos_az = std::cos(azimuth_);
        const double sin_az = std::sin(azimuth_);
        
        Vec3d offset(
            distance_ * cos_el * cos_az,
            distance_ * cos_el * sin_az,
            distance_ * sin_el
        );
        
        return focus_ + offset;
    }
    
    Vec3d CameraController::getForward() const {
        Vec3d pos = getPosition();
        Vec3d forward = focus_ - pos;
        return forward.normalized();
    }
    
    Vec3d CameraController::getRight() const {
        Vec3d forward = getForward();
        Vec3d worldUp(0, 0, 1);
        Vec3d right = forward.cross(worldUp).normalized();
        return right;
    }
    
    Vec3d CameraController::getUp() const {
        Vec3d forward = getForward();
        Vec3d right = getRight();
        return right.cross(forward).normalized();
    }
    
    Mat4d CameraController::getViewMatrix() const {
        Vec3d pos = getPosition();
        Vec3d forward = getForward();
        Vec3d right = getRight();
        Vec3d up = getUp();
        
        // Build view matrix (look-at)
        Mat4d view = Mat4d::Identity();
        
        view(0, 0) = right.x();
        view(1, 0) = right.y();
        view(2, 0) = right.z();
        
        view(0, 1) = up.x();
        view(1, 1) = up.y();
        view(2, 1) = up.z();
        
        view(0, 2) = -forward.x();
        view(1, 2) = -forward.y();
        view(2, 2) = -forward.z();
        
        view(0, 3) = -right.dot(pos);
        view(1, 3) = -up.dot(pos);
        view(2, 3) = forward.dot(pos);
        
        return view;
    }
    
    void CameraController::reset() {
        focus_ = Vec3d::Zero();
        azimuth_ = 0.0;
        elevation_ = M_PI / 6.0;
        distance_ = 1e12;
    }

} // namespace sdt::solar_system

