/**
 * Codemonkey Agent: Shader Loader Utility
 * 
 * Loads GLSL shader files for Creative Agent
 * All original implementation
 */

export interface ShaderSource {
  vertex: string;
  fragment: string;
}

/**
 * Load shader from file
 * In production, these would be bundled
 * For now, returns the shader source directly
 */
export async function loadShader(name: string): Promise<ShaderSource> {
  // In a real implementation, this would fetch the shader files
  // For now, we'll use the shader registry or return inline shaders
  
  switch (name) {
    case 'pressure-field':
      return {
        vertex: await loadShaderFile('/shaders/pressureField.vert'),
        fragment: await loadShaderFile('/shaders/pressureField.frag'),
      };
    case 'glassmorphism':
      return {
        vertex: await loadShaderFile('/shaders/glassmorphism.vert'),
        fragment: await loadShaderFile('/shaders/glassmorphism.frag'),
      };
    default:
      throw new Error(`Shader "${name}" not found`);
  }
}

/**
 * Load shader file content
 */
async function loadShaderFile(path: string): Promise<string> {
  try {
    const response = await fetch(path);
    if (!response.ok) {
      throw new Error(`Failed to load shader: ${path}`);
    }
    return await response.text();
  } catch (error) {
    // Fallback: return empty shader (for development)
    console.warn(`Could not load shader file: ${path}. Using fallback.`);
    return getFallbackShader(path);
  }
}

/**
 * Get fallback shader (for development)
 */
function getFallbackShader(path: string): string {
  if (path.includes('pressureField')) {
    return `
      void main() {
        gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
      }
    `;
  }
  return `
    void main() {
      gl_FragColor = vec4(1.0, 0.0, 0.0, 1.0);
    }
  `;
}


