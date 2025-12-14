#include "sdt/solar_system/point_particle_system.hpp"
#include <algorithm>
#include <cmath>

namespace sdt::solar_system {

    std::vector<PointParticleSystem::Marker> PointParticleSystem::calculateMarkers(
        const std::vector<CelestialBody>& bodies
    ) {
        std::vector<Marker> markers;
        
        // Find Sun (primary)
        const CelestialBody* sun = nullptr;
        for (const auto& body : bodies) {
            if (body.name == "Sun") {
                sun = &body;
                break;
            }
        }
        
        if (!sun) return markers;
        
        // Get planets in order of distance
        std::vector<const CelestialBody*> planets;
        for (const auto& body : bodies) {
            if (body.type == "planet" && body.name != "Sun") {
                planets.push_back(&body);
            }
        }
        
        // Sort by distance from Sun
        std::sort(planets.begin(), planets.end(), [sun](const CelestialBody* a, const CelestialBody* b) {
            return (a->position - sun->position).norm() < (b->position - sun->position).norm();
        });
        
        if (planets.empty()) return markers;
        
        // Mercury markers
        if (planets.size() > 0) {
            const auto& mercury = *planets[0];
            double mercuryDist = (mercury.position - sun->position).norm();
            
            // 50% Mercury orbital radius
            Marker m1;
            m1.radius = mercuryDist * 0.5;
            m1.position = getMarkerPosition(m1.radius, *sun, bodies);
            m1.label = "50% Mercury";
            markers.push_back(m1);
            
            // Mercury orbit (20% offset)
            Marker m2;
            m2.radius = mercuryDist;
            m2.position = getMarkerPosition(m2.radius, *sun, bodies);
            m2.label = "Mercury Orbit";
            markers.push_back(m2);
        }
        
        // Inter-planetary markers
        for (size_t i = 0; i < planets.size() - 1; ++i) {
            const auto& inner = *planets[i];
            const auto& outer = *planets[i + 1];
            
            double innerDist = (inner.position - sun->position).norm();
            double outerDist = (outer.position - sun->position).norm();
            double midDist = (innerDist + outerDist) / 2.0;
            
            // Halfway marker
            Marker mid;
            mid.radius = midDist;
            mid.position = getMarkerPosition(mid.radius, *sun, bodies);
            mid.label = "Halfway " + inner.name + "→" + outer.name;
            markers.push_back(mid);
            
            // Outer planet orbit (20% offset)
            Marker outer_marker;
            outer_marker.radius = outerDist;
            outer_marker.position = getMarkerPosition(outer_marker.radius, *sun, bodies);
            outer_marker.label = outer.name + " Orbit";
            markers.push_back(outer_marker);
            
            // For Mars and beyond, add 1/3 and 2/3 markers
            if (i >= 2) { // Mars is index 3 (Mercury=0, Venus=1, Earth=2, Mars=3)
                double dist1 = innerDist + (outerDist - innerDist) / 3.0;
                double dist2 = innerDist + 2.0 * (outerDist - innerDist) / 3.0;
                
                Marker m1_3;
                m1_3.radius = dist1;
                m1_3.position = getMarkerPosition(m1_3.radius, *sun, bodies);
                m1_3.label = "1/3 " + inner.name + "→" + outer.name;
                markers.push_back(m1_3);
                
                Marker m2_3;
                m2_3.radius = dist2;
                m2_3.position = getMarkerPosition(m2_3.radius, *sun, bodies);
                m2_3.label = "2/3 " + inner.name + "→" + outer.name;
                markers.push_back(m2_3);
            }
        }
        
        return markers;
    }
    
    Vec3d PointParticleSystem::getMarkerPosition(
        double orbitalRadius,
        const CelestialBody& primary,
        const std::vector<CelestialBody>& allBodies
    ) {
        // Place marker in ecliptic plane (z=0) at specified radius
        Vec3d direction(1.0, 0.0, 0.0); // Default direction
        
        // Check if any planet is too close
        double minSeparation = orbitalRadius * MIN_DISTANCE_FACTOR;
        
        // Find a safe angle
        bool foundSafe = false;
        for (double angle = 0; angle < 2.0 * M_PI && !foundSafe; angle += M_PI / 12.0) {
            direction = Vec3d(std::cos(angle), std::sin(angle), 0.0);
            Vec3d candidatePos = primary.position + direction * orbitalRadius;
            
            bool tooClose = false;
            for (const auto& body : allBodies) {
                if (&body == &primary) continue;
                double dist = (body.position - candidatePos).norm();
                double bodyDist = (body.position - primary.position).norm();
                
                // Check if marker is too close to planet
                if (dist < std::max(minSeparation, bodyDist * MIN_DISTANCE_FACTOR)) {
                    tooClose = true;
                    break;
                }
            }
            
            if (!tooClose) {
                foundSafe = true;
            }
        }
        
        return primary.position + direction * orbitalRadius;
    }

} // namespace sdt::solar_system

