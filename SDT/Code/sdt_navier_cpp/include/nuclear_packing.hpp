#pragma once

#include <array>
#include <algorithm>
#include <cmath>
#include <numbers>
#include <string>
#include <utility>
#include <vector>

#include "nuclear_geometry_occlusion.hpp"

namespace sdt::nuclear::packing {

// ============================================================================
// FUNDAMENTAL CONSTANTS (Phase 1 Nuclear Packing)
// ============================================================================
namespace constants {
    inline constexpr double r_nucleon_fm = 0.84;  // fm (packing radius)
    inline constexpr double second_layer_total_width_fm = 10.0 * r_nucleon_fm;  // from doc
    inline constexpr double second_layer_center_radius_fm = 4.0 * r_nucleon_fm;  // width=10r => center radius=5r - r
    inline constexpr double inter_alpha_spacing_fm = occlusion::constants::dist_inter_alpha_fm;
}

// ============================================================================
// ICOSAHEDRAL GEOMETRY
// ============================================================================
struct IcosahedralVertex {
    int index;
    double r;
    double theta;  // azimuthal (rad)
    double phi;    // polar (rad)
    double x;
    double y;
    double z;

    [[nodiscard]] double distance_to(const IcosahedralVertex& other) const {
        const double dx = x - other.x;
        const double dy = y - other.y;
        const double dz = z - other.z;
        return std::sqrt(dx * dx + dy * dy + dz * dz);
    }
};

struct OctahedralSpace {
    int index;
    std::pair<int, int> vertex_pair;
    double separation_fm;
    double expected_separation_fm;
    double excess_fm;

    [[nodiscard]] std::string description() const {
        return "Octahedral space " + std::to_string(index + 1) +
               ": between vertices " + std::to_string(vertex_pair.first) +
               " and " + std::to_string(vertex_pair.second);
    }
};

class IcosahedralBase {
public:
    explicit IcosahedralBase(double r_fm = constants::r_nucleon_fm)
        : r_(r_fm),
          central_sphere_radius_fm_(r_fm),
          outer_sphere_radius_fm_(r_fm),
          outer_sphere_distance_fm_(2.0 * r_fm),
          total_width_fm_(6.0 * r_fm) {
        vertices_ = generate_vertices();
        faces_ = generate_faces();
        octahedral_spaces_ = identify_octahedral_spaces();
    }

    [[nodiscard]] double r_fm() const { return r_; }
    [[nodiscard]] double central_sphere_radius_fm() const { return central_sphere_radius_fm_; }
    [[nodiscard]] double outer_sphere_radius_fm() const { return outer_sphere_radius_fm_; }
    [[nodiscard]] double outer_sphere_distance_fm() const { return outer_sphere_distance_fm_; }
    [[nodiscard]] double total_width_fm() const { return total_width_fm_; }

    [[nodiscard]] const std::vector<IcosahedralVertex>& vertices() const { return vertices_; }
    [[nodiscard]] const std::vector<OctahedralSpace>& octahedral_spaces() const { return octahedral_spaces_; }
    [[nodiscard]] const std::vector<std::array<int, 3>>& faces() const { return faces_; }

    [[nodiscard]] std::vector<std::array<double, 3>> vertex_coordinates() const {
        std::vector<std::array<double, 3>> coords;
        coords.reserve(vertices_.size());
        for (const auto& v : vertices_) {
            coords.push_back({v.x, v.y, v.z});
        }
        return coords;
    }

    [[nodiscard]] std::vector<std::vector<double>> vertex_distances() const {
        const std::size_t n = vertices_.size();
        std::vector<std::vector<double>> dist(n, std::vector<double>(n, 0.0));
        for (std::size_t i = 0; i < n; ++i) {
            for (std::size_t j = i + 1; j < n; ++j) {
                const double d = vertices_[i].distance_to(vertices_[j]);
                dist[i][j] = d;
                dist[j][i] = d;
            }
        }
        return dist;
    }

    [[nodiscard]] double solid_angle_occlusion(
        const std::array<double, 3>& observer_position_fm,
        double observer_distance_fm
    ) const {
        double total = 0.0;

        // Central sphere occlusion
        if (observer_distance_fm > central_sphere_radius_fm_) {
            total += occlusion::math::spherical_occlusion(
                central_sphere_radius_fm_,
                observer_distance_fm
            );
        }

        // Outer spheres
        for (const auto& v : vertices_) {
            const double dx = v.x - observer_position_fm[0];
            const double dy = v.y - observer_position_fm[1];
            const double dz = v.z - observer_position_fm[2];
            const double dist = std::sqrt(dx * dx + dy * dy + dz * dz);
            if (dist > outer_sphere_radius_fm_) {
                total += occlusion::math::spherical_occlusion(
                    outer_sphere_radius_fm_,
                    dist
                );
            }
        }
        return total;
    }

private:
    double r_;
    double central_sphere_radius_fm_;
    double outer_sphere_radius_fm_;
    double outer_sphere_distance_fm_;
    double total_width_fm_;
    std::vector<IcosahedralVertex> vertices_;
    std::vector<OctahedralSpace> octahedral_spaces_;
    std::vector<std::array<int, 3>> faces_;

    [[nodiscard]] std::vector<IcosahedralVertex> generate_vertices() const {
        std::vector<IcosahedralVertex> vertices;
        vertices.reserve(12);

        const double phi_icosa = (1.0 + std::sqrt(5.0)) / 2.0;
        const double scale = outer_sphere_distance_fm_ /
                             std::sqrt(1.0 + phi_icosa * phi_icosa);

        auto add_vertex = [&](double x, double y, double z) {
            const double r = std::sqrt(x * x + y * y + z * z);
            double theta = std::atan2(y, x);
            double phi = (r > 0.0) ? std::acos(z / r) : 0.0;

            // Normalize to outer_sphere_distance_fm_
            double nx = x, ny = y, nz = z;
            if (r > 0.0) {
                const double scale_factor = outer_sphere_distance_fm_ / r;
                nx *= scale_factor;
                ny *= scale_factor;
                nz *= scale_factor;
            }

            const int idx = static_cast<int>(vertices.size());
            vertices.push_back({idx, outer_sphere_distance_fm_, theta, phi, nx, ny, nz});
        };

        // (0, ±1, ±phi)
        for (int s1 : {-1, 1}) {
            for (int s2 : {-1, 1}) {
                add_vertex(0.0, s1 * scale, s2 * scale * phi_icosa);
            }
        }
        // (±1, ±phi, 0)
        for (int s1 : {-1, 1}) {
            for (int s2 : {-1, 1}) {
                add_vertex(s1 * scale, s2 * scale * phi_icosa, 0.0);
            }
        }
        // (±phi, 0, ±1)
        for (int s1 : {-1, 1}) {
            for (int s2 : {-1, 1}) {
                add_vertex(s1 * scale * phi_icosa, 0.0, s2 * scale);
            }
        }

        if (vertices.size() > 12) {
            vertices.resize(12);
        }
        return vertices;
    }

    [[nodiscard]] std::vector<OctahedralSpace> identify_octahedral_spaces() const {
        struct PairDistance {
            int i;
            int j;
            double distance;
            double expected;
        };

        std::vector<PairDistance> distances;
        const std::size_t n = vertices_.size();
        distances.reserve(n * (n - 1) / 2);

        for (std::size_t i = 0; i < n; ++i) {
            for (std::size_t j = i + 1; j < n; ++j) {
                const double dist = vertices_[i].distance_to(vertices_[j]);
                distances.push_back({
                    static_cast<int>(i),
                    static_cast<int>(j),
                    dist,
                    2.0 * r_
                });
            }
        }

        std::sort(distances.begin(), distances.end(),
                  [](const PairDistance& a, const PairDistance& b) {
                      return (a.distance - a.expected) > (b.distance - b.expected);
                  });

        std::vector<OctahedralSpace> spaces;
        const std::size_t count = std::min<std::size_t>(2, distances.size());
        spaces.reserve(count);
        for (std::size_t idx = 0; idx < count; ++idx) {
            const auto& d = distances[idx];
            spaces.push_back({
                static_cast<int>(idx),
                {d.i, d.j},
                d.distance,
                d.expected,
                d.distance - d.expected
            });
        }
        return spaces;
    }

    [[nodiscard]] std::vector<std::array<int, 3>> generate_faces() const {
        // Standard icosahedron face indices for the vertex ordering generated above.
        // This list assumes the canonical (0..11) order from generate_vertices().
        return {
            {0, 1, 4}, {0, 4, 9}, {9, 4, 5}, {4, 8, 5}, {4, 1, 8},
            {8, 1, 10}, {8, 10, 3}, {5, 8, 3}, {5, 3, 2}, {2, 3, 7},
            {7, 3, 10}, {7, 10, 6}, {7, 6, 11}, {11, 6, 0}, {0, 6, 1},
            {6, 10, 1}, {9, 5, 2}, {9, 2, 11}, {9, 11, 0}, {11, 2, 7}
        };
    }
};

// ============================================================================
// SECOND LAYER STRUCTURE (Phase 1.3)
// ============================================================================
class SecondLayer {
public:
    explicit SecondLayer(const IcosahedralBase& base)
        : base_(base) {
        interstices_ = compute_interstices();
    }

    [[nodiscard]] const std::vector<std::array<double, 3>>& interstices() const {
        return interstices_;
    }

    [[nodiscard]] std::size_t count() const { return interstices_.size(); }

private:
    const IcosahedralBase& base_;
    std::vector<std::array<double, 3>> interstices_;

    [[nodiscard]] static std::array<double, 3> normalize(const std::array<double, 3>& v) {
        const double norm = std::sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2]);
        if (norm <= 0.0) {
            return {1.0, 0.0, 0.0};
        }
        return {v[0] / norm, v[1] / norm, v[2] / norm};
    }

    [[nodiscard]] std::vector<std::array<double, 3>> compute_interstices() const {
        std::vector<std::array<double, 3>> points;
        const auto& verts = base_.vertices();
        const auto& faces = base_.faces();
        points.reserve(faces.size());

        for (const auto& face : faces) {
            const auto& a = verts[face[0]];
            const auto& b = verts[face[1]];
            const auto& c = verts[face[2]];

            // Centroid direction for triangular interstice
            std::array<double, 3> centroid = {
                (a.x + b.x + c.x) / 3.0,
                (a.y + b.y + c.y) / 3.0,
                (a.z + b.z + c.z) / 3.0
            };
            centroid = normalize(centroid);

            // Place second-layer center at defined radius
            points.push_back({
                centroid[0] * constants::second_layer_center_radius_fm,
                centroid[1] * constants::second_layer_center_radius_fm,
                centroid[2] * constants::second_layer_center_radius_fm
            });
        }

        return points;
    }
};

// ============================================================================
// FIRST SHELL COMPLETION (Phase 1.2)
// ============================================================================
struct DeuteronStructure {
    std::array<double, 3> proton_position_fm;
    std::array<double, 3> neutron_position_fm;
    double separation_fm;
    int octahedral_space_index = 0;

    [[nodiscard]] double occlusion_sr() const {
        return occlusion::math::spherical_occlusion(constants::r_nucleon_fm, separation_fm);
    }

    [[nodiscard]] double infer_k_binding_MeV_per_sr(double B_deuteron_exp_MeV) const {
        const double omega = occlusion_sr();
        if (omega <= 0.0) {
            return 0.0;
        }
        return B_deuteron_exp_MeV / omega;
    }
};

struct HeliumDeuteronStructure {
    std::array<double, 3> proton_position_fm;
    std::array<double, 3> neutron_position_fm;
    double separation_fm;
    int octahedral_space_index = 1;

    [[nodiscard]] double occlusion_sr() const {
        return occlusion::math::spherical_occlusion(constants::r_nucleon_fm, separation_fm);
    }
};

struct AlphaParticleStructure {
    DeuteronStructure deuteron;
    HeliumDeuteronStructure helium_deuteron;

    [[nodiscard]] double total_occlusion_sr() const {
        return deuteron.occlusion_sr() + helium_deuteron.occlusion_sr();
    }

    [[nodiscard]] double binding_energy_MeV(double k_binding_MeV_per_sr) const {
        return total_occlusion_sr() * k_binding_MeV_per_sr;
    }
};

class FirstShellBuilder {
public:
    explicit FirstShellBuilder(const IcosahedralBase& base)
        : base_(base) {}

    [[nodiscard]] DeuteronStructure build_deuteron(double separation_fm) const {
        const auto& spaces = base_.octahedral_spaces();
        const std::array<double, 3> center = {0.0, 0.0, 0.0};
        const std::array<double, 3> axis = pick_axis_from_space(spaces.empty() ? nullptr : &spaces[0]);
        return {
            offset(center, axis, -separation_fm / 2.0),
            offset(center, axis,  separation_fm / 2.0),
            separation_fm,
            0
        };
    }

    [[nodiscard]] HeliumDeuteronStructure build_helium_deuteron(double separation_fm) const {
        const auto& spaces = base_.octahedral_spaces();
        const std::array<double, 3> center = {0.0, 0.0, 0.0};
        const std::array<double, 3> axis = pick_axis_from_space(
            (spaces.size() > 1) ? &spaces[1] : nullptr
        );
        return {
            offset(center, axis, -separation_fm / 2.0),
            offset(center, axis,  separation_fm / 2.0),
            separation_fm,
            1
        };
    }

    [[nodiscard]] AlphaParticleStructure build_alpha(double separation_fm) const {
        return {
            build_deuteron(separation_fm),
            build_helium_deuteron(separation_fm)
        };
    }

private:
    const IcosahedralBase& base_;

    [[nodiscard]] static std::array<double, 3> normalize(const std::array<double, 3>& v) {
        const double norm = std::sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2]);
        if (norm <= 0.0) {
            return {1.0, 0.0, 0.0};
        }
        return {v[0] / norm, v[1] / norm, v[2] / norm};
    }

    [[nodiscard]] std::array<double, 3> pick_axis_from_space(const OctahedralSpace* space) const {
        if (!space || base_.vertices().empty()) {
            return {1.0, 0.0, 0.0};
        }
        const auto& v1 = base_.vertices()[space->vertex_pair.first];
        const auto& v2 = base_.vertices()[space->vertex_pair.second];
        std::array<double, 3> axis = {v1.x + v2.x, v1.y + v2.y, v1.z + v2.z};
        return normalize(axis);
    }

    [[nodiscard]] static std::array<double, 3> offset(
        const std::array<double, 3>& origin,
        const std::array<double, 3>& axis,
        double distance
    ) {
        return {
            origin[0] + axis[0] * distance,
            origin[1] + axis[1] * distance,
            origin[2] + axis[2] * distance
        };
    }
};

// ============================================================================
// ALPHA-CLUSTER ARRANGEMENTS (Phase 1.3 Continuation)
// ============================================================================
struct ClusterNode {
    std::array<double, 3> position_fm;
};

struct ClusterBond {
    int a;
    int b;
    double separation_fm;
};

struct AlphaClusterArrangement {
    std::string name;
    std::vector<ClusterNode> nodes;
    std::vector<ClusterBond> bonds;
    double alpha_radius_fm;

    [[nodiscard]] double total_bond_occlusion_sr() const {
        double total = 0.0;
        for (const auto& bond : bonds) {
            total += occlusion::math::spherical_occlusion(alpha_radius_fm, bond.separation_fm);
        }
        return total;
    }

    [[nodiscard]] double binding_energy_MeV(double k_binding_MeV_per_sr) const {
        return total_bond_occlusion_sr() * k_binding_MeV_per_sr;
    }
};

class AlphaClusterBuilder {
public:
    explicit AlphaClusterBuilder(double alpha_radius_fm)
        : alpha_radius_fm_(alpha_radius_fm) {}

    [[nodiscard]] AlphaClusterArrangement build_triangle(double spacing_fm = constants::inter_alpha_spacing_fm) const {
        // Equilateral triangle in xy-plane, centered at origin
        const double a = spacing_fm;
        const double h = std::sqrt(3.0) * 0.5 * a;
        std::vector<ClusterNode> nodes = {
            {{-0.5 * a, -h / 3.0, 0.0}},
            {{ 0.5 * a, -h / 3.0, 0.0}},
            {{ 0.0,      2.0 * h / 3.0, 0.0}}
        };
        std::vector<ClusterBond> bonds = {
            {0, 1, a},
            {1, 2, a},
            {2, 0, a}
        };
        return {"C-12 (Triangle)", std::move(nodes), std::move(bonds), alpha_radius_fm_};
    }

    [[nodiscard]] AlphaClusterArrangement build_tetrahedron(double spacing_fm = constants::inter_alpha_spacing_fm) const {
        // Regular tetrahedron centered at origin
        const double a = spacing_fm;
        // For vertices at (±s,±s,±s) as below, edge length is 2*sqrt(2)*s.
        // Choose s so that edge length equals a.
        const double s = a / (2.0 * std::sqrt(2.0));
        std::vector<ClusterNode> nodes = {
            {{ s,  s,  s}},
            {{ s, -s, -s}},
            {{-s,  s, -s}},
            {{-s, -s,  s}}
        };
        std::vector<ClusterBond> bonds;
        for (int i = 0; i < 4; ++i) {
            for (int j = i + 1; j < 4; ++j) {
                bonds.push_back({i, j, a});
            }
        }
        return {"O-16 (Tetrahedron)", std::move(nodes), std::move(bonds), alpha_radius_fm_};
    }

    [[nodiscard]] AlphaClusterArrangement build_octahedron(double spacing_fm = constants::inter_alpha_spacing_fm) const {
        // Regular octahedron centered at origin (6 nodes)
        const double a = spacing_fm;
        const double s = a / std::sqrt(2.0);
        std::vector<ClusterNode> nodes = {
            {{ s, 0.0, 0.0}},
            {{-s, 0.0, 0.0}},
            {{0.0,  s, 0.0}},
            {{0.0, -s, 0.0}},
            {{0.0, 0.0,  s}},
            {{0.0, 0.0, -s}}
        };
        std::vector<ClusterBond> bonds;
        for (int i = 0; i < 6; ++i) {
            for (int j = i + 1; j < 6; ++j) {
                // Octahedron edges: nodes that are perpendicular (dot=0)
                const auto& a_pos = nodes[i].position_fm;
                const auto& b_pos = nodes[j].position_fm;
                const double dot = a_pos[0] * b_pos[0] + a_pos[1] * b_pos[1] + a_pos[2] * b_pos[2];
                if (std::abs(dot) < 1e-9) {
                    bonds.push_back({i, j, a});
                }
            }
        }
        return {"Mg-24 (Octahedron)", std::move(nodes), std::move(bonds), alpha_radius_fm_};
    }

private:
    double alpha_radius_fm_;
};

// ============================================================================
// OVERLAP-CORRECTED OCCLUSION (Phase 1.5)
// ============================================================================
struct OcclusionSphere {
    std::array<double, 3> center_fm;
    double radius_fm;
};

inline std::vector<std::array<double, 3>> fibonacci_directions(std::size_t count) {
    std::vector<std::array<double, 3>> dirs;
    if (count == 0) return dirs;
    dirs.reserve(count);
    const double golden = (1.0 + std::sqrt(5.0)) / 2.0;
    const double golden_angle = 2.0 * std::numbers::pi * (1.0 - 1.0 / golden);
    for (std::size_t i = 0; i < count; ++i) {
        const double t = (count == 1) ? 0.0 : static_cast<double>(i) / static_cast<double>(count - 1);
        const double z = 1.0 - 2.0 * t;
        const double r = std::sqrt(std::max(0.0, 1.0 - z * z));
        const double theta = golden_angle * static_cast<double>(i);
        dirs.push_back({r * std::cos(theta), r * std::sin(theta), z});
    }
    return dirs;
}

inline double occlusion_solid_angle_sampled(
    const std::vector<OcclusionSphere>& spheres,
    const std::array<double, 3>& observer_position_fm,
    std::size_t samples = 2000
) {
    if (spheres.empty() || samples == 0) {
        return 0.0;
    }

    const auto dirs = fibonacci_directions(samples);
    std::size_t occluded = 0;

    for (const auto& dir : dirs) {
        bool blocked = false;
        for (const auto& sphere : spheres) {
            // Ray-sphere intersection from observer toward direction
            const double ox = observer_position_fm[0];
            const double oy = observer_position_fm[1];
            const double oz = observer_position_fm[2];

            const double cx = sphere.center_fm[0];
            const double cy = sphere.center_fm[1];
            const double cz = sphere.center_fm[2];

            const double dx = dir[0];
            const double dy = dir[1];
            const double dz = dir[2];

            const double lx = cx - ox;
            const double ly = cy - oy;
            const double lz = cz - oz;
            const double t_ca = lx * dx + ly * dy + lz * dz;
            if (t_ca <= 0.0) {
                continue;
            }
            const double d2 = (lx * lx + ly * ly + lz * lz) - t_ca * t_ca;
            if (d2 <= sphere.radius_fm * sphere.radius_fm) {
                blocked = true;
                break;
            }
        }
        if (blocked) {
            ++occluded;
        }
    }

    const double fraction = static_cast<double>(occluded) / static_cast<double>(samples);
    return 4.0 * std::numbers::pi * fraction;
}

}  // namespace sdt::nuclear::packing
