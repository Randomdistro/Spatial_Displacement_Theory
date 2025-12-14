#pragma once

#include "celestial_body.hpp"
#include <vector>
#include <Eigen/Dense>

namespace sdt::solar_system {

    using Vec3d = Eigen::Vector3d;

    /**
     * Point Particle System for Visualization Markers
     * Calculates white point particles at specific orbital distances
     */
    class PointParticleSystem {
    public:
        struct Marker {
            Vec3d position;
            double radius;  // Orbital radius where marker is placed
            std::string label;
        };
        
        /**
         * Calculate marker positions based on orbital distances
         * Markers are placed at:
         * - 50% Mercury orbital radius
         * - Mercury orbit (20% offset from planet)
         * - Halfway to Venus
         * - Venus orbit (20% offset)
         * - Halfway Venus→Earth
         * - Earth orbit
         * - 1/3 and 2/3 to Mars
         * - Mars orbit
         * - Continue pattern for outer planets
         */
        static std::vector<Marker> calculateMarkers(
            const std::vector<CelestialBody>& bodies
        );
        
        /**
         * Get marker position at specific orbital radius
         * Ensures at least 20% orbital distance from planet
         */
        static Vec3d getMarkerPosition(
            double orbitalRadius,
            const CelestialBody& primary,
            const std::vector<CelestialBody>& allBodies
        );
        
    private:
        // Minimum distance from planet (20% of orbital radius)
        static constexpr double MIN_DISTANCE_FACTOR = 0.2;
    };

} // namespace sdt::solar_system

