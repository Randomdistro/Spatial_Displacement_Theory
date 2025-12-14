# Vulkan SDT Solar System Visualization

A high-performance 3D solar system simulation using Vulkan graphics API with Spatial Displacement Theory (SDT) physics.

## Status

**Agent 1 (Vulkan Core Infrastructure):** ✅ Complete
- Vulkan instance, device, swapchain setup
- Command buffers and synchronization
- Descriptor sets for camera uniforms
- Base renderer class with frame loop

**Agent 2 (Shaders & Pipelines):** ⏳ Pending
- Shader compilation system
- Planet rendering pipeline
- Point particle pipeline
- Orbit trail pipeline

**Agent 3 (Physics & UI):** ⏳ Pending
- JPL DE421 ephemeris loader
- SDT physics integration
- Camera system
- ImGui UI

## Building

### Prerequisites

- **Vulkan SDK 1.3+** - Download from [vulkan.lunarg.com](https://vulkan.lunarg.com/)
- **CMake 3.20+**
- **C++20 compatible compiler** (MSVC 2019+, GCC 10+, Clang 12+)
- **GLFW 3.3+** - Can be installed via package manager or built from source

### Windows Build

```bash
# Install Vulkan SDK and add to PATH
# Install GLFW (or use vcpkg: vcpkg install glfw3)

mkdir build
cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
cmake --build . --config Release
```

### Linux Build

```bash
# Install dependencies
sudo apt-get install libvulkan-dev libglfw3-dev cmake build-essential

mkdir build
cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
make -j$(nproc)
```

### Running

```bash
# From build directory
./bin/vulkan_solar_system
```

## Project Structure

```
Vulkan_Solar_System/
├── CMakeLists.txt          # Build configuration
├── src/
│   ├── main.cpp            # Application entry point
│   └── vulkan/
│       ├── vulkan_context.cpp/hpp      # Device selection and queues
│       ├── vulkan_renderer.cpp/hpp     # Main renderer class
│       ├── vulkan_buffers.cpp/hpp      # Buffer management
│       └── vulkan_descriptors.cpp/hpp   # Descriptor sets
├── include/
│   └── vulkan/             # Header files
└── shaders/                 # GLSL shaders (to be added by Agent 2)
```

## Current Features

- ✅ Vulkan instance and device initialization
- ✅ Swapchain with triple buffering (MAILBOX mode)
- ✅ Command buffer recording and submission
- ✅ Frame synchronization (semaphores and fences)
- ✅ Descriptor sets for camera uniforms
- ✅ Window resizing support
- ✅ Basic render loop (clears screen to dark blue)

## Next Steps

1. **Agent 2** will add shaders and rendering pipelines
2. **Agent 3** will add physics simulation and UI controls
3. Integration testing and optimization

## Notes

- The renderer currently clears the screen to a dark blue color
- Camera uniform buffer is set up but not yet populated with matrices
- Command buffers are ready for drawing commands (to be added by Agent 2)

