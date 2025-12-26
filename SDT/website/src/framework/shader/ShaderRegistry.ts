/**
 * Codemonkey Agent: Shader Management System
 * 
 * All original shader management - supports Creative Agent's custom GLSL shaders
 */

export interface ShaderSource {
  vertex: string;
  fragment: string;
  uniforms?: Record<string, UniformDefinition>;
}

export interface UniformDefinition {
  type: 'float' | 'vec2' | 'vec3' | 'vec4' | 'mat3' | 'mat4' | 'sampler2D' | 'samplerCube';
  value: any;
}

export interface CompiledShader {
  program: WebGLProgram;
  uniforms: Map<string, WebGLUniformLocation>;
  attributes: Map<string, number>;
  vertexShader: WebGLShader;
  fragmentShader: WebGLShader;
}

export interface ShaderError {
  message: string;
  shader: string;
  line?: number;
  source?: string;
}

/**
 * Shader Registry
 * Manages all custom shaders
 */
export class ShaderRegistry {
  private shaders: Map<string, ShaderSource> = new Map();
  private compiled: Map<string, CompiledShader> = new Map();
  private gl: WebGLRenderingContext | null = null;

  /**
   * Initialize with WebGL context
   */
  initialize(gl: WebGLRenderingContext): void {
    this.gl = gl;
  }

  /**
   * Register a shader
   */
  register(name: string, shader: ShaderSource): void {
    this.shaders.set(name, shader);
    // Invalidate compiled version if exists
    this.compiled.delete(name);
  }

  /**
   * Get compiled shader
   */
  get(name: string): CompiledShader {
    if (!this.gl) {
      throw new Error('ShaderRegistry not initialized. Call initialize() first.');
    }

    // Check if already compiled
    if (this.compiled.has(name)) {
      return this.compiled.get(name)!;
    }

    const source = this.shaders.get(name);
    if (!source) {
      throw new Error(`Shader "${name}" not found`);
    }

    const compiled = this.compileShader(source, name);
    this.compiled.set(name, compiled);
    return compiled;
  }

  /**
   * Compile shader from source
   */
  private compileShader(source: ShaderSource, name: string): CompiledShader {
    if (!this.gl) {
      throw new Error('WebGL context not available');
    }

    const gl = this.gl;

    // Compile vertex shader
    const vertexShader = this.compileShaderSource(gl.VERTEX_SHADER, source.vertex, name);
    
    // Compile fragment shader
    const fragmentShader = this.compileShaderSource(gl.FRAGMENT_SHADER, source.fragment, name);

    // Create program
    const program = gl.createProgram();
    if (!program) {
      throw new Error('Failed to create shader program');
    }

    gl.attachShader(program, vertexShader);
    gl.attachShader(program, fragmentShader);
    gl.linkProgram(program);

    // Check link status
    if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
      const info = gl.getProgramInfoLog(program);
      gl.deleteProgram(program);
      throw new Error(`Shader program link failed for "${name}": ${info}`);
    }

    // Extract uniforms and attributes
    const uniforms = new Map<string, WebGLUniformLocation>();
    const attributes = new Map<string, number>();

    // Get uniform locations
    const uniformCount = gl.getProgramParameter(program, gl.ACTIVE_UNIFORMS);
    for (let i = 0; i < uniformCount; i++) {
      const info = gl.getActiveUniform(program, i);
      if (info) {
        const location = gl.getUniformLocation(program, info.name);
        if (location) {
          uniforms.set(info.name, location);
        }
      }
    }

    // Get attribute locations
    const attributeCount = gl.getProgramParameter(program, gl.ACTIVE_ATTRIBUTES);
    for (let i = 0; i < attributeCount; i++) {
      const info = gl.getActiveAttribute(program, i);
      if (info) {
        const location = gl.getAttribLocation(program, info.name);
        attributes.set(info.name, location);
      }
    }

    return {
      program,
      uniforms,
      attributes,
      vertexShader,
      fragmentShader,
    };
  }

  /**
   * Compile shader source
   */
  private compileShaderSource(
    type: number,
    source: string,
    name: string
  ): WebGLShader {
    if (!this.gl) {
      throw new Error('WebGL context not available');
    }

    const gl = this.gl;
    const shader = gl.createShader(type);
    
    if (!shader) {
      throw new Error(`Failed to create shader for "${name}"`);
    }

    gl.shaderSource(shader, source);
    gl.compileShader(shader);

    if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
      const info = gl.getShaderInfoLog(shader);
      const error: ShaderError = {
        message: `Shader compilation failed for "${name}": ${info}`,
        shader: name,
        source: source,
      };
      
      // Try to extract line number
      const match = info?.match(/ERROR: \d+:(\d+):/);
      if (match) {
        error.line = parseInt(match[1], 10);
      }

      gl.deleteShader(shader);
      throw error;
    }

    return shader;
  }

  /**
   * Validate shader source
   */
  validate(name: string): { valid: boolean; errors?: ShaderError[] } {
    const source = this.shaders.get(name);
    if (!source) {
      return { valid: false, errors: [{ message: `Shader "${name}" not found`, shader: name }] };
    }

    // Basic validation (could be enhanced)
    const errors: ShaderError[] = [];

    // Check for required uniforms
    if (source.uniforms) {
      // Validate uniform definitions match GLSL types
      // This is a simplified check
    }

    return { valid: errors.length === 0, errors };
  }

  /**
   * Dispose of shader
   */
  dispose(name: string): void {
    const compiled = this.compiled.get(name);
    if (compiled && this.gl) {
      this.gl.deleteProgram(compiled.program);
      this.gl.deleteShader(compiled.vertexShader);
      this.gl.deleteShader(compiled.fragmentShader);
    }
    this.compiled.delete(name);
    this.shaders.delete(name);
  }

  /**
   * Clear all shaders
   */
  clear(): void {
    for (const name of this.compiled.keys()) {
      this.dispose(name);
    }
  }
}

// Global registry instance
export const shaderRegistry = new ShaderRegistry();

