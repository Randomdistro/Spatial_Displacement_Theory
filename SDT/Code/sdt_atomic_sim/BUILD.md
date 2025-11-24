# SDT Atomic Physics Simulator - Build Instructions

## Prerequisites

### Required Dependencies

1. **C++ Compiler** (C++20 support required)
   - GCC 10+ (recommended: GCC 11+)
   - Clang 12+ (recommended: Clang 14+)
   - MSVC 2019+ (Windows, with `/std:c++20` flag)

2. **CMake** 3.20 or later

3. **Eigen3** (header-only library)
   - Minimum version: 3.3
   - Installation:
     ```bash
     # Ubuntu/Debian
     sudo apt-get install libeigen3-dev
     
     # macOS (Homebrew)
     brew install eigen
     
     # Windows (vcpkg)
     vcpkg install eigen3
     ```

4. **VTK** (Visualization Toolkit) 9.0 or later
   - Required for 3D orbital visualization
   - Installation:
     ```bash
     # Ubuntu/Debian
     sudo apt-get install libvtk9-dev
     
     # macOS (Homebrew)
     brew install vtk
     
     # Windows (vcpkg)
     vcpkg install vtk
     ```

5. **fmt** (formatting library)
   - Required for formatted output
   - Installation:
     ```bash
     # Ubuntu/Debian
     sudo apt-get install libfmt-dev
     
     # macOS (Homebrew)
     brew install fmt
     
     # Windows (vcpkg)
     vcpkg install fmt
     ```

### Optional Dependencies

- **HDF5** (for large dataset storage, future feature)
- **OpenMP** (for parallelization)
- **CUDA** (for GPU acceleration, future feature)

## Build Process

### Step 1: Configure CMake

```bash
cd SDT/Code/sdt_atomic_sim
mkdir build
cd build
cmake ..
```

**CMake Configuration Options:**

```bash
# Specify VTK location if not found automatically
cmake -DVTK_DIR=/path/to/vtk/lib/cmake/vtk-9.0 ..

# Specify Eigen3 location
cmake -DEigen3_DIR=/path/to/eigen3/share/eigen3/cmake ..

# Enable debug build
cmake -DCMAKE_BUILD_TYPE=Debug ..

# Enable optimized release build
cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_CXX_FLAGS="-O3 -march=native" ..

# Use specific compiler
cmake -DCMAKE_CXX_COMPILER=g++-11 ..
```

### Step 2: Build

```bash
# Build all targets
cmake --build . -j$(nproc)

# Or use make directly
make -j$(nproc)
```

On Windows:
```cmd
cmake --build . --config Release -j%NUMBER_OF_PROCESSORS%
```

### Step 3: Install (Optional)

```bash
cmake --install . --prefix /usr/local
```

## Build Outputs

After successful build, you'll find:

- `build/sdt_atomic_sim` - Main simulation executable
- `build/sdt_atomic_viewer` - 3D visualization tool
- `build/libsdt_atomic.a` - Static library (if building as library)

## Testing

### Run Basic Tests

```bash
# Run simulation examples
./sdt_atomic_sim

# Run visualization tool
./sdt_atomic_viewer orbital 1 0 0
```

### Expected Output

The simulator should:
1. Calculate hydrogen ground state energy: -13.598 eV
2. Calculate Lyman α wavelength: ~121.57 nm
3. Generate spectral series
4. Calculate fine structure splitting

## Troubleshooting

### VTK Not Found

**Error:** `Could not find VTK`

**Solution:**
```bash
# Set VTK_DIR environment variable
export VTK_DIR=/usr/lib/cmake/vtk-9.0
# Or specify in CMake
cmake -DVTK_DIR=/path/to/vtk/lib/cmake/vtk-9.0 ..
```

### Eigen3 Not Found

**Error:** `Could not find Eigen3`

**Solution:**
```bash
# Install Eigen3 development package
sudo apt-get install libeigen3-dev

# Or specify path
cmake -DEigen3_DIR=/usr/share/eigen3/cmake ..
```

### fmt Not Found

**Error:** `Could not find fmt`

**Solution:**
```bash
# Install fmt development package
sudo apt-get install libfmt-dev

# Or use vcpkg
vcpkg install fmt
```

### C++20 Support Missing

**Error:** `C++20 features not available`

**Solution:**
- Upgrade compiler to GCC 10+, Clang 12+, or MSVC 2019+
- For older compilers, enable C++20 explicitly:
  ```bash
  cmake -DCMAKE_CXX_STANDARD=20 ..
  ```

### Link Errors

**Error:** `undefined reference to vtk...`

**Solution:**
- Ensure VTK is properly linked
- Check that VTK libraries are in library path
- Rebuild VTK if necessary

### Runtime Errors

**Error:** `Segmentation fault in visualization`

**Solution:**
- Ensure VTK display backend is available
- Check X11/Wayland/OpenGL drivers
- Run with debug build for stack trace

## Platform-Specific Notes

### Linux

- Most dependencies available via package manager
- OpenGL drivers required for VTK rendering
- X11 or Wayland for window management

### macOS

- Use Homebrew for dependencies
- May need to install XQuartz for X11 support
- Metal backend available for VTK

### Windows

- Use vcpkg for dependency management
- Requires Visual Studio 2019+ or MinGW-w64
- May need to install Visual C++ Redistributables

## Development Build

For development with debugging symbols:

```bash
cmake -DCMAKE_BUILD_TYPE=Debug -DCMAKE_CXX_FLAGS="-g -O0 -fsanitize=address" ..
make -j$(nproc)
```

## Production Build

For optimized production builds:

```bash
cmake -DCMAKE_BUILD_TYPE=Release \
      -DCMAKE_CXX_FLAGS="-O3 -march=native -DNDEBUG" ..
make -j$(nproc)
```

## Cross-Compilation

For cross-compilation to different architectures:

```bash
cmake -DCMAKE_TOOLCHAIN_FILE=/path/to/toolchain.cmake ..
```

## Docker Build

Example Dockerfile:

```dockerfile
FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libeigen3-dev \
    libvtk9-dev \
    libfmt-dev

WORKDIR /build
COPY . .
RUN mkdir build && cd build && cmake .. && make -j$(nproc)
```

## CI/CD Integration

Example GitHub Actions workflow:

```yaml
name: Build SDT Atomic Sim

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Install dependencies
        run: |
          sudo apt-get update
          sudo apt-get install -y libeigen3-dev libvtk9-dev libfmt-dev
      - name: Build
        run: |
          mkdir build && cd build
          cmake ..
          make -j$(nproc)
      - name: Test
        run: ./build/sdt_atomic_sim
```

## Further Reading

- [CMake Documentation](https://cmake.org/documentation/)
- [VTK Installation Guide](https://vtk.org/Wiki/VTK/Build)
- [Eigen3 Documentation](https://eigen.tuxfamily.org/)
- [fmt Documentation](https://fmt.dev/)

