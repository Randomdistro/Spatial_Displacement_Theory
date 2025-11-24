#include "sdt/visualization/orbit_viewer.hpp"
#include "sdt/core/constants.hpp"
#include "sdt/core/types.hpp"
#include <iostream>
#include <fstream>
#include <sstream>
#include <cmath>
#include <algorithm>
#include <numbers>

namespace sdt::visualization {

    OrbitViewer3D::OrbitViewer3D() {
        renderer_ = vtkSmartPointer<vtkRenderer>::New();
        render_window_ = vtkSmartPointer<vtkRenderWindow>::New();
        interactor_ = vtkSmartPointer<vtkRenderWindowInteractor>::New();
        
        render_window_->AddRenderer(renderer_);
        interactor_->SetRenderWindow(render_window_);
        
        // Set interactor style
        vtkNew<vtkInteractorStyleTrackballCamera> style;
        interactor_->SetInteractorStyle(style);
    }
    
    OrbitViewer3D::~OrbitViewer3D() = default;
    
    void OrbitViewer3D::initialize(int width, int height) {
        render_window_->SetSize(width, height);
        render_window_->SetWindowName("SDT Orbital Mechanics Visualization");
        
        // Set background to space black
        renderer_->SetBackground(0.0, 0.0, 0.05);
        
        // Add axes
        axes_actor_ = vtkSmartPointer<vtkAxesActor>::New();
        axes_actor_->SetTotalLength(1e11, 1e11, 1e11);  // 1 AU scale
        axes_actor_->SetNormalizedShaftLength(0.9, 0.9, 0.9);
        axes_actor_->SetNormalizedTipLength(0.1, 0.1, 0.1);
        
        vtkNew<vtkOrientationMarkerWidget> orientation_widget;
        orientation_widget->SetOrientationMarker(axes_actor_);
        orientation_widget->SetInteractor(interactor_);
        orientation_widget->SetEnabled(show_axes_);
        orientation_widget->SetInteractive(0);
        orientation_widget_ = orientation_widget;
        
        // Create legend
        legend_ = vtkSmartPointer<vtkLegendBoxActor>::New();
        legend_->GetPositionCoordinate()->SetCoordinateSystemToNormalizedDisplay();
        legend_->GetPositionCoordinate()->SetValue(0.02, 0.98);
        legend_->BorderOff();
        legend_->SetNumberOfEntries(0);
        legend_->GetProperty()->SetColor(1.0, 1.0, 1.0);
        renderer_->AddActor2D(legend_);
        
        update_legend();
    }
    
    void OrbitViewer3D::add_trajectory(const TrajectoryData& trajectory) {
        trajectories_[trajectory.body_name] = trajectory;
        
        if (trajectory.show_orbit && !trajectory.positions.empty()) {
            auto poly_data = create_trajectory_polydata(trajectory);
            
            vtkNew<vtkPolyDataMapper> mapper;
            mapper->SetInputData(poly_data);
            
            vtkNew<vtkActor> actor;
            actor->SetMapper(mapper);
            actor->GetProperty()->SetColor(
                trajectory.color.color[0],
                trajectory.color.color[1],
                trajectory.color.color[2]
            );
            actor->GetProperty()->SetLineWidth(2.0);
            actor->GetProperty()->SetOpacity(trajectory.color.opacity);
            
            orbit_actors_.push_back(actor);
            renderer_->AddActor(actor);
        }
        
        update_legend();
    }
    
    void OrbitViewer3D::add_body(const CelestialBody& body, const BodyColor& color) {
        if (!color_scheme_.count(body.name)) {
            color_scheme_[body.name] = color;
        }
        
        auto actor = create_body_actor(body, color);
        body_actors_.push_back(actor);
        renderer_->AddActor(actor);
        
        update_legend();
    }
    
    vtkSmartPointer<vtkPolyData> OrbitViewer3D::create_trajectory_polydata(
        const TrajectoryData& trajectory
    ) {
        auto points = vtkSmartPointer<vtkPoints>::New();
        auto lines = vtkSmartPointer<vtkCellArray>::New();
        
        for (size_t i = 0; i < trajectory.positions.size(); ++i) {
            const auto& pos = trajectory.positions[i];
            points->InsertNextPoint(pos.x(), pos.y(), pos.z());
            
            if (i > 0) {
                vtkNew<vtkLine> line;
                line->GetPointIds()->SetId(0, static_cast<vtkIdType>(i - 1));
                line->GetPointIds()->SetId(1, static_cast<vtkIdType>(i));
                lines->InsertNextCell(line);
            }
        }
        
        auto poly_data = vtkSmartPointer<vtkPolyData>::New();
        poly_data->SetPoints(points);
        poly_data->SetLines(lines);
        
        return poly_data;
    }
    
    vtkSmartPointer<vtkActor> OrbitViewer3D::create_body_actor(
        const CelestialBody& body,
        const BodyColor& color
    ) {
        vtkNew<vtkSphereSource> sphere;
        
        // Scale radius for visualization (logarithmic scaling for huge range)
        const double min_display_size = 1e9;  // 1 million km minimum
        const double max_display_size = 1e11;  // 100 million km maximum
        
        double display_radius = std::max(body.radius, min_display_size);
        display_radius = std::min(display_radius, max_display_size);
        
        // Use logarithmic scaling for better visibility
        display_radius = min_display_size * std::pow(
            max_display_size / min_display_size,
            std::log(body.radius / min_display_size) / std::log(max_display_size / min_display_size)
        );
        
        display_radius *= color.size;
        
        sphere->SetRadius(display_radius);
        sphere->SetThetaResolution(32);
        sphere->SetPhiResolution(32);
        
        vtkNew<vtkPolyDataMapper> mapper;
        mapper->SetInputConnection(sphere->GetOutputPort());
        
        vtkNew<vtkActor> actor;
        actor->SetMapper(mapper);
        actor->GetProperty()->SetColor(color.color[0], color.color[1], color.color[2]);
        actor->GetProperty()->SetOpacity(color.opacity);
        actor->GetProperty()->SetAmbient(0.3);
        actor->GetProperty()->SetDiffuse(0.7);
        actor->GetProperty()->SetSpecular(0.5);
        actor->GetProperty()->SetSpecularPower(30.0);
        
        // Set position
        actor->SetPosition(body.position.x(), body.position.y(), body.position.z());
        
        return actor;
    }
    
    void OrbitViewer3D::convert_spectral_to_orbit(
        const std::string& body_name,
        const std::vector<SpectralDataPoint>& spectral_data,
        const CelestialBody& primary,
        double orbital_period,
        double inclination
    ) {
        if (spectral_data.empty()) {
            return;
        }
        
        TrajectoryData trajectory;
        trajectory.body_name = body_name;
        trajectory.color = get_default_color("planet");
        trajectory.show_orbit = true;
        
        // Convert radial velocity to orbital position
        // Simplified: assume circular orbit, edge-on view
        const double inclination_rad = inclination * M_PI / 180.0;
        const double sin_inclination = std::sin(inclination_rad);
        
        for (const auto& spec_point : spectral_data) {
            // Radial velocity gives us component along line of sight
            // v_radial = v_orbital * sin(inclination) * sin(phase)
            
            // Estimate orbital velocity amplitude from max radial velocity
            static double max_radial_velocity = 0.0;
            max_radial_velocity = std::max(max_radial_velocity, std::abs(spec_point.radial_velocity));
            
            // Phase angle from time
            const double phase = 2.0 * M_PI * spec_point.time / orbital_period;
            
            // Estimate semi-major axis from velocity
            // v = (c/κ)√(R/r), so r = R * (c/κ)² / v²
            // Simplified: assume circular orbit
            const double v_orbital = std::abs(spec_point.radial_velocity) / sin_inclination;
            const double a = primary.sdt_params.R_eff * 
                           (constants::c / primary.sdt_params.kappa) * 
                           (constants::c / primary.sdt_params.kappa) / 
                           (v_orbital * v_orbital);
            
            // Position in orbital plane
            const double x = a * std::cos(phase);
            const double y = a * std::sin(phase);
            const double z = 0.0;  // Simplified: assume orbit in xy-plane
            
            Vec3d position(x, y, z);
            position += primary.position;  // Relative to primary
            
            trajectory.positions.push_back(position);
            trajectory.times.push_back(spec_point.time);
        }
        
        add_trajectory(trajectory);
        spectral_data_[body_name] = spectral_data;
    }
    
    void OrbitViewer3D::reset_camera() {
        renderer_->ResetCamera();
        render_window_->Render();
    }
    
    void OrbitViewer3D::render() {
        render_window_->Render();
    }
    
    void OrbitViewer3D::start_interactor() {
        interactor_->Start();
    }
    
    BodyColor OrbitViewer3D::get_default_color(const std::string& body_type) const {
        BodyColor color;
        
        if (body_type == "star" || body_type == "Sun") {
            color.color = {1.0, 1.0, 0.8};  // Yellow-white
            color.size = 2.0;
        } else if (body_type == "planet") {
            color.color = {0.5, 0.7, 1.0};  // Light blue
            color.size = 0.5;
        } else if (body_type == "moon") {
            color.color = {0.7, 0.7, 0.7};  // Gray
            color.size = 0.2;
        } else {
            color.color = {1.0, 1.0, 1.0};  // White
            color.size = 0.5;
        }
        
        return color;
    }
    
    void OrbitViewer3D::update_legend() {
        legend_->SetNumberOfEntries(0);
        
        for (const auto& [name, trajectory] : trajectories_) {
            legend_->AddEntry(
                trajectory.color.color[0],
                trajectory.color.color[1],
                trajectory.color.color[2],
                name.c_str()
            );
        }
    }
    
    void OrbitViewer3D::show_orbits(bool show) {
        show_orbits_ = show;
        for (auto& actor : orbit_actors_) {
            actor->SetVisibility(show ? 1 : 0);
        }
    }
    
    void OrbitViewer3D::show_bodies(bool show) {
        show_bodies_ = show;
        for (auto& actor : body_actors_) {
            actor->SetVisibility(show ? 1 : 0);
        }
    }
    
    void OrbitViewer3D::show_axes(bool show) {
        show_axes_ = show;
        if (orientation_widget_) {
            orientation_widget_->SetEnabled(show ? 1 : 0);
        }
    }
    
    void OrbitViewer3D::save_screenshot(const std::string& filename) {
        vtkNew<vtkWindowToImageFilter> window_to_image;
        window_to_image->SetInput(render_window_);
        window_to_image->Update();
        
        vtkNew<vtkPNGWriter> writer;
        writer->SetFileName(filename.c_str());
        writer->SetInputConnection(window_to_image->GetOutputPort());
        writer->Write();
    }
    
    std::unordered_map<std::string, BodyColor> create_solar_system_colors() {
        std::unordered_map<std::string, BodyColor> colors;
        
        // Sun
        colors["Sun"] = {{1.0, 1.0, 0.8}, 1.0, 2.0};
        
        // Planets
        colors["Mercury"] = {{0.7, 0.7, 0.7}, 1.0, 0.4};
        colors["Venus"] = {{1.0, 0.8, 0.6}, 1.0, 0.6};
        colors["Earth"] = {{0.2, 0.5, 1.0}, 1.0, 0.6};
        colors["Mars"] = {{1.0, 0.3, 0.2}, 1.0, 0.5};
        colors["Jupiter"] = {{0.9, 0.7, 0.5}, 1.0, 1.2};
        colors["Saturn"] = {{0.9, 0.8, 0.6}, 1.0, 1.0};
        colors["Uranus"] = {{0.6, 0.8, 1.0}, 1.0, 0.8};
        colors["Neptune"] = {{0.2, 0.4, 1.0}, 1.0, 0.8};
        
        return colors;
    }

} // namespace sdt::visualization

