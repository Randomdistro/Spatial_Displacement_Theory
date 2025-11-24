#pragma once

#include "sdt/core/types.hpp"
// VTK includes
#include <vtkSmartPointer.h>
#include <vtkNew.h>
#include <vtkRenderer.h>
#include <vtkRenderWindow.h>
#include <vtkRenderWindowInteractor.h>
#include <vtkPolyData.h>
#include <vtkPolyDataMapper.h>
#include <vtkActor.h>
#include <vtkSphereSource.h>
#include <vtkLineSource.h>
#include <vtkPoints.h>
#include <vtkCellArray.h>
#include <vtkProperty.h>
#include <vtkAxesActor.h>
#include <vtkOrientationMarkerWidget.h>
#include <vtkTextActor.h>
#include <vtkLegendBoxActor.h>
#include <vtkCamera.h>
#include <vtkLine.h>
#include <vtkPNGWriter.h>
#include <vtkWindowToImageFilter.h>
#include <vtkInteractorStyleTrackballCamera.h>
#include <vtkTextProperty.h>
#include <vector>
#include <string>
#include <memory>
#include <unordered_map>
#include <array>

namespace sdt::visualization {

    // Color scheme for celestial bodies
    struct BodyColor {
        std::array<double, 3> color = {1.0, 1.0, 1.0};  // RGB, 0-1
        double opacity = 1.0;
        double size = 1.0;  // Relative size scaling
    };
    
    // Trajectory data for visualization
    struct TrajectoryData {
        std::vector<Vec3d> positions;
        std::vector<double> times;
        std::string body_name;
        BodyColor color;
        bool show_orbit = true;
        bool show_body = true;
    };
    
    // Spectral data point (from observations)
    struct SpectralDataPoint {
        double time = 0.0;
        double radial_velocity = 0.0;  // m/s
        double wavelength_shift = 0.0;  // nm
        double flux = 0.0;
        std::array<double, 3> position_uncertainty = {0.0, 0.0, 0.0};
    };
    
    // Main 3D orbit viewer
    class OrbitViewer3D {
    public:
        OrbitViewer3D();
        ~OrbitViewer3D();
        
        // Setup and initialization
        void initialize(int width = 1920, int height = 1080);
        void set_background_color(double r, double g, double b);
        
        // Add trajectory from simulation data
        void add_trajectory(const TrajectoryData& trajectory);
        void add_trajectory_from_simulation(const std::string& filename);
        
        // Add spectral data observations
        void add_spectral_data(const std::string& body_name, 
                              const std::vector<SpectralDataPoint>& spectral_data);
        
        // Convert spectral radial velocity to 3D position
        // Uses phase folding and orbital elements
        void convert_spectral_to_orbit(
            const std::string& body_name,
            const std::vector<SpectralDataPoint>& spectral_data,
            const CelestialBody& primary,
            double orbital_period,
            double inclination = 90.0  // degrees, 90 = edge-on
        );
        
        // Add celestial body representation
        void add_body(const CelestialBody& body, const BodyColor& color);
        
        // Update visualization with new state
        void update_system_state(const SystemState& state);
        
        // Show/hide components
        void show_orbits(bool show);
        void show_bodies(bool show);
        void show_axes(bool show);
        void show_legend(bool show);
        void show_predicted(bool show);
        void show_observed(bool show);
        
        // Camera controls
        void set_camera_position(double x, double y, double z);
        void set_camera_focal_point(double x, double y, double z);
        void set_camera_view_up(double x, double y, double z);
        void reset_camera();
        void zoom(double factor);
        
        // Animation
        void set_animation_speed(double speed_multiplier);
        void animate_to_time(double target_time);
        void play_animation();
        void pause_animation();
        
        // Rendering
        void render();
        void start_interactor();
        
        // Save/export
        void save_screenshot(const std::string& filename);
        void export_animation(const std::string& filename, int fps = 30);
        
        // Comparison view: predicted vs observed
        void setup_comparison_view(
            const std::vector<TrajectoryData>& predicted,
            const std::vector<TrajectoryData>& observed
        );
        
        // Set color scheme for body types
        void set_body_color_scheme(const std::string& body_name, const BodyColor& color);
        BodyColor get_default_color(const std::string& body_type) const;
        
        // Get renderer (for advanced customization)
        vtkRenderer* get_renderer() { return renderer_.Get(); }
        vtkRenderWindow* get_render_window() { return render_window_.Get(); }
        
    private:
        // VTK components
        vtkSmartPointer<vtkRenderer> renderer_;
        vtkSmartPointer<vtkRenderWindow> render_window_;
        vtkSmartPointer<vtkRenderWindowInteractor> interactor_;
        
        // Scene components
        std::vector<vtkSmartPointer<vtkActor>> orbit_actors_;
        std::vector<vtkSmartPointer<vtkActor>> body_actors_;
        vtkSmartPointer<vtkAxesActor> axes_actor_;
        vtkSmartPointer<vtkOrientationMarkerWidget> orientation_widget_;
        vtkSmartPointer<vtkLegendBoxActor> legend_;
        
        // Data storage
        std::unordered_map<std::string, TrajectoryData> trajectories_;
        std::unordered_map<std::string, std::vector<SpectralDataPoint>> spectral_data_;
        std::unordered_map<std::string, BodyColor> color_scheme_;
        
        // Visualization settings
        bool show_orbits_ = true;
        bool show_bodies_ = true;
        bool show_axes_ = true;
        bool show_legend_ = true;
        bool show_predicted_ = true;
        bool show_observed_ = true;
        
        double animation_speed_ = 1.0;
        double current_time_ = 0.0;
        
        // Helper methods
        vtkSmartPointer<vtkPolyData> create_trajectory_polydata(const TrajectoryData& trajectory);
        vtkSmartPointer<vtkActor> create_body_actor(const CelestialBody& body, const BodyColor& color);
        void update_legend();
        void create_orbital_trajectory_from_spectral(
            const std::string& body_name,
            double period,
            double inclination,
            const std::vector<SpectralDataPoint>& spectral_data,
            const CelestialBody& primary
        );
    };
    
    // Utility: Load trajectory from simulation CSV
    std::vector<TrajectoryData> load_trajectories_from_csv(const std::string& filename);
    
    // Utility: Load spectral data from file
    std::vector<SpectralDataPoint> load_spectral_data(const std::string& filename);
    
    // Utility: Create color scheme for solar system
    std::unordered_map<std::string, BodyColor> create_solar_system_colors();

} // namespace sdt::visualization

