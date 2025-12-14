@echo off
REM Compile GLSL shaders to SPIR-V using glslc (from Vulkan SDK)

set SHADER_DIR=shaders
set OUTPUT_DIR=shaders\spv

REM Create output directory if it doesn't exist
if not exist "%OUTPUT_DIR%" mkdir "%OUTPUT_DIR%"

REM Check if glslc is available
where glslc >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Error: glslc not found. Please install Vulkan SDK.
    exit /b 1
)

REM Compile vertex shaders
echo Compiling vertex shaders...
glslc "%SHADER_DIR%\planet.vert" -o "%OUTPUT_DIR%\planet.vert.spv"
glslc "%SHADER_DIR%\point_particle.vert" -o "%OUTPUT_DIR%\point_particle.vert.spv"
glslc "%SHADER_DIR%\orbit_trail.vert" -o "%OUTPUT_DIR%\orbit_trail.vert.spv"

REM Compile fragment shaders
echo Compiling fragment shaders...
glslc "%SHADER_DIR%\planet.frag" -o "%OUTPUT_DIR%\planet.frag.spv"
glslc "%SHADER_DIR%\point_particle.frag" -o "%OUTPUT_DIR%\point_particle.frag.spv"
glslc "%SHADER_DIR%\orbit_trail.frag" -o "%OUTPUT_DIR%\orbit_trail.frag.spv"

echo Shader compilation complete!

