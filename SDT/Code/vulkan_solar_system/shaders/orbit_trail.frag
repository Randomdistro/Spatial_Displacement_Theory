#version 450

layout(location = 0) in vec3 fragPos;
layout(location = 1) in float fragTime;
layout(location = 2) in float fragAlpha;

layout(location = 0) out vec4 outColor;

layout(set = 2, binding = 0) uniform TrailProperties {
    vec3 color;
    float width;
    float fadeStart;
    float fadeEnd;
} trailProps;

void main() {
    // Fade based on time along trail (fade older parts)
    float timeFade = 1.0;
    if (fragTime < trailProps.fadeStart) {
        timeFade = fragTime / trailProps.fadeStart;
    } else if (fragTime > trailProps.fadeEnd) {
        timeFade = 1.0 - (fragTime - trailProps.fadeEnd) / (1.0 - trailProps.fadeEnd);
    }
    
    // Combine with vertex alpha
    float finalAlpha = fragAlpha * timeFade;
    
    // Brightness based on position (brighter at edges for glow effect)
    vec3 color = trailProps.color;
    
    outColor = vec4(color, finalAlpha);
}

