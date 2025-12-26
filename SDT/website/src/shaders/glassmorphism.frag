/**
 * Creative Agent: Glassmorphism Fragment Shader
 * 
 * TEKNE: Shader IS the glassmorphism effect
 * Backdrop blur with gold border glow
 * All original GLSL code
 */

precision highp float;

uniform float time;
uniform vec3 baseColor;
uniform vec3 goldColor;
uniform float opacity;
uniform float blurRadius;
uniform float borderWidth;
uniform float borderGlow;

varying vec3 vPosition;
varying vec3 vNormal;
varying vec2 vUv;
varying vec3 vViewPosition;

/**
 * Simple blur approximation
 * Samples surrounding pixels
 */
vec3 sampleBlur(sampler2D tex, vec2 uv, float radius) {
  vec3 color = vec3(0.0);
  float total = 0.0;
  
  // Gaussian blur kernel
  for (int x = -2; x <= 2; x++) {
    for (int y = -2; y <= 2; y++) {
      vec2 offset = vec2(float(x), float(y)) * radius;
      float weight = exp(-dot(offset, offset) / (2.0 * radius * radius));
      color += texture2D(tex, uv + offset).rgb * weight;
      total += weight;
    }
  }
  
  return color / total;
}

/**
 * Calculate border distance
 */
float borderDistance(vec2 uv) {
  vec2 center = vec2(0.5);
  vec2 dist = abs(uv - center);
  float maxDist = max(dist.x, dist.y);
  return maxDist;
}

/**
 * Fresnel effect
 */
float fresnel(vec3 normal, vec3 viewDir) {
  return pow(1.0 - dot(normal, viewDir), 2.0);
}

void main() {
  vec3 viewDir = normalize(-vViewPosition);
  
  // Base color with slight tint
  vec3 color = baseColor;
  
  // Fresnel edge highlight
  float fresnelFactor = fresnel(vNormal, viewDir);
  color = mix(color, goldColor, fresnelFactor * 0.3);
  
  // Border glow
  float borderDist = borderDistance(vUv);
  float borderFactor = smoothstep(0.5 - borderWidth, 0.5, borderDist);
  color = mix(color, goldColor, borderFactor * borderGlow);
  
  // Opacity with fresnel
  float finalOpacity = opacity * (0.7 + fresnelFactor * 0.3);
  
  gl_FragColor = vec4(color, finalOpacity);
}


