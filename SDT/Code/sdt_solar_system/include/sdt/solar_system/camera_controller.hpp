#pragma once

#include <Eigen/Dense>
#include <cmath>

namespace sdt::solar_system {

    using Vec3d = Eigen::Vector3d;
    using Mat4d = Eigen::Matrix4d;

    /**
     * 3D Camera Controller
     * Provides orbit, pan, and zoom controls for 3D navigation
     */
    class CameraController {
    public:
        CameraController();
        
        // Set focus point (e.g., planet position)
        void setFocus(const Vec3d& focus);
        Vec3d getFocus() const { return focus_; }
        
        // Orbit controls (rotate around focus)
        void orbit(double deltaAzimuth, double deltaElevation);
        void setOrbit(double azimuth, double elevation);
        
        // Pan controls (translate focus)
        void pan(double deltaX, double deltaY);
        
        // Zoom controls
        void zoom(double factor);
        void setDistance(double distance);
        double getDistance() const { return distance_; }
        
        // Get view matrix
        Mat4d getViewMatrix() const;
        
        // Get camera position
        Vec3d getPosition() const;
        
        // Get camera forward/right/up vectors
        Vec3d getForward() const;
        Vec3d getRight() const;
        Vec3d getUp() const;
        
        // Reset to default view
        void reset();
        
    private:
        Vec3d focus_;          // Focus point (world space)
        double azimuth_;       // Horizontal angle (radians)
        double elevation_;     // Vertical angle (radians)
        double distance_;      // Distance from focus
        
        // Clamp elevation to prevent gimbal lock
        static constexpr double MIN_ELEVATION = -M_PI / 2.0 + 0.1;
        static constexpr double MAX_ELEVATION = M_PI / 2.0 - 0.1;
        static constexpr double MIN_DISTANCE = 1e9;  // 1 million km minimum
        static constexpr double MAX_DISTANCE = 1e15; // 1 light-year maximum
    };

} // namespace sdt::solar_system

