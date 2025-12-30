/**
 * Creative Agent: Pressure Field Fragment Shader
 * 
 * TEKNE: Shader IS the pressure field visualization
 * Volumetric gradient with gold flow lines
 * All original GLSL code
 */

precision highp float;

uniform float time;
uniform float pressureDensity;
uniform vec3 center;
uniform float radius;
uniform vec3 colorDeep;      // Deep Space Blue
uniform vec3 colorMedium;   // Medium Blue
uniform vec3 colorLight;    // Light Blue
uniform vec3 colorGold;     // Metallic Gold

varying vec3 vPosition;
varying vec3 vNormal;
varying vec2 vUv;

/**
 * Calculate distance from center
 */
float distanceFromCenter(vec3 pos) {
  return length(pos - center);
}

/**
 * Calculate pressure gradient
 * Higher pressure at center, lower at edges
 */
float calculatePressure(vec3 pos) {
  float dist = distanceFromCenter(pos);
  float normalizedDist = clamp(dist / radius, 0.0, 1.0);
  
  // Pressure decreases from center to edge
  // Using exponential falloff for natural feel
  return exp(-normalizedDist * 2.0) * pressureDensity;
}

/**
 * Calculate color based on pressure
 */
vec3 pressureColor(float pressure) {
  // Gradient: deep blue → medium → light blue
  if (pressure > 0.7) {
    return mix(colorMedium, colorDeep, (pressure - 0.7) / 0.3);
  } else if (pressure > 0.3) {
    return mix(colorLight, colorMedium, (pressure - 0.3) / 0.4);
  } else {
    return colorLight;
  }
}

/**
 * Calculate flow lines (gold)
 * Creates radial flow pattern
 */
float flowLines(vec3 pos) {
  vec3 dir = normalize(pos - center);
  
  // Radial flow pattern
  float angle = atan(dir.z, dir.x);
  float flow = sin(angle * 6.0 + time * 2.0) * 0.5 + 0.5;
  
  // Distance-based intensity
  float dist = distanceFromCenter(pos);
  float distFactor = 1.0 - clamp(dist / radius, 0.0, 1.0);
  
  return flow * distFactor * 0.3;
}

/**
 * Fresnel effect for edge glow
 */
float fresnel(vec3 normal, vec3 viewDir) {
  return pow(1.0 - dot(normal, viewDir), 2.0);
}

void main() {
  // Calculate pressure at this position
  float pressure = calculatePressure(vPosition);
  
  // Base color from pressure gradient
  vec3 color = pressureColor(pressure);
  
  // Add gold flow lines
  float flow = flowLines(vPosition);
  color = mix(color, colorGold, flow);
  
  // Fresnel edge glow (gold)
  vec3 viewDir = normalize(-vPosition);
  float fresnelFactor = fresnel(vNormal, viewDir);
  color = mix(color, colorGold, fresnelFactor * 0.2);
  
  // Emissive intensity based on pressure
  float emissive = pressure * 0.2 + flow * 0.3;
  
  // Opacity based on pressure and distance
  float opacity = pressure * 0.3 + fresnelFactor * 0.1;
  
  gl_FragColor = vec4(color, opacity);
  
  // Emissive component (for bloom)
  gl_FragColor.rgb += color * emissive;
}



