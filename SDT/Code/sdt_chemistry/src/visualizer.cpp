#include "sdt/chemistry/visualizer.hpp"
#include "sdt/chemistry/constants.hpp"
#include <fstream>
#include <sstream>
#include <cmath>
#include <algorithm>
#include <iomanip>
#include <numbers>

namespace sdt::chemistry {

    Color CPKColors::get_color(int element_Z) {
        // CPK color scheme (standard molecular visualization)
        // Colors in RGB [0, 1] range
        switch (element_Z) {
            case 1:  // H - White
                return {1.0f, 1.0f, 1.0f};
            case 2:  // He - Cyan
                return {0.85f, 1.0f, 1.0f};
            case 3:  // Li - Crimson
                return {0.8f, 0.5f, 1.0f};
            case 4:  // Be - Dark green
                return {0.76f, 1.0f, 0.0f};
            case 5:  // B - Salmon
                return {1.0f, 0.71f, 0.71f};
            case 6:  // C - Black/Gray
                return {0.2f, 0.2f, 0.2f};
            case 7:  // N - Blue
                return {0.19f, 0.31f, 0.97f};
            case 8:  // O - Red
                return {1.0f, 0.05f, 0.05f};
            case 9:  // F - Green
                return {0.56f, 0.88f, 0.31f};
            case 10: // Ne - Cyan
                return {0.7f, 0.89f, 0.96f};
            case 11: // Na - Blue
                return {0.67f, 0.36f, 0.95f};
            case 12: // Mg - Dark green
                return {0.54f, 1.0f, 0.0f};
            case 13: // Al - Gray
                return {0.75f, 0.65f, 0.65f};
            case 14: // Si - Golden
                return {0.94f, 0.78f, 0.63f};
            case 15: // P - Orange
                return {1.0f, 0.5f, 0.0f};
            case 16: // S - Yellow
                return {1.0f, 1.0f, 0.19f};
            case 17: // Cl - Green
                return {0.12f, 0.94f, 0.12f};
            case 18: // Ar - Cyan
                return {0.5f, 0.82f, 0.89f};
            case 19: // K - Violet
                return {0.56f, 0.25f, 0.83f};
            case 20: // Ca - Dark gray
                return {0.24f, 0.24f, 0.24f};
            default:
                // Default: Gray for unknown elements
                return {0.5f, 0.5f, 0.5f};
        }
    }

    Color CPKColors::get_color(const std::string& symbol) {
        try {
            const ElementData& elem = Elements::get_element(symbol);
            return get_color(elem.Z);
        } catch (...) {
            return {0.5f, 0.5f, 0.5f};  // Gray for unknown
        }
    }

    float CPKColors::get_visual_radius(int element_Z, float scale) {
        // Get atomic radius from element data and scale for visualization
        try {
            const ElementData& elem = Elements::get_element(element_Z);
            // Convert from pm to visualization units (Angstroms)
            float radius_A = elem.atomic_radius_pm / 100.0f;
            return radius_A * scale;
        } catch (...) {
            return 1.0f * scale;  // Default radius
        }
    }

    MolecularVisualization Visualizer::create_stick_ball_model(
        const Molecule& molecule,
        float atom_scale,
        float bond_radius,
        bool use_cpk_colors
    ) {
        MolecularVisualization viz;
        
        // Convert SDT positions (meters) to visualization coordinates (Angstroms)
        constexpr float m_to_A = 1e10f;
        
        // Create atom spheres
        for (size_t i = 0; i < molecule.num_atoms(); ++i) {
            const Atom& atom = molecule.atom(i);
            const ElementData& elem = atom.element_data();
            
            Sphere sphere;
            // Convert position from meters to Angstroms
            sphere.center = (atom.position.cast<float>() * m_to_A);
            
            // Get radius from SDT atomic radius
            float base_radius = elem.atomic_radius_pm / 100.0f;  // pm to Angstrom
            sphere.radius = base_radius * atom_scale;
            
            // Get CPK color
            if (use_cpk_colors) {
                sphere.color = CPKColors::get_color(atom.element_Z);
            } else {
                sphere.color = {0.7f, 0.7f, 0.7f};  // Default gray
            }
            
            viz.atoms.push_back(sphere);
        }
        
        // Create bond cylinders
        for (size_t i = 0; i < molecule.num_bonds(); ++i) {
            const Bond& bond = molecule.bond(i);
            const Atom& atom1 = molecule.atom(bond.atom1_index);
            const Atom& atom2 = molecule.atom(bond.atom2_index);
            
            Cylinder cylinder = create_bond_cylinder(atom1, atom2, bond, bond_radius);
            
            // Color bond based on bond type
            if (use_cpk_colors) {
                // Use average color of bonded atoms, or specific color for bond type
                Color color1 = CPKColors::get_color(atom1.element_Z);
                Color color2 = CPKColors::get_color(atom2.element_Z);
                cylinder.color = {
                    (color1[0] + color2[0]) * 0.5f,
                    (color1[1] + color2[1]) * 0.5f,
                    (color1[2] + color2[2]) * 0.5f
                };
            } else {
                cylinder.color = {0.3f, 0.3f, 0.3f};  // Dark gray for bonds
            }
            
            viz.bonds.push_back(cylinder);
        }
        
        // Calculate bounding box
        if (!viz.atoms.empty()) {
            viz.bounding_box_min = viz.atoms[0].center;
            viz.bounding_box_max = viz.atoms[0].center;
            
            for (const auto& sphere : viz.atoms) {
                for (int i = 0; i < 3; ++i) {
                    viz.bounding_box_min[i] = std::min(viz.bounding_box_min[i], 
                                                       sphere.center[i] - sphere.radius);
                    viz.bounding_box_max[i] = std::max(viz.bounding_box_max[i], 
                                                       sphere.center[i] + sphere.radius);
                }
            }
        }
        
        // Calculate center
        viz.center = (viz.bounding_box_min + viz.bounding_box_max) * 0.5f;
        
        return viz;
    }

    Cylinder Visualizer::create_bond_cylinder(
        const Atom& atom1,
        const Atom& atom2,
        const Bond& bond,
        float bond_radius
    ) {
        Cylinder cylinder;
        
        constexpr float m_to_A = 1e10f;
        
        Vec3f pos1 = atom1.position.cast<float>() * m_to_A;
        Vec3f pos2 = atom2.position.cast<float>() * m_to_A;
        
        // Get atomic radii for visualization
        float r1 = CPKColors::get_visual_radius(atom1.element_Z);
        float r2 = CPKColors::get_visual_radius(atom2.element_Z);
        
        // Calculate bond vector
        Vec3f bond_vec = pos2 - pos1;
        float bond_length = bond_vec.norm();
        
        // Shorten cylinder to avoid overlap with atoms
        Vec3f direction = bond_vec.normalized();
        float shorten1 = r1 * 0.9f;  // Leave 10% overlap for visual connection
        float shorten2 = r2 * 0.9f;
        
        cylinder.start = pos1 + direction * shorten1;
        cylinder.end = pos2 - direction * shorten2;
        cylinder.radius = bond_radius;
        
        return cylinder;
    }

    bool Visualizer::export_to_obj(
        const MolecularVisualization& viz,
        const std::string& filepath
    ) {
        std::ofstream file(filepath);
        if (!file.is_open()) {
            return false;
        }
        
        file << "# OBJ file generated by SDT Chemistry Visualizer\n";
        file << "# Stick-and-ball molecular model\n\n";
        
        int vertex_offset = 1;  // OBJ uses 1-based indexing
        
        // Export atoms (spheres)
        for (size_t i = 0; i < viz.atoms.size(); ++i) {
            const Sphere& sphere = viz.atoms[i];
            
            file << "# Atom " << i << " (sphere)\n";
            file << "v " << std::fixed << std::setprecision(6)
                 << sphere.center.x() << " "
                 << sphere.center.y() << " "
                 << sphere.center.z() << "\n";
            file << "v " << sphere.color[0] << " "
                 << sphere.color[1] << " "
                 << sphere.color[2] << "\n";
            file << "# Radius: " << sphere.radius << "\n\n";
        }
        
        // Export bonds (cylinders)
        for (size_t i = 0; i < viz.bonds.size(); ++i) {
            const Cylinder& cylinder = viz.bonds[i];
            
            file << "# Bond " << i << " (cylinder)\n";
            file << "v " << std::fixed << std::setprecision(6)
                 << cylinder.start.x() << " "
                 << cylinder.start.y() << " "
                 << cylinder.start.z() << "\n";
            file << "v " << cylinder.end.x() << " "
                 << cylinder.end.y() << " "
                 << cylinder.end.z() << "\n";
            file << "v " << cylinder.color[0] << " "
                 << cylinder.color[1] << " "
                 << cylinder.color[2] << "\n";
            file << "# Radius: " << cylinder.radius << "\n\n";
        }
        
        file.close();
        return true;
    }

    bool Visualizer::export_to_ply(
        const MolecularVisualization& viz,
        const std::string& filepath
    ) {
        std::ofstream file(filepath);
        if (!file.is_open()) {
            return false;
        }
        
        // Count vertices and faces
        int num_vertices = 0;
        int num_faces = 0;
        
        // Spheres: generate mesh vertices
        for (const auto& sphere : viz.atoms) {
            std::vector<Vec3f> sphere_verts = generate_sphere_mesh(
                sphere.center, sphere.radius, 16
            );
            num_vertices += sphere_verts.size();
            num_faces += sphere_verts.size() / 3;  // Approximate
        }
        
        // Cylinders: generate mesh vertices
        for (const auto& cylinder : viz.bonds) {
            std::vector<Vec3f> cyl_verts = generate_cylinder_mesh(
                cylinder.start, cylinder.end, cylinder.radius, 8
            );
            num_vertices += cyl_verts.size();
            num_faces += cyl_verts.size() / 3;
        }
        
        // Write PLY header
        file << "ply\n";
        file << "format ascii 1.0\n";
        file << "comment Generated by SDT Chemistry Visualizer\n";
        file << "element vertex " << num_vertices << "\n";
        file << "property float x\n";
        file << "property float y\n";
        file << "property float z\n";
        file << "property uchar red\n";
        file << "property uchar green\n";
        file << "property uchar blue\n";
        file << "element face " << num_faces << "\n";
        file << "property list uchar int vertex_indices\n";
        file << "end_header\n";
        
        // Write vertices (simplified - would need full mesh generation)
        int vertex_idx = 0;
        for (const auto& sphere : viz.atoms) {
            file << std::fixed << std::setprecision(6)
                 << sphere.center.x() << " "
                 << sphere.center.y() << " "
                 << sphere.center.z() << " "
                 << static_cast<int>(sphere.color[0] * 255) << " "
                 << static_cast<int>(sphere.color[1] * 255) << " "
                 << static_cast<int>(sphere.color[2] * 255) << "\n";
            vertex_idx++;
        }
        
        file.close();
        return true;
    }

    bool Visualizer::export_to_pdb(
        const Molecule& molecule,
        const std::string& filepath
    ) {
        std::ofstream file(filepath);
        if (!file.is_open()) {
            return false;
        }
        
        file << "HEADER    MOLECULE GENERATED BY SDT CHEMISTRY VISUALIZER\n";
        file << "TITLE     " << molecule.name() << "\n";
        file << "REMARK   1 SDT-based molecular structure\n";
        file << "REMARK   2 Positions from pressure field geometry\n\n";
        
        constexpr float m_to_A = 1e10f;
        
        // Write atoms (ATOM records)
        int atom_serial = 1;
        for (size_t i = 0; i < molecule.num_atoms(); ++i) {
            const Atom& atom = molecule.atom(i);
            const ElementData& elem = atom.element_data();
            
            Vec3f pos = atom.position.cast<float>() * m_to_A;
            
            file << "ATOM  " << std::setw(5) << atom_serial
                 << "  " << std::setw(4) << elem.symbol.substr(0, 2)
                 << " MOL A" << std::setw(4) << 1
                 << "    "
                 << std::fixed << std::setprecision(3)
                 << std::setw(8) << pos.x()
                 << std::setw(8) << pos.y()
                 << std::setw(8) << pos.z()
                 << "  1.00  0.00          " << elem.symbol << "\n";
            
            atom_serial++;
        }
        
        // Write bonds (CONECT records)
        for (size_t i = 0; i < molecule.num_bonds(); ++i) {
            const Bond& bond = molecule.bond(i);
            file << "CONECT" << std::setw(5) << (bond.atom1_index + 1)
                 << std::setw(5) << (bond.atom2_index + 1) << "\n";
        }
        
        file << "END\n";
        file.close();
        return true;
    }

    bool Visualizer::export_to_xyz(
        const Molecule& molecule,
        const std::string& filepath
    ) {
        std::ofstream file(filepath);
        if (!file.is_open()) {
            return false;
        }
        
        constexpr float m_to_A = 1e10f;
        
        // Write header
        file << molecule.num_atoms() << "\n";
        file << molecule.name() << " - SDT Chemistry\n";
        
        // Write atoms
        for (size_t i = 0; i < molecule.num_atoms(); ++i) {
            const Atom& atom = molecule.atom(i);
            const ElementData& elem = atom.element_data();
            
            Vec3f pos = atom.position.cast<float>() * m_to_A;
            
            file << elem.symbol << " "
                 << std::fixed << std::setprecision(6)
                 << pos.x() << " "
                 << pos.y() << " "
                 << pos.z() << "\n";
        }
        
        file.close();
        return true;
    }

    bool Visualizer::export_to_pov(
        const MolecularVisualization& viz,
        const std::string& filepath
    ) {
        std::ofstream file(filepath);
        if (!file.is_open()) {
            return false;
        }
        
        file << "// POV-Ray scene generated by SDT Chemistry Visualizer\n";
        file << "#include \"colors.inc\"\n\n";
        file << "camera {\n";
        file << "  location <" << viz.center.x() << ", " << viz.center.y() 
             << ", " << (viz.center.z() + 50.0f) << ">\n";
        file << "  look_at <" << viz.center.x() << ", " << viz.center.y() 
             << ", " << viz.center.z() << ">\n";
        file << "  angle 45\n";
        file << "}\n\n";
        file << "light_source { <0, 0, 100> color White }\n\n";
        
        // Export atoms as spheres
        for (const auto& sphere : viz.atoms) {
            file << "sphere {\n";
            file << "  <" << sphere.center.x() << ", " 
                 << sphere.center.y() << ", " << sphere.center.z() << ">, "
                 << sphere.radius << "\n";
            file << "  pigment { color rgb <" 
                 << sphere.color[0] << ", " 
                 << sphere.color[1] << ", " 
                 << sphere.color[2] << "> }\n";
            file << "  finish { phong 0.8 }\n";
            file << "}\n\n";
        }
        
        // Export bonds as cylinders
        for (const auto& cylinder : viz.bonds) {
            file << "cylinder {\n";
            file << "  <" << cylinder.start.x() << ", " 
                 << cylinder.start.y() << ", " << cylinder.start.z() << ">,\n";
            file << "  <" << cylinder.end.x() << ", " 
                 << cylinder.end.y() << ", " << cylinder.end.z() << ">,\n";
            file << "  " << cylinder.radius << "\n";
            file << "  pigment { color rgb <" 
                 << cylinder.color[0] << ", " 
                 << cylinder.color[1] << ", " 
                 << cylinder.color[2] << "> }\n";
            file << "  finish { phong 0.5 }\n";
            file << "}\n\n";
        }
        
        file.close();
        return true;
    }

    Eigen::Matrix3f Visualizer::optimal_view_angle(const Molecule& molecule) {
        // Calculate principal axes for optimal viewing
        // Simplified: return identity matrix
        return Eigen::Matrix3f::Identity();
    }

    void Visualizer::center_molecule(MolecularVisualization& viz) {
        Vec3f offset = -viz.center;
        
        for (auto& sphere : viz.atoms) {
            sphere.center += offset;
        }
        
        for (auto& cylinder : viz.bonds) {
            cylinder.start += offset;
            cylinder.end += offset;
        }
        
        viz.bounding_box_min += offset;
        viz.bounding_box_max += offset;
        viz.center = Vec3f::Zero();
    }

    void Visualizer::scale_visualization(MolecularVisualization& viz, float scale) {
        for (auto& sphere : viz.atoms) {
            sphere.center *= scale;
            sphere.radius *= scale;
        }
        
        for (auto& cylinder : viz.bonds) {
            cylinder.start *= scale;
            cylinder.end *= scale;
            cylinder.radius *= scale;
        }
        
        viz.bounding_box_min *= scale;
        viz.bounding_box_max *= scale;
        viz.center *= scale;
    }

    std::vector<Vec3f> Visualizer::generate_sphere_mesh(
        const Vec3f& center,
        float radius,
        int segments
    ) {
        std::vector<Vec3f> vertices;
        // Simplified sphere generation
        // Full implementation would generate proper mesh
        vertices.reserve(segments * segments);
        
        for (int i = 0; i < segments; ++i) {
            float theta = 2.0f * std::numbers::pi_v<float> * i / segments;
            for (int j = 0; j < segments; ++j) {
                float phi = std::numbers::pi_v<float> * j / segments;
                Vec3f point;
                point.x() = center.x() + radius * std::sin(phi) * std::cos(theta);
                point.y() = center.y() + radius * std::sin(phi) * std::sin(theta);
                point.z() = center.z() + radius * std::cos(phi);
                vertices.push_back(point);
            }
        }
        
        return vertices;
    }

    std::vector<Vec3f> Visualizer::generate_cylinder_mesh(
        const Vec3f& start,
        const Vec3f& end,
        float radius,
        int segments
    ) {
        std::vector<Vec3f> vertices;
        // Simplified cylinder generation
        vertices.reserve(segments * 2);
        
        Vec3f direction = (end - start).normalized();
        float length = (end - start).norm();
        
        // Generate circular cross-sections
        for (int i = 0; i < segments; ++i) {
            float angle = 2.0f * std::numbers::pi_v<float> * i / segments;
            // Simplified: would need proper perpendicular vectors
            Vec3f point = start + direction * (length * 0.5f);
            vertices.push_back(point);
        }
        
        return vertices;
    }

} // namespace sdt::chemistry

