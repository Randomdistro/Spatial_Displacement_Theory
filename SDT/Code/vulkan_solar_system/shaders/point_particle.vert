#version 450

layout(location = 0) in vec3 inPosition;

layout(location = 0) out vec3 fragPos;
layout(location = 1) out float fragSize;

layout(set = 0, binding = 0) uniform UniformBufferObject {
    mat4 model;
    mat4 view;
    mat4 proj;
    vec3 cameraPos;
    vec3 lightPos;
    float time;
} ubo;

layout(push_constant) uniform PointParticlePushConstants {
    vec3 position;
    float size;
    vec3 color;
} pc;

void main() {
    fragPos = pc.position;
    fragSize = pc.size;
    
    // Transform position to clip space
    vec4 worldPos = vec4(pc.position, 1.0);
    vec4 viewPos = ubo.view * worldPos;
    vec4 clipPos = ubo.proj * viewPos;
    
    // Billboard effect: expand particle size based on distance
    vec3 cameraRight = vec3(ubo.view[0][0], ubo.view[1][0], ubo.view[2][0]);
    vec3 cameraUp = vec3(ubo.view[0][1], ubo.view[1][1], ubo.view[2][1]);
    
    vec3 pos = pc.position;
    pos += (inPosition.x * cameraRight + inPosition.y * cameraUp) * pc.size;
    
    gl_Position = ubo.proj * ubo.view * vec4(pos, 1.0);
    gl_PointSize = pc.size * 500.0 / -viewPos.z; // Scale based on distance
}

