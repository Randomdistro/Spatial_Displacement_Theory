#include "sdt/visualization/orbital_viewer.hpp"
#include <vtkInteractorStyleTrackballCamera.h>
#include <vtkTextProperty.h>
#include <vtkPNGWriter.h>
#include <vtkWindowToImageFilter.h>
#include <vtkColorTransferFunction.h>
#include <vtkPiecewiseFunction.h>
#include <iostream>
#include <cmath>

namespace sdt::visualization::atomic {

    OrbitalViewer3D::OrbitalViewer3D() {
        renderer_ = vtkSmartPointer<vtkRenderer>::New();
        render_window_ = vtkSmartPointer<vtkRenderWindow>::New();
        interactor_ = vtkSmartPointer<vtkRenderWindowInteractor>::New();
        
        render_window_->AddRenderer(renderer_);
        interactor_->SetRenderWindow(render_window_);
        
        auto style = vtkSmartPointer<vtkInteractorStyleTrackballCamera>::New();
        interactor_->SetInteractorStyle(style);
    }
    
    OrbitalViewer3D::~OrbitalViewer3D() = default;
    
    void OrbitalViewer3D::initialize(int width, int height) {
        render_window_->SetSize(width, height);
        render_window_->SetWindowName("SDT Atomic Orbital Visualization");
        
        renderer_->SetBackground(0.0, 0.0, 0.1);
        
        // Add axes
        axes_actor_ = vtkSmartPointer<vtkAxesActor>::New();
        axes_actor_->SetTotalLength(1e-10, 1e-10, 1e-10);  // Atomic scale
        axes_actor_->SetNormalizedShaftLength(0.9, 0.9, 0.9);
        axes_actor_->SetNormalizedTipLength(0.1, 0.1, 0.1);
        
        if (show_axes_) {
            auto orientation_widget = vtkSmartPointer<vtkOrientationMarkerWidget>::New();
            orientation_widget->SetOrientationMarker(axes_actor_);
            orientation_widget->SetInteractor(interactor_);
            orientation_widget->SetEnabled(1);
            orientation_widget->SetInteractive(0);
        }
    }
    
    void OrbitalViewer3D::visualize_orbital(const ElectronOrbital& orbital, double isosurface_value) {
        auto isosurface = create_orbital_isosurface(orbital, isosurface_value);
        auto color = get_orbital_color(orbital.state.qn.l, orbital.state.qn.m);
        auto actor = create_orbital_actor(orbital, color);
        
        orbital_actors_.push_back(actor);
        renderer_->AddActor(actor);
    }
    
    std::array<double, 3> OrbitalViewer3D::get_orbital_color(int l, int m) const {
        // Color scheme: s=red, p=green, d=blue, f=yellow
        std::array<double, 3> color;
        
        if (l == 0) {
            // s-orbital: red
            color = {1.0, 0.3, 0.3};
        } else if (l == 1) {
            // p-orbital: green (with m-dependent shading)
            if (m == 0) color = {0.3, 1.0, 0.3};  // pz: bright green
            else color = {0.2, 0.8, 0.2};  // px, py: darker green
        } else if (l == 2) {
            // d-orbital: blue
            color = {0.3, 0.3, 1.0};
        } else {
            // f-orbital: yellow
            color = {1.0, 1.0, 0.3};
        }
        
        return color;
    }
    
    vtkSmartPointer<vtkPolyData> OrbitalViewer3D::create_orbital_isosurface(
        const ElectronOrbital& orbital,
        double isovalue
    ) {
        // Generate probability density grid
        const Vec3d center(0.0, 0.0, 0.0);
        const double extent = 3.0 * orbital.expected_radius();
        const int resolution = 100;
        
        auto grid = orbital.generate_probability_grid(center, extent, resolution);
        
        // Create VTK image data
        auto image_data = vtkSmartPointer<vtkImageData>::New();
        image_data->SetDimensions(resolution, resolution, resolution);
        image_data->SetSpacing(
            2.0 * extent / resolution,
            2.0 * extent / resolution,
            2.0 * extent / resolution
        );
        image_data->SetOrigin(-extent, -extent, -extent);
        
        auto scalars = vtkSmartPointer<vtkFloatArray>::New();
        scalars->SetNumberOfTuples(resolution * resolution * resolution);
        
        int idx = 0;
        for (int k = 0; k < resolution; ++k) {
            for (int j = 0; j < resolution; ++j) {
                for (int i = 0; i < resolution; ++i) {
                    scalars->SetValue(idx++, static_cast<float>(grid[i][j][k]));
                }
            }
        }
        
        image_data->GetPointData()->SetScalars(scalars);
        
        // Marching cubes for isosurface
        auto marching_cubes = vtkSmartPointer<vtkMarchingCubes>::New();
        marching_cubes->SetInputData(image_data);
        marching_cubes->SetValue(0, isovalue);
        marching_cubes->Update();
        
        return marching_cubes->GetOutput();
    }
    
    vtkSmartPointer<vtkActor> OrbitalViewer3D::create_orbital_actor(
        const ElectronOrbital& orbital,
        const std::array<double, 3>& color
    ) {
        auto isosurface = create_orbital_isosurface(orbital, isosurface_value_);
        
        auto mapper = vtkSmartPointer<vtkPolyDataMapper>::New();
        mapper->SetInputData(isosurface);
        
        auto actor = vtkSmartPointer<vtkActor>::New();
        actor->SetMapper(mapper);
        actor->GetProperty()->SetColor(color[0], color[1], color[2]);
        actor->GetProperty()->SetOpacity(opacity_);
        actor->GetProperty()->SetAmbient(0.3);
        actor->GetProperty()->SetDiffuse(0.7);
        actor->GetProperty()->SetSpecular(0.5);
        
        return actor;
    }
    
    void OrbitalViewer3D::visualize_atom(const AtomicSystem& atom) {
        // Visualize nucleus
        if (show_nucleus_) {
            auto nucleus = vtkSmartPointer<vtkSphereSource>::New();
            nucleus->SetRadius(1e-15);  // Nuclear scale
            nucleus->SetThetaResolution(16);
            nucleus->SetPhiResolution(16);
            
            auto mapper = vtkSmartPointer<vtkPolyDataMapper>::New();
            mapper->SetInputConnection(nucleus->GetOutputPort());
            
            auto actor = vtkSmartPointer<vtkActor>::New();
            actor->SetMapper(mapper);
            actor->GetProperty()->SetColor(1.0, 1.0, 0.0);  // Yellow
            actor->SetPosition(0, 0, 0);
            
            nucleus_actor_ = actor;
            renderer_->AddActor(actor);
        }
        
        // Visualize each occupied orbital
        for (const auto& orbital_state : atom.occupied_orbitals) {
            ElectronOrbital orbital;
            orbital.state = orbital_state;
            orbital.Z = atom.Z;
            visualize_orbital(orbital);
        }
    }
    
    void OrbitalViewer3D::reset_camera() {
        renderer_->ResetCamera();
        render_window_->Render();
    }
    
    void OrbitalViewer3D::render() {
        render_window_->Render();
    }
    
    void OrbitalViewer3D::start_interactor() {
        interactor_->Start();
    }
    
    void OrbitalViewer3D::save_screenshot(const std::string& filename) {
        auto window_to_image = vtkSmartPointer<vtkWindowToImageFilter>::New();
        window_to_image->SetInput(render_window_);
        window_to_image->Update();
        
        auto writer = vtkSmartPointer<vtkPNGWriter>::New();
        writer->SetFileName(filename.c_str());
        writer->SetInputConnection(window_to_image->GetOutputPort());
        writer->Write();
    }

} // namespace sdt::visualization::atomic

