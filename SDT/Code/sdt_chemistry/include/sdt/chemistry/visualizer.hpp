#pragma once

#include "molecules.hpp"
#include "elements.hpp"
#include "bonds.hpp"
#include <Eigen/Dense>
#include <vector>
#include <string>
#include <array>

namespace sdt::chemistry {

    using Vec3d = Eigen::Vector3d;
    using Vec3f = Eigen::Vector3f;
    using Color = std::array<float, 3>;  // RGB color [0-1]

    /**
     * CPK color scheme for elements (standard convention)
     */
    class CPKColors {
    public:
        /**
         * Get CPK color for element
         * Returns RGB values in [0, 1] range
         */
        static Color get_color(int element_Z);
        
        /**
         * Get CPK color by element symbol
         */
        static Color get_color(const std::string& symbol);
        
        /**
         * Get atomic radius for visualization (scaled for display)
         */
        static float get_visual_radius(int element_Z, float scale = 1.0f);
    };

    /**
     * 3D geometry primitives for visualization
     */
    struct Sphere {
        Vec3f center;
        float radius;
        Color color;
    };

    struct Cylinder {
        Vec3f start;
        Vec3f end;
        float radius;
        Color color;
    };

    /**
     * Visual representation of a molecule (stick-and-ball model)
     */
    struct MolecularVisualization {
        std::vector<Sphere> atoms;      // Atoms as spheres
        std::vector<Cylinder> bonds;   // Bonds as cylinders
        Vec3f center;                  // Center of molecule
        Vec3f bounding_box_min;        // Bounding box
        Vec3f bounding_box_max;
    };

    /**
     * Molecular visualizer using SDT geometry
     */
    class Visualizer {
    public:
        /**
         * Create stick-and-ball visualization from molecule
         * 
         * Uses SDT-calculated positions and bond lengths
         * Atoms are rendered as spheres, bonds as cylinders
         */
        static MolecularVisualization create_stick_ball_model(
            const Molecule& molecule,
            float atom_scale = 1.0f,
            float bond_radius = 0.1f,
            bool use_cpk_colors = true
        );
        
        /**
         * Export to OBJ format (Wavefront)
         */
        static bool export_to_obj(
            const MolecularVisualization& viz,
            const std::string& filepath
        );
        
        /**
         * Export to PLY format (Stanford Polygon)
         */
        static bool export_to_ply(
            const MolecularVisualization& viz,
            const std::string& filepath
        );
        
        /**
         * Export to PDB format (Protein Data Bank)
         */
        static bool export_to_pdb(
            const Molecule& molecule,
            const std::string& filepath
        );
        
        /**
         * Export to XYZ format (simple coordinate format)
         */
        static bool export_to_xyz(
            const Molecule& molecule,
            const std::string& filepath
        );
        
        /**
         * Generate POV-Ray scene file
         */
        static bool export_to_pov(
            const MolecularVisualization& viz,
            const std::string& filepath
        );
        
        /**
         * Calculate optimal viewing angle
         * Returns rotation matrix for best view
         */
        static Eigen::Matrix3f optimal_view_angle(const Molecule& molecule);
        
        /**
         * Center molecule at origin
         */
        static void center_molecule(MolecularVisualization& viz);
        
        /**
         * Scale visualization
         */
        static void scale_visualization(MolecularVisualization& viz, float scale);
        
    private:
        /**
         * Generate sphere mesh vertices (for OBJ/PLY export)
         */
        static std::vector<Vec3f> generate_sphere_mesh(
            const Vec3f& center,
            float radius,
            int segments = 16
        );
        
        /**
         * Generate cylinder mesh vertices
         */
        static std::vector<Vec3f> generate_cylinder_mesh(
            const Vec3f& start,
            const Vec3f& end,
            float radius,
            int segments = 8
        );
        
        /**
         * Calculate bond cylinder geometry from SDT positions
         */
        static Cylinder create_bond_cylinder(
            const Atom& atom1,
            const Atom& atom2,
            const Bond& bond,
            float bond_radius
        );
    };

} // namespace sdt::chemistry

