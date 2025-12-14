#!/bin/bash

# Compile GLSL shaders to SPIR-V using glslc (from Vulkan SDK)

SHADER_DIR="shaders"
OUTPUT_DIR="shaders/spv"

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Check if glslc is available
if ! command -v glslc &> /dev/null; then
    echo "Error: glslc not found. Please install Vulkan SDK."
    exit 1
fi

# Compile vertex shaders
echo "Compiling vertex shaders..."
glslc "$SHADER_DIR/planet.vert" -o "$OUTPUT_DIR/planet.vert.spv"
glslc "$SHADER_DIR/point_particle.vert" -o "$OUTPUT_DIR/point_particle.vert.spv"
glslc "$SHADER_DIR/orbit_trail.vert" -o "$OUTPUT_DIR/orbit_trail.vert.spv"

# Compile fragment shaders
echo "Compiling fragment shaders..."
glslc "$SHADER_DIR/planet.frag" -o "$OUTPUT_DIR/planet.frag.spv"
glslc "$SHADER_DIR/point_particle.frag" -o "$OUTPUT_DIR/point_particle.frag.spv"
glslc "$SHADER_DIR/orbit_trail.frag" -o "$OUTPUT_DIR/orbit_trail.frag.spv"

echo "Shader compilation complete!"

