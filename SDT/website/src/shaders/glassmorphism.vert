/**
 * Creative Agent: Glassmorphism Vertex Shader
 * 
 * TEKNE: Shader IS the glassmorphism effect
 * All original GLSL code
 */

attribute vec3 position;
attribute vec3 normal;
attribute vec2 uv;

uniform mat4 modelViewMatrix;
uniform mat4 projectionMatrix;
uniform mat3 normalMatrix;

varying vec3 vPosition;
varying vec3 vNormal;
varying vec2 vUv;
varying vec3 vViewPosition;

void main() {
  vPosition = position;
  vNormal = normalize(normalMatrix * normal);
  vUv = uv;
  vViewPosition = (modelViewMatrix * vec4(position, 1.0)).xyz;
  
  gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
}



