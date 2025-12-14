#version 450

layout(location = 0) in vec3 inPosition;
layout(location = 1) in float inTime; // Time along trail (0.0 to 1.0)
layout(location = 2) in float inAlpha; // Alpha value for fade

layout(location = 0) out vec3 fragPos;
layout(location = 1) out float fragTime;
layout(location = 2) out float fragAlpha;

layout(set = 0, binding = 0) uniform UniformBufferObject {
    mat4 model;
    mat4 view;
    mat4 proj;
    vec3 cameraPos;
    vec3 lightPos;
    float time;
} ubo;

layout(set = 2, binding = 0) uniform TrailProperties {
    vec3 color;
    float width;
    float fadeStart;
    float fadeEnd;
} trailProps;

void main() {
    fragPos = inPosition;
    fragTime = inTime;
    fragAlpha = inAlpha;
    
    gl_Position = ubo.proj * ubo.view * vec4(inPosition, 1.0);
}

