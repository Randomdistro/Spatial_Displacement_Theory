#pragma once

#include "sdt/physics/electron_orbitals.hpp"
#include "sdt/physics/spectral_transitions.hpp"
#include <vtkSmartPointer.h>
#include <vtkRenderer.h>
#include <vtkRenderWindow.h>
#include <vtkRenderWindowInteractor.h>
#include <vtkPolyData.h>
#include <vtkPolyDataMapper.h>
#include <vtkActor.h>
#include <vtkSphereSource.h>
#include <vtkMarchingCubes.h>
#include <vtkVolume.h>
#include <vtkVolumeMapper.h>
#include <vtkColorTransferFunction.h>
#include <vtkPiecewiseFunction.h>
#include <vtkAxesActor.h>
#include <vtkOrientationMarkerWidget.h>
#include <vtkChartXY.h>
#include <vtkPlot.h>
#include <vtkTable.h>
#include <vtkContextView.h>
#include <vtkFloatArray.h>
#include <string>
#include <vector>
#include <memory>

namespace sdt::visualization::atomic {

    // 3D orbital visualization viewer
    class OrbitalViewer3D {
    public:
        OrbitalViewer3D();
        ~OrbitalViewer3D();
        
        // Initialize viewer
        void initialize(int width = 1920, int height = 1080);
        
        // Visualize single orbital
        void visualize_orbital(const ElectronOrbital& orbital, double isosurface_value = 0.01);
        
        // Visualize multiple orbitals (overlay)
        void visualize_orbitals(const std::vector<ElectronOrbital>& orbitals);
        
        // Visualize atomic system (electron density)
        void visualize_atom(const AtomicSystem& atom);
        
        // Visualize orbital transition (animation)
        void visualize_transition(
            const OrbitalState& initial,
            const OrbitalState& final,
            bool animate = true
        );
        
        // Energy level diagram
        void show_energy_levels(const AtomicSystem& atom, int max_n = 10);
        
        // Spectral line visualization
        void show_spectrum(const AtomicSpectrum& spectrum);
        
        // Set visualization options
        void set_isosurface_value(double value);
        void set_colormap(const std::string& colormap_name);
        void set_opacity(double opacity);
        void show_nucleus(bool show);
        void show_axes(bool show);
        void show_orbital_labels(bool show);
        
        // Camera controls
        void reset_camera();
        void set_view_angle(const std::string& view);  // "xy", "xz", "yz", "3d"
        
        // Rendering
        void render();
        void start_interactor();
        void save_screenshot(const std::string& filename);
        
        // Animation
        void animate_transition(double duration = 2.0);
        void set_animation_speed(double speed);
        
    private:
        vtkSmartPointer<vtkRenderer> renderer_;
        vtkSmartPointer<vtkRenderWindow> render_window_;
        vtkSmartPointer<vtkRenderWindowInteractor> interactor_;
        
        std::vector<vtkSmartPointer<vtkActor>> orbital_actors_;
        vtkSmartPointer<vtkActor> nucleus_actor_;
        vtkSmartPointer<vtkAxesActor> axes_actor_;
        
        double isosurface_value_ = 0.01;
        double opacity_ = 0.7;
        bool show_nucleus_ = true;
        bool show_axes_ = true;
        
        // Helper methods
        vtkSmartPointer<vtkPolyData> create_orbital_isosurface(
            const ElectronOrbital& orbital,
            double isovalue
        );
        
        vtkSmartPointer<vtkActor> create_orbital_actor(
            const ElectronOrbital& orbital,
            const std::array<double, 3>& color
        );
        
        std::array<double, 3> get_orbital_color(int l, int m) const;
    };
    
    // Energy level diagram viewer
    class EnergyLevelViewer {
    public:
        EnergyLevelViewer();
        
        // Show energy levels for atom
        void show_levels(const AtomicSystem& atom, int max_n = 10);
        
        // Show transitions
        void show_transitions(const std::vector<SpectralTransition>& transitions);
        
        // Show fine structure
        void show_fine_structure(const FineStructureLevel& level);
        
        // Render to window
        void render();
        
    private:
        vtkSmartPointer<vtkRenderer> renderer_;
        vtkSmartPointer<vtkRenderWindow> render_window_;
        vtkSmartPointer<vtkContextView> chart_view_;
        vtkSmartPointer<vtkChartXY> chart_;
    };
    
    // Spectral line viewer (2D plot)
    class SpectralViewer {
    public:
        SpectralViewer();
        
        // Show spectrum
        void show_spectrum(const AtomicSpectrum& spectrum);
        
        // Compare calculated vs experimental
        void compare_spectra(
            const AtomicSpectrum& calculated,
            const AtomicSpectrum& experimental
        );
        
        // Show specific series
        void show_series(const AtomicSpectrum& spectrum, SpectralSeries series);
        
        // Render
        void render();
        
    private:
        vtkSmartPointer<vtkContextView> view_;
        vtkSmartPointer<vtkChartXY> chart_;
    };
    
    // Transition animation viewer
    class TransitionViewer {
    public:
        TransitionViewer();
        
        // Animate transition between states
        void animate_transition(
            const OrbitalState& initial,
            const OrbitalState& final,
            double duration = 2.0
        );
        
        // Show photon emission
        void show_photon_emission(
            const Vec3d& source_position,
            double wavelength,
            const Vec3d& direction
        );
        
        // Render
        void render();
        void start_interactor();
        
    private:
        vtkSmartPointer<vtkRenderer> renderer_;
        vtkSmartPointer<vtkRenderWindow> render_window_;
        vtkSmartPointer<vtkRenderWindowInteractor> interactor_;
    };

} // namespace sdt::visualization::atomic

