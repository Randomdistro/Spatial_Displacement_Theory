#include "sdt_navier/io.hpp"
#include <fstream>
#include <iomanip>
#include <sstream>

namespace sdt_navier {

void save_fields_csv(
    const FieldSystem& fields,
    const std::string& filename
) {
    std::ofstream file(filename);
    file << std::scientific << std::setprecision(6);

    // Header
    file << "i,j,k,P,kappa,eta,e,Gamma,vx,vy,vz\n";

    // Data
    for (std::size_t k = 0; k < fields.nz(); ++k) {
        for (std::size_t j = 0; j < fields.ny(); ++j) {
            for (std::size_t i = 0; i < fields.nx(); ++i) {
                std::size_t idx = fields.index(i, j, k);
                auto P = fields.P();
                auto kappa = fields.kappa();
                auto eta = fields.eta();
                auto e = fields.e();
                auto Gamma = fields.Gamma();
                const auto& v = fields.v();

                file << i << "," << j << "," << k << ","
                     << P[idx] << "," << kappa[idx] << "," << eta[idx] << ","
                     << e[idx] << "," << Gamma[idx] << ","
                     << v[idx][0] << "," << v[idx][1] << "," << v[idx][2] << "\n";
            }
        }
    }
}

void save_timeseries_csv(
    const std::vector<double>& times,
    const std::vector<double>& values,
    const std::string& filename,
    const std::string& header
) {
    std::ofstream file(filename);
    file << std::scientific << std::setprecision(6);
    file << header << "\n";

    for (std::size_t i = 0; i < times.size() && i < values.size(); ++i) {
        file << times[i] << "," << values[i] << "\n";
    }
}

void save_results_json(
    const std::string& filename,
    double binding_energy_mev,
    double magnetic_moment,
    double experimental_binding_energy,
    double experimental_magnetic_moment
) {
    std::ofstream file(filename);
    file << std::scientific << std::setprecision(6);

    file << "{\n";
    file << "  \"binding_energy\": {\n";
    file << "    \"computed\": " << binding_energy_mev << ",\n";
    file << "    \"experimental\": " << experimental_binding_energy << ",\n";
    file << "    \"error\": " << (binding_energy_mev - experimental_binding_energy) << ",\n";
    file << "    \"relative_error_percent\": " 
         << ((binding_energy_mev - experimental_binding_energy) / experimental_binding_energy * 100.0) << "\n";
    file << "  },\n";
    file << "  \"magnetic_moment\": {\n";
    file << "    \"computed\": " << magnetic_moment << ",\n";
    file << "    \"experimental\": " << experimental_magnetic_moment << ",\n";
    file << "    \"error\": " << (magnetic_moment - experimental_magnetic_moment) << ",\n";
    file << "    \"relative_error_percent\": "
         << ((magnetic_moment - experimental_magnetic_moment) / experimental_magnetic_moment * 100.0) << "\n";
    file << "  }\n";
    file << "}\n";
}

}  // namespace sdt_navier

