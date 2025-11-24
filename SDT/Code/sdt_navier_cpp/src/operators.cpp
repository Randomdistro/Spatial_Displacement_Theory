#include "sdt_navier/operators.hpp"
#include "sdt_navier/fields.hpp"
#include <algorithm>
#include <cmath>
#include <string>

namespace sdt_navier {

std::vector<std::array<double, 3>> compute_gradient(
    const std::vector<double>& field,
    const FieldSystem& fields,
    const std::string& boundary
) {
    std::vector<std::array<double, 3>> grad(fields.size(), {0.0, 0.0, 0.0});

    for (std::size_t k = 0; k < fields.nz(); ++k) {
        for (std::size_t j = 0; j < fields.ny(); ++j) {
            for (std::size_t i = 0; i < fields.nx(); ++i) {
                std::size_t idx = fields.index(i, j, k);

                // x-component
                if (i > 0 && i < fields.nx() - 1) {
                    std::size_t idx_p = fields.index(i + 1, j, k);
                    std::size_t idx_m = fields.index(i - 1, j, k);
                    grad[idx][0] = (field[idx_p] - field[idx_m]) / (2.0 * fields.dx());
                } else if (boundary == "extrapolate") {
                    if (i == 0) {
                        std::size_t idx_p = fields.index(i + 1, j, k);
                        grad[idx][0] = (field[idx_p] - field[idx]) / fields.dx();
                    } else {
                        std::size_t idx_m = fields.index(i - 1, j, k);
                        grad[idx][0] = (field[idx] - field[idx_m]) / fields.dx();
                    }
                } else if (boundary == "periodic") {
                    std::size_t i_p = (i + 1) % fields.nx();
                    std::size_t i_m = (i + fields.nx() - 1) % fields.nx();
                    std::size_t idx_p = fields.index(i_p, j, k);
                    std::size_t idx_m = fields.index(i_m, j, k);
                    grad[idx][0] = (field[idx_p] - field[idx_m]) / (2.0 * fields.dx());
                }

                // y-component
                if (j > 0 && j < fields.ny() - 1) {
                    std::size_t idx_p = fields.index(i, j + 1, k);
                    std::size_t idx_m = fields.index(i, j - 1, k);
                    grad[idx][1] = (field[idx_p] - field[idx_m]) / (2.0 * fields.dy());
                } else if (boundary == "extrapolate") {
                    if (j == 0) {
                        std::size_t idx_p = fields.index(i, j + 1, k);
                        grad[idx][1] = (field[idx_p] - field[idx]) / fields.dy();
                    } else if (j == fields.ny() - 1) {
                        std::size_t idx_m = fields.index(i, j - 1, k);
                        grad[idx][1] = (field[idx] - field[idx_m]) / fields.dy();
                    }
                } else if (boundary == "periodic") {
                    std::size_t j_p = (j + 1) % fields.ny();
                    std::size_t j_m = (j + fields.ny() - 1) % fields.ny();
                    std::size_t idx_p = fields.index(i, j_p, k);
                    std::size_t idx_m = fields.index(i, j_m, k);
                    grad[idx][1] = (field[idx_p] - field[idx_m]) / (2.0 * fields.dy());
                }

                // z-component
                if (k > 0 && k < fields.nz() - 1) {
                    std::size_t idx_p = fields.index(i, j, k + 1);
                    std::size_t idx_m = fields.index(i, j, k - 1);
                    grad[idx][2] = (field[idx_p] - field[idx_m]) / (2.0 * fields.dz());
                } else if (boundary == "extrapolate") {
                    if (k == 0) {
                        std::size_t idx_p = fields.index(i, j, k + 1);
                        grad[idx][2] = (field[idx_p] - field[idx]) / fields.dz();
                    } else if (k == fields.nz() - 1) {
                        std::size_t idx_m = fields.index(i, j, k - 1);
                        grad[idx][2] = (field[idx] - field[idx_m]) / fields.dz();
                    }
                } else if (boundary == "periodic") {
                    std::size_t k_p = (k + 1) % fields.nz();
                    std::size_t k_m = (k + fields.nz() - 1) % fields.nz();
                    std::size_t idx_p = fields.index(i, j, k_p);
                    std::size_t idx_m = fields.index(i, j, k_m);
                    grad[idx][2] = (field[idx_p] - field[idx_m]) / (2.0 * fields.dz());
                }
            }
        }
    }

    return grad;
}

std::vector<double> compute_divergence(
    const std::vector<FieldSystem::Vector3d>& v,
    const FieldSystem& fields,
    const std::string& boundary
) {
    std::vector<double> div(fields.size(), 0.0);

    for (std::size_t k = 0; k < fields.nz(); ++k) {
        for (std::size_t j = 0; j < fields.ny(); ++j) {
            for (std::size_t i = 0; i < fields.nx(); ++i) {
                std::size_t idx = fields.index(i, j, k);

                // ∂v_x/∂x
                if (i > 0 && i < fields.nx() - 1) {
                    std::size_t idx_p = fields.index(i + 1, j, k);
                    std::size_t idx_m = fields.index(i - 1, j, k);
                    div[idx] += (v[idx_p][0] - v[idx_m][0]) / (2.0 * fields.dx());
                } else if (boundary == "extrapolate") {
                    if (i == 0) {
                        std::size_t idx_p = fields.index(i + 1, j, k);
                        div[idx] += (v[idx_p][0] - v[idx][0]) / fields.dx();
                    } else if (i == fields.nx() - 1) {
                        std::size_t idx_m = fields.index(i - 1, j, k);
                        div[idx] += (v[idx][0] - v[idx_m][0]) / fields.dx();
                    }
                }

                // ∂v_y/∂y
                if (j > 0 && j < fields.ny() - 1) {
                    std::size_t idx_p = fields.index(i, j + 1, k);
                    std::size_t idx_m = fields.index(i, j - 1, k);
                    div[idx] += (v[idx_p][1] - v[idx_m][1]) / (2.0 * fields.dy());
                } else if (boundary == "extrapolate") {
                    if (j == 0) {
                        std::size_t idx_p = fields.index(i, j + 1, k);
                        div[idx] += (v[idx_p][1] - v[idx][1]) / fields.dy();
                    } else if (j == fields.ny() - 1) {
                        std::size_t idx_m = fields.index(i, j - 1, k);
                        div[idx] += (v[idx][1] - v[idx_m][1]) / fields.dy();
                    }
                }

                // ∂v_z/∂z
                if (k > 0 && k < fields.nz() - 1) {
                    std::size_t idx_p = fields.index(i, j, k + 1);
                    std::size_t idx_m = fields.index(i, j, k - 1);
                    div[idx] += (v[idx_p][2] - v[idx_m][2]) / (2.0 * fields.dz());
                } else if (boundary == "extrapolate") {
                    if (k == 0) {
                        std::size_t idx_p = fields.index(i, j, k + 1);
                        div[idx] += (v[idx_p][2] - v[idx][2]) / fields.dz();
                    } else if (k == fields.nz() - 1) {
                        std::size_t idx_m = fields.index(i, j, k - 1);
                        div[idx] += (v[idx][2] - v[idx_m][2]) / fields.dz();
                    }
                }
            }
        }
    }

    return div;
}

std::vector<std::array<std::array<double, 3>, 3>> compute_velocity_gradient(
    const std::vector<FieldSystem::Vector3d>& v,
    const FieldSystem& fields,
    const std::string& boundary
) {
    std::vector<std::array<std::array<double, 3>, 3>> grad_v(fields.size());

    for (std::size_t a = 0; a < 3; ++a) {
        std::vector<double> v_component(fields.size());
        for (std::size_t i = 0; i < fields.size(); ++i) {
            v_component[i] = v[i][a];
        }

        auto grad_component = compute_gradient(v_component, fields, boundary);

        for (std::size_t i = 0; i < fields.size(); ++i) {
            for (std::size_t b = 0; b < 3; ++b) {
                grad_v[i][a][b] = grad_component[i][b];
            }
        }
    }

    return grad_v;
}

std::vector<double> compute_advection(
    const std::vector<double>& field,
    const std::vector<FieldSystem::Vector3d>& v,
    const FieldSystem& fields,
    const std::string& method
) {
    std::vector<double> adv(fields.size(), 0.0);

    if (method == "upwind") {
        // Upwind differencing
        for (std::size_t k = 0; k < fields.nz(); ++k) {
            for (std::size_t j = 0; j < fields.ny(); ++j) {
                for (std::size_t i = 0; i < fields.nx(); ++i) {
                    std::size_t idx = fields.index(i, j, k);

                    // x-direction
                    if (i > 0 && i < fields.nx() - 1) {
                        std::size_t idx_p = fields.index(i + 1, j, k);
                        std::size_t idx_m = fields.index(i - 1, j, k);
                        double backward = (field[idx] - field[idx_m]) / fields.dx();
                        double forward = (field[idx_p] - field[idx]) / fields.dx();
                        adv[idx] += (v[idx][0] > 0 ? backward : forward) * v[idx][0];
                    }

                    // y-direction
                    if (j > 0 && j < fields.ny() - 1) {
                        std::size_t idx_p = fields.index(i, j + 1, k);
                        std::size_t idx_m = fields.index(i, j - 1, k);
                        double backward = (field[idx] - field[idx_m]) / fields.dy();
                        double forward = (field[idx_p] - field[idx]) / fields.dy();
                        adv[idx] += (v[idx][1] > 0 ? backward : forward) * v[idx][1];
                    }

                    // z-direction
                    if (k > 0 && k < fields.nz() - 1) {
                        std::size_t idx_p = fields.index(i, j, k + 1);
                        std::size_t idx_m = fields.index(i, j, k - 1);
                        double backward = (field[idx] - field[idx_m]) / fields.dz();
                        double forward = (field[idx_p] - field[idx]) / fields.dz();
                        adv[idx] += (v[idx][2] > 0 ? backward : forward) * v[idx][2];
                    }
                }
            }
        }
    } else if (method == "central") {
        auto grad = compute_gradient(field, fields, "extrapolate");
        for (std::size_t i = 0; i < fields.size(); ++i) {
            adv[i] = v[i][0] * grad[i][0] + v[i][1] * grad[i][1] + v[i][2] * grad[i][2];
        }
    }

    return adv;
}

}  // namespace sdt_navier

