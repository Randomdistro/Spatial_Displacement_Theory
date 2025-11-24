# Building SDT-Navier C++ Simulator

## Quick Start

```bash
mkdir build
cd build
cmake ..
make
```

## Detailed Build Instructions

### Prerequisites

1. **CMake 3.20+**
   ```bash
   cmake --version  # Check version
   ```

2. **C++20 Compiler**
   - GCC 10+ (Linux/Mac)
   - Clang 12+ (Linux/Mac)
   - MSVC 2019+ (Windows)

3. **Required Dependencies**
   - **Eigen3**: Linear algebra library
     ```bash
     # Ubuntu/Debian
     sudo apt-get install libeigen3-dev
     
     # macOS
     brew install eigen
     
     # Or build from source: https://eigen.tuxfamily.org/
     ```

4. **Optional Dependencies**
   - **HDF5**: For advanced I/O (optional)
     ```bash
     sudo apt-get install libhdf5-dev
     ```
   
   - **pybind11**: For Python bindings (optional)
     ```bash
     pip install pybind11
     # Or
     git clone https://github.com/pybind/pybind11.git
     ```
   
   - **Catch2**: For unit tests (optional)
     ```bash
     git clone https://github.com/catchorg/Catch2.git
     ```

### Build Steps

1. **Create build directory**
   ```bash
   mkdir build
   cd build
   ```

2. **Configure with CMake**
   ```bash
   cmake ..
   ```
   
   Or with specific options:
   ```bash
   cmake -DCMAKE_BUILD_TYPE=Release \
         -DBUILD_PYTHON_BINDINGS=ON \
         -DBUILD_TESTS=ON \
         ..
   ```

3. **Build**
   ```bash
   make -j4  # Use 4 parallel jobs
   ```

4. **Run tests** (if built)
   ```bash
   ctest
   ```

5. **Run executables**
   ```bash
   ./tools/simulate_deuteron
   ```

### Build Options

| Option | Default | Description |
|--------|---------|-------------|
| `CMAKE_BUILD_TYPE` | `Release` | Build type: `Debug`, `Release`, `RelWithDebInfo` |
| `BUILD_PYTHON_BINDINGS` | `ON` | Build Python bindings (requires pybind11) |
| `BUILD_TESTS` | `ON` | Build unit tests (requires Catch2) |
| `BUILD_TOOLS` | `ON` | Build executable tools |

### Troubleshooting

#### Eigen3 not found
```bash
cmake -DEigen3_DIR=/path/to/eigen/share/eigen3/cmake ..
```

#### HDF5 not found
HDF5 is optional. If not found, the build will continue without HDF5 support.

#### Python bindings not building
- Ensure pybind11 is installed: `pip install pybind11`
- Or set `BUILD_PYTHON_BINDINGS=OFF` to skip

#### Tests not building
- Ensure Catch2 is available
- Or set `BUILD_TESTS=OFF` to skip

### Installation

To install the library system-wide:

```bash
cmake -DCMAKE_INSTALL_PREFIX=/usr/local ..
make
sudo make install
```

### Using the Python Bindings

After building with `BUILD_PYTHON_BINDINGS=ON`:

```python
import sys
sys.path.insert(0, '/path/to/build')
import sdt_navier_cpp

# Use the library
fields = sdt_navier_cpp.FieldSystem(50, 50, 50, 0.2e-15, 0.2e-15, 0.2e-15)
```

### Performance Tips

1. **Use Release mode**
   ```bash
   cmake -DCMAKE_BUILD_TYPE=Release ..
   ```

2. **Enable optimizations**
   The CMakeLists.txt already includes `-O3 -march=native` for Release builds.

3. **Use parallel builds**
   ```bash
   make -j$(nproc)  # Use all CPU cores
   ```

### Cross-Platform Notes

#### Windows (MSVC)
```cmd
mkdir build
cd build
cmake .. -G "Visual Studio 16 2019" -A x64
cmake --build . --config Release
```

#### macOS
```bash
# May need to set compiler
export CC=clang
export CXX=clang++
cmake ..
make
```

#### Linux
Standard build process should work. May need to install development packages:
```bash
sudo apt-get install build-essential cmake libeigen3-dev
```

