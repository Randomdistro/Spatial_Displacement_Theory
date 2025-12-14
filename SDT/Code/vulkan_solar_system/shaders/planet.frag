#version 450

layout(location = 0) in vec3 fragPos;
layout(location = 1) in vec3 fragNormal;
layout(location = 2) in vec2 fragTexCoord;

layout(location = 0) out vec4 outColor;

layout(set = 0, binding = 0) uniform UniformBufferObject {
    mat4 model;
    mat4 view;
    mat4 proj;
    vec3 cameraPos;
    vec3 lightPos;
    float time;
} ubo;

layout(set = 1, binding = 0) uniform PlanetProperties {
    vec3 color;
    float radius;
    float emissivity;
    float specular;
} planetProps;

void main() {
    vec3 normal = normalize(fragNormal);
    vec3 lightDir = normalize(ubo.lightPos - fragPos);
    vec3 viewDir = normalize(ubo.cameraPos - fragPos);
    
    // Ambient lighting
    float ambient = 0.1;
    
    // Diffuse lighting
    float diff = max(dot(normal, lightDir), 0.0);
    
    // Specular lighting
    vec3 reflectDir = reflect(-lightDir, normal);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), 32.0) * planetProps.specular;
    
    // Combine lighting
    vec3 lighting = vec3(ambient + diff + spec);
    
    // Base color with emissivity
    vec3 finalColor = planetProps.color * lighting + planetProps.color * planetProps.emissivity;
    
    outColor = vec4(finalColor, 1.0);
}

