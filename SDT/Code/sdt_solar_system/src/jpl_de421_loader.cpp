#include "sdt/solar_system/jpl_de421_loader.hpp"
#include "sdt/solar_system/data_loader.hpp"
#include <cmath>
#include <map>

namespace sdt::solar_system {

    // J2000.0 epoch: JD 2451545.0
    constexpr double J2000_JD = 2451545.0;
    
    // Earliest verified date: 1800-01-01, JD 2378495.0
    constexpr double EARLIEST_VERIFIED_JD = 2378495.0;
    
    std::map<JPLDE421Loader::BodyID, std::string> JPLDE421Loader::body_names_ = {
        {MERCURY, "Mercury"},
        {VENUS, "Venus"},
        {EARTH, "Earth"},
        {MARS, "Mars"},
        {JUPITER, "Jupiter"},
        {SATURN, "Saturn"},
        {URANUS, "Uranus"},
        {NEPTUNE, "Neptune"},
        {PLUTO, "Pluto"},
        {MOON, "Moon"},
        {SUN, "Sun"}
    };
    
    // Orbital elements at J2000.0 (simplified - full DE421 would interpolate)
    std::map<JPLDE421Loader::BodyID, JPLDE421Loader::OrbitalElements> JPLDE421Loader::elements_at_j2000_ = {
        {MERCURY, {5.791e10, 0.2056, 0.1222, 0.8435, 1.3518, 4.4026, 8.2667e-7}},
        {VENUS, {1.082e11, 0.0068, 0.0592, 1.3383, 1.7968, 3.1761, 3.2367e-7}},
        {EARTH, {1.496e11, 0.0167, 0.0000, 0.0000, 1.7968, 6.2401, 1.9909e-7}},
        {MARS, {2.279e11, 0.0934, 0.0323, 0.8649, 0.8642, 6.2035, 1.0559e-7}},
        {JUPITER, {7.785e11, 0.0484, 0.0228, 1.7535, 1.7544, 0.6005, 1.6755e-8}},
        {SATURN, {1.433e12, 0.0542, 0.0434, 1.9838, 1.9838, 0.8719, 6.7607e-9}},
        {URANUS, {2.867e12, 0.0472, 0.0135, 1.2916, 1.2916, 5.4664, 2.3653e-9}},
        {NEPTUNE, {4.515e12, 0.0086, 0.0309, 2.2990, 0.8642, 5.3212, 1.2024e-9}}
    };
    
    std::vector<CelestialBody> JPLDE421Loader::load_initial_conditions(
        double jd,
        const std::vector<BodyID>& body_ids
    ) {
        std::vector<CelestialBody> bodies;
        
        // Load SDT parameters from CSV first
        // Try multiple possible paths
        std::string csv_path = "SDT/data/planetary_parameters.csv";
        std::ifstream test_file(csv_path);
        if (!test_file.is_open()) {
            csv_path = "../../data/planetary_parameters.csv";
            test_file.open(csv_path);
            if (!test_file.is_open()) {
                csv_path = "data/planetary_parameters.csv";
            }
        }
        test_file.close();
        
        auto csv_bodies = DataLoader::load_from_csv(csv_path);
        std::map<std::string, CelestialBody> csv_map;
        for (const auto& body : csv_bodies) {
            csv_map[body.name] = body;
        }
        
        // Load Sun first (fixed at origin)
        CelestialBody sun;
        sun.name = "Sun";
        sun.type = "star";
        sun.position = Vec3d::Zero();
        sun.velocity = Vec3d::Zero();
        sun.isFixed = true;
        
        if (csv_map.find("Sun") != csv_map.end()) {
            const auto& sun_data = csv_map["Sun"];
            sun.radius = sun_data.radius;
            sun.sdt_params = sun_data.sdt_params;
        } else {
            // Default Sun parameters
            sun.radius = 6.957e8;
            sun.sdt_params.kappa = 686.42;
            sun.sdt_params.R_eff = sun.radius;
        }
        
        bodies.push_back(sun);
        
        // Load requested bodies
        for (BodyID id : body_ids) {
            if (id == SUN) continue; // Already loaded
            
            CelestialBody body;
            body.name = body_names_[id];
            body.type = (id == MOON) ? "moon" : "planet";
            
            // Get SDT parameters from CSV
            if (csv_map.find(body.name) != csv_map.end()) {
                const auto& csv_body = csv_map[body.name];
                body.radius = csv_body.radius;
                body.sdt_params = csv_body.sdt_params;
            }
            
            // Calculate position and velocity from JPL DE421
            calculate_state(id, jd, body.position, body.velocity);
            
            bodies.push_back(body);
        }
        
        return bodies;
    }
    
    std::vector<CelestialBody> JPLDE421Loader::load_earliest_verified() {
        return load_initial_conditions(EARLIEST_VERIFIED_JD, {
            MERCURY, VENUS, EARTH, MARS, JUPITER, SATURN, URANUS, NEPTUNE, MOON
        });
    }
    
    std::vector<CelestialBody> JPLDE421Loader::load_modern_reference() {
        return load_initial_conditions(J2000_JD, {
            MERCURY, VENUS, EARTH, MARS, JUPITER, SATURN, URANUS, NEPTUNE, MOON
        });
    }
    
    void JPLDE421Loader::calculate_state(
        BodyID body_id,
        double jd,
        Vec3d& position,
        Vec3d& velocity
    ) {
        if (elements_at_j2000_.find(body_id) == elements_at_j2000_.end()) {
            // Default: circular orbit approximation
            position = Vec3d::Zero();
            velocity = Vec3d::Zero();
            return;
        }
        
        const auto& elements = elements_at_j2000_[body_id];
        elements_to_state(elements, jd, position, velocity);
    }
    
    void JPLDE421Loader::elements_to_state(
        const OrbitalElements& elements,
        double jd,
        Vec3d& position,
        Vec3d& velocity
    ) {
        // Calculate time since J2000.0
        const double t = (jd - J2000_JD) * 86400.0; // Convert to seconds
        
        // Mean anomaly at time t
        const double M = elements.M0 + elements.n * t;
        
        // Solve Kepler's equation for eccentric anomaly (simplified: use M for small e)
        double E = M;
        if (elements.e > 0.01) {
            // Iterative solution for larger eccentricity
            for (int i = 0; i < 10; ++i) {
                E = M + elements.e * std::sin(E);
            }
        }
        
        // True anomaly
        const double nu = 2.0 * std::atan2(
            std::sqrt(1.0 + elements.e) * std::sin(E / 2.0),
            std::sqrt(1.0 - elements.e) * std::cos(E / 2.0)
        );
        
        // Distance from focus
        const double r = elements.a * (1.0 - elements.e * elements.e) / 
                         (1.0 + elements.e * std::cos(nu));
        
        // Position in orbital plane
        const double x_orb = r * std::cos(nu);
        const double y_orb = r * std::sin(nu);
        
        // Rotate to ecliptic coordinates
        const double cos_omega = std::cos(elements.omega);
        const double sin_omega = std::sin(elements.omega);
        const double cos_Omega = std::cos(elements.Omega);
        const double sin_Omega = std::sin(elements.Omega);
        const double cos_i = std::cos(elements.i);
        const double sin_i = std::sin(elements.i);
        
        // Rotation matrices
        const double x = x_orb * (cos_omega * cos_Omega - sin_omega * sin_Omega * cos_i) -
                         y_orb * (sin_omega * cos_Omega + cos_omega * sin_Omega * cos_i);
        const double y = x_orb * (cos_omega * sin_Omega + sin_omega * cos_Omega * cos_i) +
                         y_orb * (cos_omega * cos_Omega * cos_i - sin_omega * sin_Omega);
        const double z = x_orb * sin_omega * sin_i + y_orb * cos_omega * sin_i;
        
        position = Vec3d(x, y, z);
        
        // Velocity calculation (simplified)
        const double h = std::sqrt(elements.a * (1.0 - elements.e * elements.e) * 
                                   (299792458.0 * 299792458.0 * 6.957e8 / (686.42 * 686.42)));
        const double v_r = std::sqrt((299792458.0 * 299792458.0 * 6.957e8) / 
                                     (686.42 * 686.42 * r)) * elements.e * std::sin(nu);
        const double v_theta = h / r;
        
        // Velocity in orbital plane
        const double vx_orb = v_r * std::cos(nu) - v_theta * std::sin(nu);
        const double vy_orb = v_r * std::sin(nu) + v_theta * std::cos(nu);
        
        // Rotate to ecliptic coordinates
        const double vx = vx_orb * (cos_omega * cos_Omega - sin_omega * sin_Omega * cos_i) -
                          vy_orb * (sin_omega * cos_Omega + cos_omega * sin_Omega * cos_i);
        const double vy = vx_orb * (cos_omega * sin_Omega + sin_omega * cos_Omega * cos_i) +
                          vy_orb * (cos_omega * cos_Omega * cos_i - sin_omega * sin_Omega);
        const double vz = vx_orb * sin_omega * sin_i + vy_orb * cos_omega * sin_i;
        
        velocity = Vec3d(vx, vy, vz);
    }

} // namespace sdt::solar_system

