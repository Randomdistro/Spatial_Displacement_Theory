#pragma once

#include <vulkan/vulkan.h>
#include <vector>
#include <string>
#include <memory>

namespace sdt::vulkan {

struct PipelineConfig {
    VkPipelineLayout pipelineLayout = VK_NULL_HANDLE;
    VkRenderPass renderPass = VK_NULL_HANDLE;
    uint32_t subpass = 0;
    VkPrimitiveTopology topology = VK_PRIMITIVE_TOPOLOGY_TRIANGLE_LIST;
    bool depthTest = true;
    bool depthWrite = true;
    bool blendEnable = false;
    VkBlendFactor srcColorBlendFactor = VK_BLEND_FACTOR_ONE;
    VkBlendFactor dstColorBlendFactor = VK_BLEND_FACTOR_ZERO;
    VkBlendOp colorBlendOp = VK_BLEND_OP_ADD;
    VkBlendFactor srcAlphaBlendFactor = VK_BLEND_FACTOR_ONE;
    VkBlendFactor dstAlphaBlendFactor = VK_BLEND_FACTOR_ZERO;
    VkBlendOp alphaBlendOp = VK_BLEND_OP_ADD;
    VkCullModeFlags cullMode = VK_CULL_MODE_BACK_BIT;
    VkFrontFace frontFace = VK_FRONT_FACE_COUNTER_CLOCKWISE;
    float lineWidth = 1.0f;
    std::vector<VkVertexInputBindingDescription> vertexBindings;
    std::vector<VkVertexInputAttributeDescription> vertexAttributes;
};

class VulkanPipelineBuilder {
public:
    VulkanPipelineBuilder(VkDevice device);
    ~VulkanPipelineBuilder();

    // Load shader from file
    VkShaderModule loadShader(const std::string& filename);
    
    // Create shader module from SPIR-V code
    VkShaderModule createShaderModule(const std::vector<uint32_t>& code);
    
    // Build pipeline
    VkPipeline buildPipeline(const PipelineConfig& config,
                           const std::vector<VkShaderModule>& shaderModules,
                           const std::vector<VkPipelineShaderStageCreateInfo>& shaderStages);

private:
    VkDevice device_;
    
    std::vector<uint32_t> readFile(const std::string& filename);
};

class PipelineManager {
public:
    PipelineManager(VkDevice device, VkRenderPass renderPass);
    ~PipelineManager();

    // Initialize all pipelines
    void initializePipelines();
    
    // Get pipeline handles
    VkPipeline getPlanetPipeline() const { return planetPipeline_; }
    VkPipeline getPointParticlePipeline() const { return pointParticlePipeline_; }
    VkPipeline getOrbitTrailPipeline() const { return orbitTrailPipeline_; }
    
    // Get pipeline layouts
    VkPipelineLayout getPlanetPipelineLayout() const { return planetPipelineLayout_; }
    VkPipelineLayout getPointParticlePipelineLayout() const { return pointParticlePipelineLayout_; }
    VkPipelineLayout getOrbitTrailPipelineLayout() const { return orbitTrailPipelineLayout_; }
    
    // Cleanup
    void cleanup();

private:
    VkDevice device_;
    VkRenderPass renderPass_;
    
    VulkanPipelineBuilder pipelineBuilder_;
    
    // Planet pipeline
    VkPipeline planetPipeline_ = VK_NULL_HANDLE;
    VkPipelineLayout planetPipelineLayout_ = VK_NULL_HANDLE;
    
    // Point particle pipeline
    VkPipeline pointParticlePipeline_ = VK_NULL_HANDLE;
    VkPipelineLayout pointParticlePipelineLayout_ = VK_NULL_HANDLE;
    
    // Orbit trail pipeline
    VkPipeline orbitTrailPipeline_ = VK_NULL_HANDLE;
    VkPipelineLayout orbitTrailPipelineLayout_ = VK_NULL_HANDLE;
    
    // Descriptor set layouts
    VkDescriptorSetLayout uniformDescriptorSetLayout_ = VK_NULL_HANDLE;
    VkDescriptorSetLayout planetPropertiesDescriptorSetLayout_ = VK_NULL_HANDLE;
    VkDescriptorSetLayout trailPropertiesDescriptorSetLayout_ = VK_NULL_HANDLE;
    
    void createDescriptorSetLayouts();
    void createPlanetPipeline();
    void createPointParticlePipeline();
    void createOrbitTrailPipeline();
    
    VkPipelineLayout createPipelineLayout(const std::vector<VkDescriptorSetLayout>& layouts,
                                         const std::vector<VkPushConstantRange>& pushConstants);
};

} // namespace sdt::vulkan

