import { useEffect, useRef } from 'react';

/**
 * WebGL Hero Animation
 * Renders an animated toroidal vortex field representing the spation medium
 * World-class visual that immediately communicates SDT's core concept
 */
export default function HeroAnimation() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const animationRef = useRef<number>(0);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const gl = canvas.getContext('webgl2') || canvas.getContext('webgl');
    if (!gl) {
      console.warn('WebGL not supported, falling back to CSS animation');
      return;
    }

    // Resize handler
    const resize = () => {
      const dpr = Math.min(window.devicePixelRatio, 2);
      canvas.width = canvas.clientWidth * dpr;
      canvas.height = canvas.clientHeight * dpr;
      gl.viewport(0, 0, canvas.width, canvas.height);
    };
    resize();
    window.addEventListener('resize', resize);

    // Vertex shader - creates a full-screen quad
    const vertexShaderSource = `#version 300 es
      in vec2 a_position;
      out vec2 v_uv;
      void main() {
        v_uv = a_position * 0.5 + 0.5;
        gl_Position = vec4(a_position, 0.0, 1.0);
      }
    `;

    // Fragment shader - animated pressure field visualization
    const fragmentShaderSource = `#version 300 es
      precision highp float;

      in vec2 v_uv;
      out vec4 fragColor;

      uniform float u_time;
      uniform vec2 u_resolution;
      uniform vec2 u_mouse;

      #define PI 3.14159265359
      #define TAU 6.28318530718

      // SDT color palette
      vec3 primaryBlue = vec3(0.145, 0.388, 0.922);
      vec3 accentGold = vec3(0.961, 0.620, 0.043);
      vec3 deepSpace = vec3(0.059, 0.082, 0.165);

      // Smooth noise function
      float hash(vec2 p) {
        return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453123);
      }

      float noise(vec2 p) {
        vec2 i = floor(p);
        vec2 f = fract(p);
        f = f * f * (3.0 - 2.0 * f);

        float a = hash(i);
        float b = hash(i + vec2(1.0, 0.0));
        float c = hash(i + vec2(0.0, 1.0));
        float d = hash(i + vec2(1.0, 1.0));

        return mix(mix(a, b, f.x), mix(c, d, f.x), f.y);
      }

      float fbm(vec2 p) {
        float value = 0.0;
        float amplitude = 0.5;
        float frequency = 1.0;

        for (int i = 0; i < 6; i++) {
          value += amplitude * noise(p * frequency);
          amplitude *= 0.5;
          frequency *= 2.0;
        }
        return value;
      }

      // Toroidal pressure field - SDT's core visual
      float torusField(vec2 uv, vec2 center, float majorR, float minorR, float time) {
        vec2 d = uv - center;
        float dist = length(d);
        float angle = atan(d.y, d.x);

        // Distance to torus surface
        float torusDist = abs(dist - majorR) - minorR;

        // Helical wave pattern along the torus (SDT electron wake)
        float helicalWave = sin(angle * 7.0 + time * 2.0) * 0.5 + 0.5;

        // Pressure falloff
        float pressure = exp(-torusDist * torusDist * 20.0);

        return pressure * (0.7 + 0.3 * helicalWave);
      }

      // Occlusion effect - two bodies creating pressure shadow
      float occlusionField(vec2 uv, float time) {
        vec2 body1 = vec2(0.35 + sin(time * 0.3) * 0.05, 0.5);
        vec2 body2 = vec2(0.65 + cos(time * 0.3) * 0.05, 0.5);

        float r1 = 0.08;
        float r2 = 0.06;

        float d1 = length(uv - body1);
        float d2 = length(uv - body2);

        // Bodies create pressure shadows
        float shadow1 = smoothstep(r1, r1 + 0.1, d1);
        float shadow2 = smoothstep(r2, r2 + 0.08, d2);

        // Combined occlusion effect
        float occlusion = shadow1 * shadow2;

        // Pressure gradient between bodies (the force!)
        vec2 midpoint = (body1 + body2) * 0.5;
        float gradientDist = length(uv - midpoint);
        float gradient = smoothstep(0.2, 0.0, gradientDist);

        return occlusion * (1.0 - gradient * 0.3);
      }

      // Spation lattice background
      float lattice(vec2 uv, float time) {
        vec2 grid = fract(uv * 30.0) - 0.5;
        float dots = smoothstep(0.15, 0.1, length(grid));

        // Subtle wave through lattice
        float wave = sin(uv.x * 20.0 + uv.y * 10.0 + time) * 0.5 + 0.5;

        return dots * wave * 0.15;
      }

      void main() {
        vec2 uv = v_uv;
        float aspect = u_resolution.x / u_resolution.y;
        uv.x *= aspect;

        float time = u_time * 0.5;

        // Background gradient
        vec3 color = mix(deepSpace, deepSpace * 1.5, uv.y);

        // Add spation lattice (subtle)
        float latticeVal = lattice(uv, time);
        color += primaryBlue * latticeVal * 0.3;

        // Multiple pressure wave fronts
        for (int i = 0; i < 3; i++) {
          float phase = float(i) * TAU / 3.0;
          vec2 waveCenter = vec2(0.5 * aspect, 0.5);
          float radius = mod(time * 0.2 + phase, 1.5);
          float wave = exp(-pow(length(uv - waveCenter) - radius, 2.0) * 50.0);
          color += primaryBlue * wave * 0.15;
        }

        // Central toroidal vortex (electron)
        float torus = torusField(uv, vec2(0.5 * aspect, 0.5), 0.15, 0.03, time);
        color += mix(primaryBlue, accentGold, torus * 0.5) * torus * 0.8;

        // Occlusion demonstration
        float occ = occlusionField(vec2(uv.x / aspect, uv.y), time);
        color = mix(color, color * occ, 0.3);

        // Vignette
        float vignette = 1.0 - length(v_uv - 0.5) * 0.8;
        color *= vignette;

        // Subtle noise for texture
        float n = fbm(uv * 3.0 + time * 0.1);
        color += (n - 0.5) * 0.02;

        // Gamma correction
        color = pow(color, vec3(0.9));

        fragColor = vec4(color, 1.0);
      }
    `;

    // Compile shaders
    const compileShader = (type: number, source: string) => {
      const shader = gl.createShader(type);
      if (!shader) return null;
      gl.shaderSource(shader, source);
      gl.compileShader(shader);
      if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
        console.error('Shader compile error:', gl.getShaderInfoLog(shader));
        gl.deleteShader(shader);
        return null;
      }
      return shader;
    };

    const vertexShader = compileShader(gl.VERTEX_SHADER, vertexShaderSource);
    const fragmentShader = compileShader(gl.FRAGMENT_SHADER, fragmentShaderSource);
    if (!vertexShader || !fragmentShader) return;

    // Create program
    const program = gl.createProgram();
    if (!program) return;
    gl.attachShader(program, vertexShader);
    gl.attachShader(program, fragmentShader);
    gl.linkProgram(program);

    if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
      console.error('Program link error:', gl.getProgramInfoLog(program));
      return;
    }

    // Setup geometry (full-screen quad)
    const positions = new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]);
    const positionBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, positions, gl.STATIC_DRAW);

    const positionLocation = gl.getAttribLocation(program, 'a_position');
    const timeLocation = gl.getUniformLocation(program, 'u_time');
    const resolutionLocation = gl.getUniformLocation(program, 'u_resolution');
    const mouseLocation = gl.getUniformLocation(program, 'u_mouse');

    // Mouse tracking
    let mouseX = 0.5, mouseY = 0.5;
    const handleMouse = (e: MouseEvent) => {
      const rect = canvas.getBoundingClientRect();
      mouseX = (e.clientX - rect.left) / rect.width;
      mouseY = 1.0 - (e.clientY - rect.top) / rect.height;
    };
    canvas.addEventListener('mousemove', handleMouse);

    // Animation loop
    const startTime = performance.now();
    const render = () => {
      const time = (performance.now() - startTime) / 1000;

      gl.useProgram(program);
      gl.uniform1f(timeLocation, time);
      gl.uniform2f(resolutionLocation, canvas.width, canvas.height);
      gl.uniform2f(mouseLocation, mouseX, mouseY);

      gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);
      gl.enableVertexAttribArray(positionLocation);
      gl.vertexAttribPointer(positionLocation, 2, gl.FLOAT, false, 0, 0);

      gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);

      animationRef.current = requestAnimationFrame(render);
    };
    render();

    // Cleanup
    return () => {
      cancelAnimationFrame(animationRef.current);
      window.removeEventListener('resize', resize);
      canvas.removeEventListener('mousemove', handleMouse);
      gl.deleteProgram(program);
      gl.deleteShader(vertexShader);
      gl.deleteShader(fragmentShader);
      gl.deleteBuffer(positionBuffer);
    };
  }, []);

  return (
    <canvas
      ref={canvasRef}
      className="absolute inset-0 w-full h-full"
      style={{ background: '#0f172a' }}
    />
  );
}
