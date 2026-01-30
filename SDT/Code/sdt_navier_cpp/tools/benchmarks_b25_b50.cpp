#include <array>
#include <chrono>
#include <cmath>
#include <filesystem>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <optional>
#include <sstream>
#include <string>
#include <string_view>
#include <vector>

#include "../include/nuclear_geometry_occlusion.hpp"
#include "../include/nuclear_packing.hpp"
#include "../include/sdt_navier/fields.hpp"

namespace fs = std::filesystem;

namespace {

// -----------------------------------------------------------------------------
// Minimal JSON helpers (no external deps)
// -----------------------------------------------------------------------------
std::string json_escape(std::string_view s) {
    std::ostringstream o;
    for (char c : s) {
        switch (c) {
            case '\\': o << "\\\\"; break;
            case '"': o << "\\\""; break;
            case '\b': o << "\\b"; break;
            case '\f': o << "\\f"; break;
            case '\n': o << "\\n"; break;
            case '\r': o << "\\r"; break;
            case '\t': o << "\\t"; break;
            default:
                // Control chars must be escaped in JSON
                if (static_cast<unsigned char>(c) < 0x20) {
                    o << "\\u" << std::hex << std::setw(4) << std::setfill('0')
                      << (static_cast<int>(static_cast<unsigned char>(c))) << std::dec;
                } else {
                    o << c;
                }
        }
    }
    return o.str();
}

std::string now_iso8601() {
    using namespace std::chrono;
    const auto now = system_clock::now();
    const std::time_t t = system_clock::to_time_t(now);
    std::tm tm{};
#if defined(_WIN32)
    gmtime_s(&tm, &t);
#else
    gmtime_r(&t, &tm);
#endif
    std::ostringstream ss;
    ss << std::put_time(&tm, "%Y-%m-%dT%H:%M:%SZ");
    return ss.str();
}

void ensure_dir(const fs::path& p) {
    std::error_code ec;
    fs::create_directories(p, ec);
    if (ec) {
        throw std::runtime_error("Failed to create directory: " + p.string() + " (" + ec.message() + ")");
    }
}

void write_text(const fs::path& p, const std::string& text) {
    ensure_dir(p.parent_path());
    std::ofstream f(p, std::ios::binary);
    if (!f) throw std::runtime_error("Failed to open for writing: " + p.string());
    f.write(text.data(), static_cast<std::streamsize>(text.size()));
}

std::optional<fs::path> find_repo_root_from(const fs::path& start) {
    fs::path cur = fs::absolute(start);
    for (int depth = 0; depth < 10; ++depth) {
        const auto candidate = cur / "SDT" / "benchmarks";
        if (fs::exists(candidate) && fs::is_directory(candidate)) {
            return cur;
        }
        if (!cur.has_parent_path()) break;
        cur = cur.parent_path();
    }
    return std::nullopt;
}

struct Report {
    std::string benchmark_id;
    std::string title;
    std::string status; // CERTIFIED | UNDER_INVESTIGATION | DRAFT

    std::vector<std::string> data_sources;
    std::vector<std::string> data_files;
    std::vector<std::string> constants_used;

    std::vector<std::string> equations;
    std::vector<std::string> pipeline;

    int total_tested = 0;
    int within_tolerance = 0;
    double max_error_percent = 0.0;
    double mean_error_percent = 0.0;
    double r_squared = 0.0;

    std::string metric;
    std::string tolerance;
    std::string conclusion;
};

std::string report_to_json(const Report& r) {
    auto arr = [](const std::vector<std::string>& xs) {
        std::ostringstream o;
        o << "[";
        for (std::size_t i = 0; i < xs.size(); ++i) {
            if (i) o << ", ";
            o << "\"" << json_escape(xs[i]) << "\"";
        }
        o << "]";
        return o.str();
    };

    std::ostringstream o;
    o << "{\n";
    o << "  \"benchmark_id\": \"" << json_escape(r.benchmark_id) << "\",\n";
    o << "  \"title\": \"" << json_escape(r.title) << "\",\n";
    o << "  \"status\": \"" << json_escape(r.status) << "\",\n";
    o << "  \"validation_date\": \"" << json_escape(now_iso8601()) << "\",\n";
    o << "  \"inputs\": {\n";
    o << "    \"data_sources\": " << arr(r.data_sources) << ",\n";
    o << "    \"data_files\": " << arr(r.data_files) << ",\n";
    o << "    \"constants\": " << arr(r.constants_used) << "\n";
    o << "  },\n";
    o << "  \"methods\": {\n";
    o << "    \"equations\": " << arr(r.equations) << ",\n";
    o << "    \"pipeline\": " << arr(r.pipeline) << "\n";
    o << "  },\n";
    o << "  \"results\": {\n";
    o << "    \"total_tested\": " << r.total_tested << ",\n";
    o << "    \"within_tolerance\": " << r.within_tolerance << ",\n";
    o << "    \"max_error_percent\": " << std::setprecision(10) << r.max_error_percent << ",\n";
    o << "    \"mean_error_percent\": " << std::setprecision(10) << r.mean_error_percent << ",\n";
    o << "    \"r_squared\": " << std::setprecision(10) << r.r_squared << "\n";
    o << "  },\n";
    o << "  \"comparison\": {\n";
    o << "    \"metric\": \"" << json_escape(r.metric) << "\",\n";
    o << "    \"tolerance\": \"" << json_escape(r.tolerance) << "\"\n";
    o << "  },\n";
    o << "  \"conclusion\": \"" << json_escape(r.conclusion) << "\"\n";
    o << "}\n";
    return o.str();
}

// -----------------------------------------------------------------------------
// Math helpers
// -----------------------------------------------------------------------------
double norm3(const std::array<double, 3>& v) {
    return std::sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2]);
}

double dist3(const std::array<double, 3>& a, const std::array<double, 3>& b) {
    const double dx = a[0] - b[0];
    const double dy = a[1] - b[1];
    const double dz = a[2] - b[2];
    return std::sqrt(dx * dx + dy * dy + dz * dz);
}

// -----------------------------------------------------------------------------
// B25: Alpha-Cluster Geometry Fidelity
// -----------------------------------------------------------------------------
Report run_B25_alpha_cluster_geometry() {
    using sdt::nuclear::packing::AlphaClusterArrangement;
    using sdt::nuclear::packing::AlphaClusterBuilder;
    using sdt::nuclear::occlusion::AlphaGeometry;

    // Treat alpha clusters as spheres with radius comparable to nucleon radius for
    // geometry/occlusion invariants (cluster-center geometry is validated separately).
    const double alpha_radius_fm = sdt::nuclear::occlusion::constants::proton_radius_fm;
    AlphaClusterBuilder builder(alpha_radius_fm);

    const double d_cluster = sdt::nuclear::occlusion::constants::dist_inter_alpha_fm;
    const auto tri = builder.build_triangle(d_cluster);
    const auto tet = builder.build_tetrahedron(d_cluster);
    const auto oct = builder.build_octahedron(d_cluster);

    struct Case {
        const AlphaClusterArrangement* a;
        std::string_view name;
        std::size_t expected_bonds;
        bool require_planar;
    };
    const std::vector<Case> cases = {
        {&tri, tri.name, 3, true},
        {&tet, tet.name, 6, false},
        {&oct, oct.name, 12, false},
    };

    double max_rel_edge_dev = 0.0;
    double max_centroid_norm = 0.0;
    double max_planarity_abs_z = 0.0;
    int total = 0;
    int pass = 0;

    for (const auto& c : cases) {
        ++total;
        const auto& arr = *c.a;
        // centroid
        std::array<double, 3> centroid{0.0, 0.0, 0.0};
        for (const auto& node : arr.nodes) {
            centroid[0] += node.position_fm[0];
            centroid[1] += node.position_fm[1];
            centroid[2] += node.position_fm[2];
            if (c.require_planar) {
                max_planarity_abs_z = std::max(max_planarity_abs_z, std::abs(node.position_fm[2]));
            }
        }
        centroid[0] /= static_cast<double>(arr.nodes.size());
        centroid[1] /= static_cast<double>(arr.nodes.size());
        centroid[2] /= static_cast<double>(arr.nodes.size());
        const double centroid_n = norm3(centroid);
        max_centroid_norm = std::max(max_centroid_norm, centroid_n);

        // bond count
        const bool bond_count_ok = (arr.bonds.size() == c.expected_bonds);

        // edge-length deviation across listed bonds
        double local_max_dev = 0.0;
        for (const auto& bond : arr.bonds) {
            const auto& pa = arr.nodes[bond.a].position_fm;
            const auto& pb = arr.nodes[bond.b].position_fm;
            const double d_actual = dist3(pa, pb);
            const double d_expected = bond.separation_fm;
            const double rel = (d_expected > 0.0) ? std::abs(d_actual - d_expected) / d_expected : 0.0;
            local_max_dev = std::max(local_max_dev, rel);
        }
        max_rel_edge_dev = std::max(max_rel_edge_dev, local_max_dev);

        // Pass criteria per prompt
        const double d = d_cluster;
        const bool edge_ok = local_max_dev <= 1e-9;
        const bool centroid_ok = centroid_n <= (1e-12 * d);
        const bool planar_ok = !c.require_planar || (max_planarity_abs_z <= 1e-12 * d);
        const bool ok = bond_count_ok && edge_ok && centroid_ok && planar_ok;
        if (ok) ++pass;
    }

    Report r;
    r.benchmark_id = "B25";
    r.title = "Alpha-Cluster Geometry Fidelity";
    r.data_sources = {"Internal geometry invariants (no external data)"};
    r.constants_used = {
        "sdt::nuclear::occlusion::constants::dist_inter_alpha_fm",
        "sdt::nuclear::occlusion::constants::proton_radius_fm"
    };
    r.equations = {
        "Edge deviation = max(|d_actual - d_expected| / d_expected)",
        "Centroid norm = ||mean(position_i)||"
    };
    r.pipeline = {
        "Build triangle/tetrahedron/octahedron arrangements",
        "Compute bond distances and centroid",
        "Check invariants vs strict thresholds"
    };
    r.metric = "max relative edge deviation; centroid norm";
    r.tolerance = "edge ≤ 1e-9; centroid ≤ 1e-12·d";
    r.total_tested = total;
    r.within_tolerance = pass;
    r.max_error_percent = 100.0 * max_rel_edge_dev;
    r.mean_error_percent = 100.0 * max_rel_edge_dev; // conservative single metric

    if (pass == total) {
        r.status = "CERTIFIED";
        r.conclusion = "All alpha-cluster geometric invariants satisfied under strict tolerances.";
    } else {
        r.status = "UNDER_INVESTIGATION";
        std::ostringstream c;
        c << "One or more geometry invariants failed. "
          << "max_rel_edge_dev=" << max_rel_edge_dev
          << ", max_centroid_norm=" << max_centroid_norm
          << ", max_planarity_abs_z=" << max_planarity_abs_z;
        r.conclusion = c.str();
    }

    return r;
}

// -----------------------------------------------------------------------------
// B26: Inter-Alpha Occlusion Overlap Correction
// -----------------------------------------------------------------------------
Report run_B26_inter_alpha_overlap() {
    using sdt::nuclear::packing::AlphaClusterBuilder;
    using sdt::nuclear::packing::OcclusionSphere;
    using sdt::nuclear::packing::occlusion_solid_angle_sampled;
    using sdt::nuclear::occlusion::AlphaGeometry;
    using sdt::nuclear::occlusion::math::spherical_occlusion;

    const double alpha_radius_fm = sdt::nuclear::occlusion::constants::proton_radius_fm;
    AlphaClusterBuilder builder(alpha_radius_fm);

    const double d_cluster = sdt::nuclear::occlusion::constants::dist_inter_alpha_fm;
    const auto arrangement = builder.build_tetrahedron(d_cluster);

    // We interpret this benchmark as:
    // - Analytic: sum of pairwise occlusion solid angles (no overlap correction)
    // - Sampled: overlap-corrected union occlusion (per node), using ray sampling
    //
    // That is, for each alpha, sample the sky of directions and measure how much
    // is blocked by *any* neighbor alpha; then sum across nodes.
    double analytic_sum = 0.0;

    auto sampled_sum_for = [&](std::size_t samples) {
        double sampled_total = 0.0;
        for (std::size_t i = 0; i < arrangement.nodes.size(); ++i) {
            const auto observer = arrangement.nodes[i].position_fm;

            std::vector<OcclusionSphere> spheres;
            spheres.reserve(arrangement.nodes.size() - 1);
            for (std::size_t j = 0; j < arrangement.nodes.size(); ++j) {
                if (j == i) continue;
                spheres.push_back({arrangement.nodes[j].position_fm, arrangement.alpha_radius_fm});

                const double d = dist3(observer, arrangement.nodes[j].position_fm);
                analytic_sum += spherical_occlusion(arrangement.alpha_radius_fm, d);
            }

            sampled_total += occlusion_solid_angle_sampled(spheres, observer, samples);
        }
        return sampled_total;
    };

    const double sampled_2k = sampled_sum_for(2000);
    // analytic_sum accumulated during sampled_sum_for(2000); reuse for 10k without double-counting
    const double analytic_baseline = analytic_sum;

    auto rel_diff_from = [&](double sampled) {
        const double denom = (analytic_baseline == 0.0) ? 1.0 : analytic_baseline;
        return std::abs(sampled - analytic_baseline) / denom;
    };

    const double diff_2k = rel_diff_from(sampled_2k);

    // Compute 10k sampled with the same analytic baseline
    double sampled_10k = 0.0;
    for (std::size_t i = 0; i < arrangement.nodes.size(); ++i) {
        const auto observer = arrangement.nodes[i].position_fm;
        std::vector<OcclusionSphere> spheres;
        spheres.reserve(arrangement.nodes.size() - 1);
        for (std::size_t j = 0; j < arrangement.nodes.size(); ++j) {
            if (j == i) continue;
            spheres.push_back({arrangement.nodes[j].position_fm, arrangement.alpha_radius_fm});
        }
        sampled_10k += occlusion_solid_angle_sampled(spheres, observer, 10000);
    }
    const double diff_10k = rel_diff_from(sampled_10k);

    const bool pass_2k = diff_2k <= 0.10;
    const bool pass_10k = diff_10k <= 0.05;

    Report r;
    r.benchmark_id = "B26";
    r.title = "Inter-Alpha Occlusion Overlap Correction";
    r.data_sources = {"Internal occlusion sampling (no external data)"};
    r.constants_used = {
        "sdt::nuclear::packing::occlusion_solid_angle_sampled",
        "sdt::nuclear::occlusion::math::spherical_occlusion"
    };
    r.equations = {
        "analytic_sum = Σ_i Ω_i (no overlap correction)",
        "sampled = 4π·(occluded_rays / total_rays)",
        "relative_difference = |sampled - analytic_sum| / analytic_sum"
    };
    r.pipeline = {
        "Build alpha-cluster arrangement (tetrahedron)",
        "Compute analytic per-node Σ occlusion(neighbor) without overlap correction",
        "Compute overlap-corrected per-node union occlusion via Fibonacci ray sampling (2k and 10k)"
    };
    r.metric = "relative difference";
    r.tolerance = "≤10% at 2k samples; ≤5% at 10k samples";
    r.total_tested = 2;
    r.within_tolerance = (pass_2k ? 1 : 0) + (pass_10k ? 1 : 0);
    r.max_error_percent = 100.0 * std::max(diff_2k, diff_10k);
    r.mean_error_percent = 100.0 * (diff_2k + diff_10k) / 2.0;

    if (pass_2k && pass_10k) {
        r.status = "CERTIFIED";
        std::ostringstream c;
        c << "Overlap-corrected occlusion converges: rel_diff(2k)=" << diff_2k
          << ", rel_diff(10k)=" << diff_10k;
        r.conclusion = c.str();
    } else {
        r.status = "UNDER_INVESTIGATION";
        std::ostringstream c;
        c << "Overlap-corrected occlusion did not meet thresholds: rel_diff(2k)=" << diff_2k
          << ", rel_diff(10k)=" << diff_10k
          << ". Note: analytic baseline is per-node Σ spherical_occlusion(neighbor), sampled is per-node union occlusion via ray sampling.";
        r.conclusion = c.str();
    }

    return r;
}

// -----------------------------------------------------------------------------
// B34: Binding Energy from Occlusion Constant
// -----------------------------------------------------------------------------
Report run_B34_binding_from_occlusion_constant() {
    using namespace sdt::nuclear::occlusion;

    DeuteronGeometry d;
    AlphaGeometry a;
    Carbon12Geometry c;
    Oxygen16Geometry o;

    struct Case {
        std::string name;
        double pred;
        double exp;
        double tolerance_pct;
    };
    std::vector<Case> cases = {
        {"He-4", a.binding_energy_predicted(), AlphaGeometry::binding_energy_experimental(), 10.0},
        {"C-12", c.binding_energy_predicted(), Carbon12Geometry::binding_energy_experimental(), 15.0},
        {"O-16", o.binding_energy_predicted(), Oxygen16Geometry::binding_energy_experimental(), 15.0},
    };

    double max_err = 0.0;
    double sum_err = 0.0;
    int pass = 0;
    for (const auto& tc : cases) {
        const double err = std::abs(tc.pred - tc.exp) / tc.exp * 100.0;
        max_err = std::max(max_err, err);
        sum_err += err;
        if (err <= tc.tolerance_pct) ++pass;
    }

    Report r;
    r.benchmark_id = "B34";
    r.title = "Binding Energy from Occlusion Constant";
    r.data_sources = {"NIST binding energies for D, He-4, C-12, O-16 (encoded in SDT headers)"};
    r.data_files = {"SDT/Code/sdt_navier_cpp/include/nuclear_geometry_occlusion.hpp"};
    r.constants_used = {
        "sdt::nuclear::occlusion::constants::k_binding_MeV_per_sr",
        "sdt::nuclear::occlusion::constants::dist_deuteron_fm",
        "sdt::nuclear::occlusion::constants::dist_alpha_fm",
        "sdt::nuclear::occlusion::constants::dist_inter_alpha_fm"
    };
    r.equations = {
        "E_bind = Ω_total · k_binding",
        "Ω_sphere(d) = 2π(1 - cosθ), sinθ=R/d"
    };
    r.pipeline = {
        "Use deuteron-calibrated k_binding",
        "Compute occlusion-based binding energies for He-4, C-12, O-16",
        "Compare to embedded experimental references"
    };
    r.metric = "percent error";
    r.tolerance = "He-4 ≤ 10%; C-12/O-16 ≤ 15%";
    r.total_tested = static_cast<int>(cases.size());
    r.within_tolerance = pass;
    r.max_error_percent = max_err;
    r.mean_error_percent = sum_err / static_cast<double>(cases.size());
    r.r_squared = 0.0;

    if (pass == static_cast<int>(cases.size())) {
        r.status = "CERTIFIED";
        r.conclusion = "Occlusion constant calibrated on deuteron yields acceptable light-nuclei binding energies within stated tolerances.";
    } else {
        r.status = "UNDER_INVESTIGATION";
        std::ostringstream cmt;
        cmt << "One or more light-nuclei binding energies exceeded tolerance. max_error_pct=" << max_err
            << ". Consider revising effective alpha radius or inter-alpha overlap correction.";
        r.conclusion = cmt.str();
    }
    return r;
}

// -----------------------------------------------------------------------------
// B41: Spation Field Initialization Consistency
// -----------------------------------------------------------------------------
Report run_B41_spation_field_initialization_consistency() {
    using namespace sdt_navier;

    // Baseline hydrogen reference
    const double P_H = compute_p_infinity_hydrogen();

    // Monotonic tests: vary each parameter while holding others constant
    struct Test {
        std::string name;
        double a;
        double b;
        bool expect_increasing;
    };

    // compute_p_infinity ∝ n_e * rho_n / r_n^2 (with alpha fixed)
    const double n0 = sdt_navier::sdt::N_E_HYDROGEN;
    const double rho0 = sdt_navier::sdt::RHO_N;
    const double r0 = sdt_navier::sdt::R_P;

    std::vector<Test> tests = {
        {"n_e: 0.5x→2x", compute_p_infinity(0.5 * n0, rho0, r0), compute_p_infinity(2.0 * n0, rho0, r0), true},
        {"rho_n: 0.5x→2x", compute_p_infinity(n0, 0.5 * rho0, r0), compute_p_infinity(n0, 2.0 * rho0, r0), true},
        {"r_n: 2x→0.5x", compute_p_infinity(n0, rho0, 2.0 * r0), compute_p_infinity(n0, rho0, 0.5 * r0), true}, // smaller r_n => larger P
    };

    int total = static_cast<int>(tests.size());
    int pass = 0;
    double max_err_pct = 0.0;

    // Also check positivity and hydrogen consistency
    const bool positive = (P_H > 0.0);
    if (!positive) {
        max_err_pct = 100.0;
    }

    for (const auto& t : tests) {
        const bool mono = t.expect_increasing ? (t.b > t.a) : (t.b < t.a);
        if (mono) ++pass;
    }

    Report r;
    r.benchmark_id = "B41";
    r.title = "Spation Field Initialization Consistency";
    r.data_sources = {"Internal formula monotonicity checks"};
    r.constants_used = {
        "sdt_navier::compute_p_infinity",
        "sdt_navier::compute_p_infinity_hydrogen",
        "sdt_navier::sdt::N_E_HYDROGEN",
        "sdt_navier::sdt::RHO_N",
        "sdt_navier::sdt::R_P",
        "sdt_navier::sdt::ALPHA"
    };
    r.equations = {
        "P_infinity = (ħ² n_e ρ_n) / (2 m_e r_n² α²)"
    };
    r.pipeline = {
        "Compute P_infinity for hydrogen reference",
        "Vary (n_e, ρ_n, r_n) independently and check monotonic behavior",
        "Check P_infinity > 0"
    };
    r.metric = "monotonic checks pass/fail";
    r.tolerance = "all monotonic checks pass; P_infinity > 0";
    r.total_tested = total + 1;
    r.within_tolerance = pass + (positive ? 1 : 0);
    r.max_error_percent = max_err_pct;
    r.mean_error_percent = max_err_pct;

    if (pass == total && positive) {
        r.status = "CERTIFIED";
        std::ostringstream c;
        c << "P_infinity monotonicity holds; P_H=" << P_H;
        r.conclusion = c.str();
    } else {
        r.status = "UNDER_INVESTIGATION";
        std::ostringstream c;
        c << "Monotonicity/positivity failure: pass=" << pass << "/" << total
          << ", P_H=" << P_H;
        r.conclusion = c.str();
    }

    return r;
}

// -----------------------------------------------------------------------------
// B42: Turbine Cell Consistency Test
// -----------------------------------------------------------------------------
Report run_B42_turbine_cell_consistency() {
    using namespace sdt_navier;

    FieldSystem fields(21, 21, 21, 1.0, 1.0, 1.0);
    initialize_fields(fields, sdt_navier::sdt::P_INFINITY_NUCLEAR, 0.0, 0.01, sdt_navier::sdt::GAMMA_P);

    const std::array<std::size_t, 3> center{10, 10, 10};

    // Inject gaussian and step profiles
    add_turbine_source(fields, center, 4.0, /*kappa*/ 1.0, /*Gamma*/ 1.0, /*eta*/ 0.25, "gaussian");
    add_turbine_source(fields, center, 3.0, /*kappa*/ 0.5, /*Gamma*/ 0.8, /*eta*/ 0.50, "step");

    auto eta = fields.eta();
    auto Gamma = fields.Gamma();

    int violations = 0;
    for (std::size_t i = 0; i < fields.size(); ++i) {
        if (!(eta[i] >= 0.0 && eta[i] <= 1.0)) ++violations;
        if (!(Gamma[i] >= 0.0)) ++violations;
    }

    Report r;
    r.benchmark_id = "B42";
    r.title = "Turbine Cell Consistency Test";
    r.data_sources = {"Internal field constraints (no external data)"};
    r.constants_used = {
        "sdt_navier::FieldSystem",
        "sdt_navier::initialize_fields",
        "sdt_navier::add_turbine_source"
    };
    r.equations = {
        "σ = Γ κ (1-η) (diversion density constraint input)",
        "Constraints: η∈[0,1], Γ≥0"
    };
    r.pipeline = {
        "Initialize FieldSystem with defaults",
        "Inject turbine sources using gaussian and step profiles",
        "Scan fields for constraint violations"
    };
    r.metric = "constraint violations";
    r.tolerance = "0 violations";
    r.total_tested = 1;
    r.within_tolerance = (violations == 0) ? 1 : 0;
    r.max_error_percent = (violations == 0) ? 0.0 : 100.0;
    r.mean_error_percent = r.max_error_percent;
    r.r_squared = 0.0;

    if (violations == 0) {
        r.status = "CERTIFIED";
        r.conclusion = "No η or Γ constraint violations after turbine injection.";
    } else {
        r.status = "UNDER_INVESTIGATION";
        r.conclusion = "Found constraint violations: " + std::to_string(violations);
    }
    return r;
}

// -----------------------------------------------------------------------------
// Generic placeholder (for not-yet-implemented B27..B33, B35..B40, B43..B50)
// -----------------------------------------------------------------------------
Report placeholder(std::string id, std::string title, std::string next_steps) {
    Report r;
    r.benchmark_id = std::move(id);
    r.title = std::move(title);
    r.status = "DRAFT";
    r.data_sources = {"TBD"};
    r.data_files = {};
    r.constants_used = {};
    r.equations = {};
    r.pipeline = {"Not implemented yet"};
    r.metric = "TBD";
    r.tolerance = "TBD";
    r.total_tested = 0;
    r.within_tolerance = 0;
    r.max_error_percent = 0.0;
    r.mean_error_percent = 0.0;
    r.r_squared = 0.0;
    r.conclusion = std::move(next_steps);
    return r;
}

std::vector<Report> run_all() {
    std::vector<Report> out;
    out.reserve(25);

    out.push_back(run_B25_alpha_cluster_geometry());
    out.push_back(run_B26_inter_alpha_overlap());

    out.push_back(placeholder("B27", "Nuclear Radius Scaling (Packing → Radius)",
                              "Missing: curated ENSDF charge radius dataset + SDT packing-radius model mapping."));
    out.push_back(placeholder("B28", "Z_eff (Valence) from Occlusion Geometry",
                              "Missing: explicit Xi_val→Z_eff formula + Slater/NIST baseline dataset. Candidate: use AtomicCalculator screening + curated reference Z_eff."));
    out.push_back(placeholder("B29", "First Ionization Energy from SDT Pressure",
                              "Missing: NIST I1 dataset (Z=1–36) + explicit SDT I1 formula implementation (currently only screening is implemented)."));
    out.push_back(placeholder("B30", "Electron Affinity Trend Consistency",
                              "Missing: NIST electron affinity dataset + SDT trend-sign predictor implementation."));
    out.push_back(placeholder("B31", "Atomic Radius Canonical Definition",
                              "Missing: single-type NIST radius dataset + SDT radius definition mapping."));
    out.push_back(placeholder("B32", "Shell Closure Prediction from Packing",
                              "Missing: packing layer capacities formalization + closure prediction code; compare to He/Ne/Ar/Kr/Xe/Rn."));
    out.push_back(placeholder("B33", "Isotope Shift from Neutron Overload (T=N−Z)",
                              "Missing: ENSDF isotopic series dataset + SDT isotope-shift predictor."));

    out.push_back(run_B34_binding_from_occlusion_constant());

    out.push_back(placeholder("B35", "Spin/Parity Proxy via Packing Symmetry",
                              "Missing: ground-state spin/parity dataset + symmetry classifier mapping to parity prediction."));
    out.push_back(placeholder("B36", "Quadrupole Moments from Packing Geometry",
                              "Missing: quadrupole moment dataset + tensor-from-cluster-position estimator + normalization rule."));
    out.push_back(placeholder("B37", "Screening Factor Geometry (B21 Extension)",
                              "Missing: heavy-element screening trend dataset (Z>20) + overlap-corrected Xi implementation."));
    out.push_back(placeholder("B38", "Multi-Electron Occlusion (B24 Extension)",
                              "Missing: NIST I1 for Z=21–54 + multi-electron occlusion model beyond Slater-like screening."));
    out.push_back(placeholder("B39", "Nuclear Charge Radius vs Packing Saturation",
                              "Missing: charge radii dataset + saturation slope-change detector."));
    out.push_back(placeholder("B40", "Nuclear Surface Pressure Coupling",
                              "Missing: nuclear surface pressure definition + scaling exponent validation dataset."));

    out.push_back(run_B41_spation_field_initialization_consistency());
    out.push_back(run_B42_turbine_cell_consistency());

    out.push_back(placeholder("B43", "Occlusion Transmission vs Ionization",
                              "Missing: Xi_ion definition in C++ + NIST I1 dataset + correlation calculation."));
    out.push_back(placeholder("B44", "Periodic Table Emergence from Packing",
                              "Missing: packing→group assignment rule + ground-truth group table for Z=1–36."));
    out.push_back(placeholder("B45", "CMB Pressure Scaling Across Elements",
                              "Missing: P_infinity per element definition + expected scaling law + correlation test implementation."));
    out.push_back(placeholder("B46", "Metallic vs Non-Metallic Boundary Prediction",
                              "Missing: classification rule + ground-truth metal/nonmetal table for Z=1–36."));
    out.push_back(placeholder("B47", "Phase-Velocity Constraint Consistency",
                              "Missing: extract explicit phase-velocity constraints from SDT docs + implement checks."));
    out.push_back(placeholder("B48", "Nuclear Packing Pathway Enumeration",
                              "Missing: packing transition rule-set + stable isotope list + alignment scoring."));
    out.push_back(placeholder("B49", "Energetic Stability Map",
                              "Missing: binding-energy predictor across Z=1–30 + stability ground truth + map scoring."));
    out.push_back(placeholder("B50", "End-to-End SDT Prediction Pass",
                              "Missing: end-to-end atomic prediction pipeline (r_atom, Z_eff, I1, radius) + NIST evaluation datasets."));

    return out;
}

} // namespace

int main(int argc, char** argv) {
    try {
        const auto repo_root_opt = find_repo_root_from(fs::current_path());
        if (!repo_root_opt) {
            std::cerr << "Error: Could not locate repo root (expected to find SDT/benchmarks in parent paths).\n";
            return 2;
        }
        const fs::path repo_root = *repo_root_opt;
        const fs::path benchmarks_dir = repo_root / "SDT" / "benchmarks";
        const fs::path data_dir = benchmarks_dir / "data";
        ensure_dir(data_dir);

        std::optional<std::string> only;
        for (int i = 1; i < argc; ++i) {
            std::string arg = argv[i];
            if ((arg == "--benchmark" || arg == "-b") && i + 1 < argc) {
                only = argv[++i];
            } else if (arg == "--all") {
                only.reset();
            }
        }

        const auto reports = run_all();
        int written = 0;
        for (const auto& rep : reports) {
            if (only && rep.benchmark_id != *only) continue;
            const fs::path out_json = benchmarks_dir / (rep.benchmark_id + "_validation_report.json");
            write_text(out_json, report_to_json(rep));
            ++written;
        }

        std::cout << "Wrote " << written << " validation report(s) to " << benchmarks_dir.string() << "\n";
        return 0;
    } catch (const std::exception& e) {
        std::cerr << "Fatal error: " << e.what() << "\n";
        return 1;
    }
}

