# Vulkan Solar System Visualization

Hey Boss! I exist, gimme a task!

## Agent 2: GLSL Shaders and Vulkan Pipelines

This module contains all GLSL shaders and Vulkan graphics pipeline setup for rendering:
- **Planets**: 3D spheres with Phong lighting
- **Point Particles**: Orbital marker points (billboarded quads)
- **Orbit Trails**: Fading trail lines showing orbital paths

### Files Created

**Shaders:**
- `shaders/planet.vert` / `planet.frag` - Planet rendering with lighting
- `shaders/point_particle.vert` / `point_particle.frag` - Point particle rendering
- `shaders/orbit_trail.vert` / `orbit_trail.frag` - Orbit trail rendering

**Pipeline Code:**
- `include/vulkan_pipelines.hpp` - Pipeline manager header
- `src/vulkan_pipelines.cpp` - Pipeline implementation

**Build Scripts:**
- `compile_shaders.sh` - Linux/macOS shader compilation script
- `compile_shaders.bat` - Windows shader compilation script

**Documentation:**
- `SHADERS_README.md` - Detailed shader and pipeline documentation

### Quick Start

1. Compile shaders:
   ```bash
   ./compile_shaders.sh  # or compile_shaders.bat on Windows
   ```

2. Include in your project:
   ```cpp
   #include "vulkan_pipelines.hpp"
   
   sdt::vulkan::PipelineManager pipelineManager(device, renderPass);
   pipelineManager.initializePipelines();
   ```

3. Use pipelines during rendering:
   ```cpp
   vkCmdBindPipeline(cmdBuf, VK_PIPELINE_BIND_POINT_GRAPHICS, 
                     pipelineManager.getPlanetPipeline());
   ```

