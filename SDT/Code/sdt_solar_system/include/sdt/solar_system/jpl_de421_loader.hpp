#pragma once

#include "celestial_body.hpp"
#include <string>
#include <vector>
#include <map>
#include <memory>

namespace sdt::solar_system {

    /**
     * JPL DE421 Ephemeris Loader
     * Loads initial conditions from JPL Development Ephemeris 421
     * DE421 covers 1900-2050 with high precision
     */
    class JPLDE421Loader {
    public:
        // Body IDs for JPL DE421
        enum BodyID {
            MERCURY = 1,
            VENUS = 2,
            EARTH = 3,
            MARS = 4,
            JUPITER = 5,
            SATURN = 6,
            URANUS = 7,
            NEPTUNE = 8,
            PLUTO = 9,
            MOON = 10,
            SUN = 11
        };
        
        /**
         * Load initial conditions from JPL DE421 at specified Julian Date
         * @param jd Julian Date (e.g., 2415020.5 for 1900-01-01)
         * @param body_ids List of body IDs to load
         * @return Vector of celestial bodies with positions and velocities
         */
        static std::vector<CelestialBody> load_initial_conditions(
            double jd,
            const std::vector<BodyID>& body_ids
        );
        
        /**
         * Load earliest verified ephemeris (1800-01-01, JD 2378495.0)
         * This is the earliest date with 100% verified data
         */
        static std::vector<CelestialBody> load_earliest_verified();
        
        /**
         * Load modern reference ephemeris (2000-01-01, JD 2451545.0)
         * For comparison with simulation results
         */
        static std::vector<CelestialBody> load_modern_reference();
        
        /**
         * Calculate position and velocity from JPL DE421
         * Uses simplified calculation - full implementation would use DE421 binary file
         * For now, uses orbital elements approximation
         */
        static void calculate_state(
            BodyID body_id,
            double jd,
            Vec3d& position,
            Vec3d& velocity
        );
        
    private:
        // Map body IDs to names
        static std::map<BodyID, std::string> body_names_;
        
        // Orbital elements at J2000.0 (for approximation)
        struct OrbitalElements {
            double a;      // Semi-major axis (m)
            double e;      // Eccentricity
            double i;      // Inclination (rad)
            double Omega;  // Longitude of ascending node (rad)
            double omega;  // Argument of perihelion (rad)
            double M0;     // Mean anomaly at epoch (rad)
            double n;      // Mean motion (rad/s)
        };
        
        static std::map<BodyID, OrbitalElements> elements_at_j2000_;
        
        // Convert orbital elements to position and velocity
        static void elements_to_state(
            const OrbitalElements& elements,
            double jd,
            Vec3d& position,
            Vec3d& velocity
        );
    };

} // namespace sdt::solar_system

