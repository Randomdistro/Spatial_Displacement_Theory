#version 450

layout(location = 0) in vec3 fragPos;
layout(location = 1) in float fragSize;

layout(location = 0) out vec4 outColor;

layout(push_constant) uniform PointParticlePushConstants {
    vec3 position;
    float size;
    vec3 color;
} pc;

void main() {
    // Create circular point with soft edges
    vec2 coord = gl_PointCoord - vec2(0.5);
    float dist = length(coord);
    
    if (dist > 0.5) {
        discard;
    }
    
    // Soft falloff
    float alpha = 1.0 - smoothstep(0.3, 0.5, dist);
    
    // Bright center with falloff
    float brightness = 1.0 - dist * 2.0;
    brightness = max(brightness, 0.3);
    
    outColor = vec4(pc.color * brightness, alpha);
}

