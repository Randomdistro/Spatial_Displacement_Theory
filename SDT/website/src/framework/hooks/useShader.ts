/**
 * Codemonkey Agent: React Hook for Shader Management
 * 
 * Convenient hook for Creative Agent to use custom shaders
 */

import { useEffect, useRef, useState } from 'react';
import { useThree } from '@react-three/fiber';
import { shaderRegistry, ShaderSource, CompiledShader, ShaderError } from '../shader/ShaderRegistry';

export interface UseShaderOptions {
  shader: ShaderSource;
  uniforms?: Record<string, any>;
  onError?: (error: ShaderError) => void;
}

export interface UseShaderReturn {
  compiledShader: CompiledShader | null;
  error: ShaderError | null;
  isLoading: boolean;
  updateUniforms: (uniforms: Record<string, any>) => void;
}

/**
 * Hook for using custom shaders
 * 
 * @example
 * ```tsx
 * const { compiledShader } = useShader({
 *   shader: {
 *     vertex: vertexShaderSource,
 *     fragment: fragmentShaderSource,
 *     uniforms: { time: { type: 'float', value: 0 } }
 *   }
 * });
 * ```
 */
export function useShader(options: UseShaderOptions): UseShaderReturn {
  const { gl } = useThree();
  const [compiledShader, setCompiledShader] = useState<CompiledShader | null>(null);
  const [error, setError] = useState<ShaderError | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const shaderNameRef = useRef<string | null>(null);
  const uniformsRef = useRef<Record<string, any>>(options.uniforms || {});

  useEffect(() => {
    if (!gl) return;

    // Initialize registry if needed
    if (!shaderRegistry['gl']) {
      shaderRegistry.initialize(gl);
    }

    // Generate unique name for this shader instance
    const shaderName = `shader-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    shaderNameRef.current = shaderName;

    try {
      // Register shader
      shaderRegistry.register(shaderName, options.shader);

      // Compile shader
      const compiled = shaderRegistry.get(shaderName);
      setCompiledShader(compiled);
      setError(null);
      setIsLoading(false);
    } catch (err) {
      const shaderError = err as ShaderError;
      setError(shaderError);
      setIsLoading(false);
      
      if (options.onError) {
        options.onError(shaderError);
      }
    }

    // Cleanup
    return () => {
      if (shaderNameRef.current) {
        shaderRegistry.dispose(shaderNameRef.current);
      }
    };
  }, [gl, options.shader]);

  const updateUniforms = (newUniforms: Record<string, any>) => {
    uniformsRef.current = { ...uniformsRef.current, ...newUniforms };
  };

  return {
    compiledShader,
    error,
    isLoading,
    updateUniforms,
  };
}

