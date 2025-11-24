#!/bin/bash
# Build script for SDT Orbital Simulation

set -e

echo "=== SDT Orbital Simulation Build Script ==="

# Create build directory
mkdir -p build
cd build

# Configure CMake
echo "Configuring CMake..."
cmake .. -DCMAKE_BUILD_TYPE=Release

# Build
echo "Building..."
make -j$(nproc)

echo "Build complete!"
echo "Executable: build/sdt_sim"
echo ""
echo "Usage: ./build/sdt_sim [data_file] [output_file] [simulation_time]"

