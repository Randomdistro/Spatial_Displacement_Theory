# Vulkan Shaders and Pipelines

This directory contains all GLSL shaders and Vulkan pipeline setup code for the SDT Solar System visualization.

## Shader Files

### Planet Shaders
- `shaders/planet.vert` - Vertex shader for planet rendering with lighting
- `shaders/planet.frag` - Fragment shader for planet rendering with Phong lighting

### Point Particle Shaders
- `shaders/point_particle.vert` - Vertex shader for orbital marker points (billboarded)
- `shaders/point_particle.frag` - Fragment shader for point particles with soft edges

### Orbit Trail Shaders
- `shaders/orbit_trail.vert` - Vertex shader for orbit trail lines
- `shaders/orbit_trail.frag` - Fragment shader for trail lines with fade effects

## Compiling Shaders

Shaders must be compiled to SPIR-V format before use. Use the provided scripts:

**Linux/macOS:**
```bash
chmod +x compile_shaders.sh
./compile_shaders.sh
```

**Windows:**
```cmd
compile_shaders.bat
```

This requires the Vulkan SDK to be installed with `glslc` compiler.

## Pipeline Structure

The `PipelineManager` class manages three graphics pipelines:

1. **Planet Pipeline** - Renders 3D planet spheres with lighting
   - Uses descriptor sets for uniforms and planet properties
   - Supports position, normal, and texture coordinates

2. **Point Particle Pipeline** - Renders orbital marker points
   - Uses push constants for per-particle data
   - Billboarded quads that always face the camera
   - Alpha blending for soft edges

3. **Orbit Trail Pipeline** - Renders orbit trail lines
   - Uses descriptor sets for uniforms and trail properties
   - Supports time-based fading along the trail
   - Alpha blending for smooth fade effects

## Usage

```cpp
#include "vulkan_pipelines.hpp"

// Initialize pipelines
sdt::vulkan::PipelineManager pipelineManager(device, renderPass);
pipelineManager.initializePipelines();

// Use pipelines during rendering
vkCmdBindPipeline(commandBuffer, VK_PIPELINE_BIND_POINT_GRAPHICS, 
                  pipelineManager.getPlanetPipeline());
```

## Descriptor Sets

- **Set 0**: Uniform buffer (UBO) - Contains view/projection matrices, camera position, light position, time
- **Set 1**: Planet properties - Per-planet color, radius, emissivity, specular
- **Set 2**: Trail properties - Trail color, width, fade parameters

## Push Constants

Point particle pipeline uses push constants:
- `vec3 position` - World position
- `float size` - Particle size
- `vec3 color` - Particle color

