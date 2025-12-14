#include "vulkan_pipelines.hpp"
#include <fstream>
#include <iostream>
#include <stdexcept>

namespace sdt::vulkan {

VulkanPipelineBuilder::VulkanPipelineBuilder(VkDevice device) : device_(device) {}

VulkanPipelineBuilder::~VulkanPipelineBuilder() {}

std::vector<uint32_t> VulkanPipelineBuilder::readFile(const std::string& filename) {
    std::ifstream file(filename, std::ios::ate | std::ios::binary);
    
    if (!file.is_open()) {
        throw std::runtime_error("Failed to open file: " + filename);
    }
    
    size_t fileSize = static_cast<size_t>(file.tellg());
    std::vector<uint32_t> buffer(fileSize / sizeof(uint32_t));
    
    file.seekg(0);
    file.read(reinterpret_cast<char*>(buffer.data()), fileSize);
    file.close();
    
    return buffer;
}

VkShaderModule VulkanPipelineBuilder::loadShader(const std::string& filename) {
    auto code = readFile(filename);
    return createShaderModule(code);
}

VkShaderModule VulkanPipelineBuilder::createShaderModule(const std::vector<uint32_t>& code) {
    VkShaderModuleCreateInfo createInfo{};
    createInfo.sType = VK_STRUCTURE_TYPE_SHADER_MODULE_CREATE_INFO;
    createInfo.codeSize = code.size() * sizeof(uint32_t);
    createInfo.pCode = code.data();
    
    VkShaderModule shaderModule;
    if (vkCreateShaderModule(device_, &createInfo, nullptr, &shaderModule) != VK_SUCCESS) {
        throw std::runtime_error("Failed to create shader module");
    }
    
    return shaderModule;
}

VkPipeline VulkanPipelineBuilder::buildPipeline(
    const PipelineConfig& config,
    const std::vector<VkShaderModule>& shaderModules,
    const std::vector<VkPipelineShaderStageCreateInfo>& shaderStages) {
    
    // Vertex input state
    VkPipelineVertexInputStateCreateInfo vertexInputInfo{};
    vertexInputInfo.sType = VK_STRUCTURE_TYPE_PIPELINE_VERTEX_INPUT_STATE_CREATE_INFO;
    vertexInputInfo.vertexBindingDescriptionCount = static_cast<uint32_t>(config.vertexBindings.size());
    vertexInputInfo.pVertexBindingDescriptions = config.vertexBindings.data();
    vertexInputInfo.vertexAttributeDescriptionCount = static_cast<uint32_t>(config.vertexAttributes.size());
    vertexInputInfo.pVertexAttributeDescriptions = config.vertexAttributes.data();
    
    // Input assembly
    VkPipelineInputAssemblyStateCreateInfo inputAssembly{};
    inputAssembly.sType = VK_STRUCTURE_TYPE_PIPELINE_INPUT_ASSEMBLY_STATE_CREATE_INFO;
    inputAssembly.topology = config.topology;
    inputAssembly.primitiveRestartEnable = VK_FALSE;
    
    // Viewport and scissor
    VkViewport viewport{};
    viewport.x = 0.0f;
    viewport.y = 0.0f;
    viewport.width = 1920.0f; // Will be set dynamically
    viewport.height = 1080.0f;
    viewport.minDepth = 0.0f;
    viewport.maxDepth = 1.0f;
    
    VkRect2D scissor{};
    scissor.offset = {0, 0};
    scissor.extent = {1920, 1080};
    
    VkPipelineViewportStateCreateInfo viewportState{};
    viewportState.sType = VK_STRUCTURE_TYPE_PIPELINE_VIEWPORT_STATE_CREATE_INFO;
    viewportState.viewportCount = 1;
    viewportState.pViewports = &viewport;
    viewportState.scissorCount = 1;
    viewportState.pScissors = &scissor;
    
    // Rasterization
    VkPipelineRasterizationStateCreateInfo rasterizer{};
    rasterizer.sType = VK_STRUCTURE_TYPE_PIPELINE_RASTERIZATION_STATE_CREATE_INFO;
    rasterizer.depthClampEnable = VK_FALSE;
    rasterizer.rasterizerDiscardEnable = VK_FALSE;
    rasterizer.polygonMode = VK_POLYGON_MODE_FILL;
    rasterizer.lineWidth = config.lineWidth;
    rasterizer.cullMode = config.cullMode;
    rasterizer.frontFace = config.frontFace;
    rasterizer.depthBiasEnable = VK_FALSE;
    
    // Multisampling
    VkPipelineMultisampleStateCreateInfo multisampling{};
    multisampling.sType = VK_STRUCTURE_TYPE_PIPELINE_MULTISAMPLE_STATE_CREATE_INFO;
    multisampling.sampleShadingEnable = VK_FALSE;
    multisampling.rasterizationSamples = VK_SAMPLE_COUNT_1_BIT;
    
    // Depth stencil
    VkPipelineDepthStencilStateCreateInfo depthStencil{};
    depthStencil.sType = VK_STRUCTURE_TYPE_PIPELINE_DEPTH_STENCIL_STATE_CREATE_INFO;
    depthStencil.depthTestEnable = config.depthTest ? VK_TRUE : VK_FALSE;
    depthStencil.depthWriteEnable = config.depthWrite ? VK_TRUE : VK_FALSE;
    depthStencil.depthCompareOp = VK_COMPARE_OP_LESS;
    depthStencil.depthBoundsTestEnable = VK_FALSE;
    depthStencil.stencilTestEnable = VK_FALSE;
    
    // Color blending
    VkPipelineColorBlendAttachmentState colorBlendAttachment{};
    colorBlendAttachment.colorWriteMask = VK_COLOR_COMPONENT_R_BIT | VK_COLOR_COMPONENT_G_BIT |
                                         VK_COLOR_COMPONENT_B_BIT | VK_COLOR_COMPONENT_A_BIT;
    colorBlendAttachment.blendEnable = config.blendEnable ? VK_TRUE : VK_FALSE;
    colorBlendAttachment.srcColorBlendFactor = config.srcColorBlendFactor;
    colorBlendAttachment.dstColorBlendFactor = config.dstColorBlendFactor;
    colorBlendAttachment.colorBlendOp = config.colorBlendOp;
    colorBlendAttachment.srcAlphaBlendFactor = config.srcAlphaBlendFactor;
    colorBlendAttachment.dstAlphaBlendFactor = config.dstAlphaBlendFactor;
    colorBlendAttachment.alphaBlendOp = config.alphaBlendOp;
    
    VkPipelineColorBlendStateCreateInfo colorBlending{};
    colorBlending.sType = VK_STRUCTURE_TYPE_PIPELINE_COLOR_BLEND_STATE_CREATE_INFO;
    colorBlending.logicOpEnable = VK_FALSE;
    colorBlending.attachmentCount = 1;
    colorBlending.pAttachments = &colorBlendAttachment;
    
    // Dynamic state
    std::vector<VkDynamicState> dynamicStates = {
        VK_DYNAMIC_STATE_VIEWPORT,
        VK_DYNAMIC_STATE_SCISSOR
    };
    
    VkPipelineDynamicStateCreateInfo dynamicState{};
    dynamicState.sType = VK_STRUCTURE_TYPE_PIPELINE_DYNAMIC_STATE_CREATE_INFO;
    dynamicState.dynamicStateCount = static_cast<uint32_t>(dynamicStates.size());
    dynamicState.pDynamicStates = dynamicStates.data();
    
    // Pipeline creation
    VkGraphicsPipelineCreateInfo pipelineInfo{};
    pipelineInfo.sType = VK_STRUCTURE_TYPE_GRAPHICS_PIPELINE_CREATE_INFO;
    pipelineInfo.stageCount = static_cast<uint32_t>(shaderStages.size());
    pipelineInfo.pStages = shaderStages.data();
    pipelineInfo.pVertexInputState = &vertexInputInfo;
    pipelineInfo.pInputAssemblyState = &inputAssembly;
    pipelineInfo.pViewportState = &viewportState;
    pipelineInfo.pRasterizationState = &rasterizer;
    pipelineInfo.pMultisampleState = &multisampling;
    pipelineInfo.pDepthStencilState = &depthStencil;
    pipelineInfo.pColorBlendState = &colorBlending;
    pipelineInfo.pDynamicState = &dynamicState;
    pipelineInfo.layout = config.pipelineLayout;
    pipelineInfo.renderPass = config.renderPass;
    pipelineInfo.subpass = config.subpass;
    pipelineInfo.basePipelineHandle = VK_NULL_HANDLE;
    
    VkPipeline pipeline;
    if (vkCreateGraphicsPipelines(device_, VK_NULL_HANDLE, 1, &pipelineInfo, nullptr, &pipeline) != VK_SUCCESS) {
        throw std::runtime_error("Failed to create graphics pipeline");
    }
    
    return pipeline;
}

PipelineManager::PipelineManager(VkDevice device, VkRenderPass renderPass)
    : device_(device), renderPass_(renderPass), pipelineBuilder_(device) {}

PipelineManager::~PipelineManager() {
    cleanup();
}

void PipelineManager::createDescriptorSetLayouts() {
    // Uniform buffer descriptor set layout (set 0)
    VkDescriptorSetLayoutBinding uboLayoutBinding{};
    uboLayoutBinding.binding = 0;
    uboLayoutBinding.descriptorType = VK_DESCRIPTOR_TYPE_UNIFORM_BUFFER;
    uboLayoutBinding.descriptorCount = 1;
    uboLayoutBinding.stageFlags = VK_SHADER_STAGE_VERTEX_BIT | VK_SHADER_STAGE_FRAGMENT_BIT;
    uboLayoutBinding.pImmutableSamplers = nullptr;
    
    VkDescriptorSetLayoutCreateInfo layoutInfo{};
    layoutInfo.sType = VK_STRUCTURE_TYPE_DESCRIPTOR_SET_LAYOUT_CREATE_INFO;
    layoutInfo.bindingCount = 1;
    layoutInfo.pBindings = &uboLayoutBinding;
    
    if (vkCreateDescriptorSetLayout(device_, &layoutInfo, nullptr, &uniformDescriptorSetLayout_) != VK_SUCCESS) {
        throw std::runtime_error("Failed to create uniform descriptor set layout");
    }
    
    // Planet properties descriptor set layout (set 1)
    VkDescriptorSetLayoutBinding planetPropsBinding{};
    planetPropsBinding.binding = 0;
    planetPropsBinding.descriptorType = VK_DESCRIPTOR_TYPE_UNIFORM_BUFFER;
    planetPropsBinding.descriptorCount = 1;
    planetPropsBinding.stageFlags = VK_SHADER_STAGE_FRAGMENT_BIT;
    
    layoutInfo.bindingCount = 1;
    layoutInfo.pBindings = &planetPropsBinding;
    
    if (vkCreateDescriptorSetLayout(device_, &layoutInfo, nullptr, &planetPropertiesDescriptorSetLayout_) != VK_SUCCESS) {
        throw std::runtime_error("Failed to create planet properties descriptor set layout");
    }
    
    // Trail properties descriptor set layout (set 2)
    VkDescriptorSetLayoutBinding trailPropsBinding{};
    trailPropsBinding.binding = 0;
    trailPropsBinding.descriptorType = VK_DESCRIPTOR_TYPE_UNIFORM_BUFFER;
    trailPropsBinding.descriptorCount = 1;
    trailPropsBinding.stageFlags = VK_SHADER_STAGE_FRAGMENT_BIT;
    
    layoutInfo.pBindings = &trailPropsBinding;
    
    if (vkCreateDescriptorSetLayout(device_, &layoutInfo, nullptr, &trailPropertiesDescriptorSetLayout_) != VK_SUCCESS) {
        throw std::runtime_error("Failed to create trail properties descriptor set layout");
    }
}

void PipelineManager::createPlanetPipeline() {
    // Load shaders
    VkShaderModule vertShader = pipelineBuilder_.loadShader("shaders/spv/planet.vert.spv");
    VkShaderModule fragShader = pipelineBuilder_.loadShader("shaders/spv/planet.frag.spv");
    
    VkPipelineShaderStageCreateInfo vertShaderStageInfo{};
    vertShaderStageInfo.sType = VK_STRUCTURE_TYPE_PIPELINE_SHADER_STAGE_CREATE_INFO;
    vertShaderStageInfo.stage = VK_SHADER_STAGE_VERTEX_BIT;
    vertShaderStageInfo.module = vertShader;
    vertShaderStageInfo.pName = "main";
    
    VkPipelineShaderStageCreateInfo fragShaderStageInfo{};
    fragShaderStageInfo.sType = VK_STRUCTURE_TYPE_PIPELINE_SHADER_STAGE_CREATE_INFO;
    fragShaderStageInfo.stage = VK_SHADER_STAGE_FRAGMENT_BIT;
    fragShaderStageInfo.module = fragShader;
    fragShaderStageInfo.pName = "main";
    
    std::vector<VkPipelineShaderStageCreateInfo> shaderStages = {vertShaderStageInfo, fragShaderStageInfo};
    
    // Create pipeline layout
    std::vector<VkDescriptorSetLayout> layouts = {
        uniformDescriptorSetLayout_,
        planetPropertiesDescriptorSetLayout_
    };
    
    planetPipelineLayout_ = createPipelineLayout(layouts, {});
    
    // Vertex input: position(3), normal(3), texCoord(2)
    VkVertexInputBindingDescription bindingDescription{};
    bindingDescription.binding = 0;
    bindingDescription.stride = sizeof(float) * 8; // 3 pos + 3 normal + 2 tex
    bindingDescription.inputRate = VK_VERTEX_INPUT_RATE_VERTEX;
    
    std::vector<VkVertexInputAttributeDescription> attributes(3);
    attributes[0].binding = 0;
    attributes[0].location = 0;
    attributes[0].format = VK_FORMAT_R32G32B32_SFLOAT;
    attributes[0].offset = 0;
    
    attributes[1].binding = 0;
    attributes[1].location = 1;
    attributes[1].format = VK_FORMAT_R32G32B32_SFLOAT;
    attributes[1].offset = sizeof(float) * 3;
    
    attributes[2].binding = 0;
    attributes[2].location = 2;
    attributes[2].format = VK_FORMAT_R32G32_SFLOAT;
    attributes[2].offset = sizeof(float) * 6;
    
    // Configure pipeline
    PipelineConfig config;
    config.pipelineLayout = planetPipelineLayout_;
    config.renderPass = renderPass_;
    config.topology = VK_PRIMITIVE_TOPOLOGY_TRIANGLE_LIST;
    config.depthTest = true;
    config.depthWrite = true;
    config.blendEnable = false;
    config.cullMode = VK_CULL_MODE_BACK_BIT;
    config.vertexBindings = {bindingDescription};
    config.vertexAttributes = attributes;
    
    planetPipeline_ = pipelineBuilder_.buildPipeline(config, {vertShader, fragShader}, shaderStages);
    
    // Cleanup shader modules
    vkDestroyShaderModule(device_, fragShader, nullptr);
    vkDestroyShaderModule(device_, vertShader, nullptr);
}

void PipelineManager::createPointParticlePipeline() {
    // Load shaders
    VkShaderModule vertShader = pipelineBuilder_.loadShader("shaders/spv/point_particle.vert.spv");
    VkShaderModule fragShader = pipelineBuilder_.loadShader("shaders/spv/point_particle.frag.spv");
    
    VkPipelineShaderStageCreateInfo vertShaderStageInfo{};
    vertShaderStageInfo.sType = VK_STRUCTURE_TYPE_PIPELINE_SHADER_STAGE_CREATE_INFO;
    vertShaderStageInfo.stage = VK_SHADER_STAGE_VERTEX_BIT;
    vertShaderStageInfo.module = vertShader;
    vertShaderStageInfo.pName = "main";
    
    VkPipelineShaderStageCreateInfo fragShaderStageInfo{};
    fragShaderStageInfo.sType = VK_STRUCTURE_TYPE_PIPELINE_SHADER_STAGE_CREATE_INFO;
    fragShaderStageInfo.stage = VK_SHADER_STAGE_FRAGMENT_BIT;
    fragShaderStageInfo.module = fragShader;
    fragShaderStageInfo.pName = "main";
    
    std::vector<VkPipelineShaderStageCreateInfo> shaderStages = {vertShaderStageInfo, fragShaderStageInfo};
    
    // Create pipeline layout with push constants
    VkPushConstantRange pushConstantRange{};
    pushConstantRange.stageFlags = VK_SHADER_STAGE_VERTEX_BIT | VK_SHADER_STAGE_FRAGMENT_BIT;
    pushConstantRange.offset = 0;
    pushConstantRange.size = sizeof(float) * 7; // position(3) + size(1) + color(3)
    
    std::vector<VkDescriptorSetLayout> layouts = {uniformDescriptorSetLayout_};
    
    pointParticlePipelineLayout_ = createPipelineLayout(layouts, {pushConstantRange});
    
    // Vertex input: position(3) for billboard quad
    VkVertexInputBindingDescription bindingDescription{};
    bindingDescription.binding = 0;
    bindingDescription.stride = sizeof(float) * 3;
    bindingDescription.inputRate = VK_VERTEX_INPUT_RATE_VERTEX;
    
    VkVertexInputAttributeDescription attribute{};
    attribute.binding = 0;
    attribute.location = 0;
    attribute.format = VK_FORMAT_R32G32B32_SFLOAT;
    attribute.offset = 0;
    
    // Configure pipeline
    PipelineConfig config;
    config.pipelineLayout = pointParticlePipelineLayout_;
    config.renderPass = renderPass_;
    config.topology = VK_PRIMITIVE_TOPOLOGY_POINT_LIST;
    config.depthTest = true;
    config.depthWrite = false;
    config.blendEnable = true;
    config.srcColorBlendFactor = VK_BLEND_FACTOR_SRC_ALPHA;
    config.dstColorBlendFactor = VK_BLEND_FACTOR_ONE_MINUS_SRC_ALPHA;
    config.colorBlendOp = VK_BLEND_OP_ADD;
    config.srcAlphaBlendFactor = VK_BLEND_FACTOR_ONE;
    config.dstAlphaBlendFactor = VK_BLEND_FACTOR_ONE_MINUS_SRC_ALPHA;
    config.cullMode = VK_CULL_MODE_NONE;
    config.vertexBindings = {bindingDescription};
    config.vertexAttributes = {attribute};
    
    pointParticlePipeline_ = pipelineBuilder_.buildPipeline(config, {vertShader, fragShader}, shaderStages);
    
    // Cleanup shader modules
    vkDestroyShaderModule(device_, fragShader, nullptr);
    vkDestroyShaderModule(device_, vertShader, nullptr);
}

void PipelineManager::createOrbitTrailPipeline() {
    // Load shaders
    VkShaderModule vertShader = pipelineBuilder_.loadShader("shaders/spv/orbit_trail.vert.spv");
    VkShaderModule fragShader = pipelineBuilder_.loadShader("shaders/spv/orbit_trail.frag.spv");
    
    VkPipelineShaderStageCreateInfo vertShaderStageInfo{};
    vertShaderStageInfo.sType = VK_STRUCTURE_TYPE_PIPELINE_SHADER_STAGE_CREATE_INFO;
    vertShaderStageInfo.stage = VK_SHADER_STAGE_VERTEX_BIT;
    vertShaderStageInfo.module = vertShader;
    vertShaderStageInfo.pName = "main";
    
    VkPipelineShaderStageCreateInfo fragShaderStageInfo{};
    fragShaderStageInfo.sType = VK_STRUCTURE_TYPE_PIPELINE_SHADER_STAGE_CREATE_INFO;
    fragShaderStageInfo.stage = VK_SHADER_STAGE_FRAGMENT_BIT;
    fragShaderStageInfo.module = fragShader;
    fragShaderStageInfo.pName = "main";
    
    std::vector<VkPipelineShaderStageCreateInfo> shaderStages = {vertShaderStageInfo, fragShaderStageInfo};
    
    // Create pipeline layout
    std::vector<VkDescriptorSetLayout> layouts = {
        uniformDescriptorSetLayout_,
        trailPropertiesDescriptorSetLayout_
    };
    
    orbitTrailPipelineLayout_ = createPipelineLayout(layouts, {});
    
    // Vertex input: position(3), time(1), alpha(1)
    VkVertexInputBindingDescription bindingDescription{};
    bindingDescription.binding = 0;
    bindingDescription.stride = sizeof(float) * 5; // 3 pos + 1 time + 1 alpha
    bindingDescription.inputRate = VK_VERTEX_INPUT_RATE_VERTEX;
    
    std::vector<VkVertexInputAttributeDescription> attributes(3);
    attributes[0].binding = 0;
    attributes[0].location = 0;
    attributes[0].format = VK_FORMAT_R32G32B32_SFLOAT;
    attributes[0].offset = 0;
    
    attributes[1].binding = 0;
    attributes[1].location = 1;
    attributes[1].format = VK_FORMAT_R32_SFLOAT;
    attributes[1].offset = sizeof(float) * 3;
    
    attributes[2].binding = 0;
    attributes[2].location = 2;
    attributes[2].format = VK_FORMAT_R32_SFLOAT;
    attributes[2].offset = sizeof(float) * 4;
    
    // Configure pipeline
    PipelineConfig config;
    config.pipelineLayout = orbitTrailPipelineLayout_;
    config.renderPass = renderPass_;
    config.topology = VK_PRIMITIVE_TOPOLOGY_LINE_STRIP;
    config.depthTest = true;
    config.depthWrite = false;
    config.blendEnable = true;
    config.srcColorBlendFactor = VK_BLEND_FACTOR_SRC_ALPHA;
    config.dstColorBlendFactor = VK_BLEND_FACTOR_ONE_MINUS_SRC_ALPHA;
    config.colorBlendOp = VK_BLEND_OP_ADD;
    config.srcAlphaBlendFactor = VK_BLEND_FACTOR_ONE;
    config.dstAlphaBlendFactor = VK_BLEND_FACTOR_ONE_MINUS_SRC_ALPHA;
    config.cullMode = VK_CULL_MODE_NONE;
    config.lineWidth = 2.0f;
    config.vertexBindings = {bindingDescription};
    config.vertexAttributes = attributes;
    
    orbitTrailPipeline_ = pipelineBuilder_.buildPipeline(config, {vertShader, fragShader}, shaderStages);
    
    // Cleanup shader modules
    vkDestroyShaderModule(device_, fragShader, nullptr);
    vkDestroyShaderModule(device_, vertShader, nullptr);
}

VkPipelineLayout PipelineManager::createPipelineLayout(
    const std::vector<VkDescriptorSetLayout>& layouts,
    const std::vector<VkPushConstantRange>& pushConstants) {
    
    VkPipelineLayoutCreateInfo pipelineLayoutInfo{};
    pipelineLayoutInfo.sType = VK_STRUCTURE_TYPE_PIPELINE_LAYOUT_CREATE_INFO;
    pipelineLayoutInfo.setLayoutCount = static_cast<uint32_t>(layouts.size());
    pipelineLayoutInfo.pSetLayouts = layouts.data();
    pipelineLayoutInfo.pushConstantRangeCount = static_cast<uint32_t>(pushConstants.size());
    pipelineLayoutInfo.pPushConstantRanges = pushConstants.data();
    
    VkPipelineLayout pipelineLayout;
    if (vkCreatePipelineLayout(device_, &pipelineLayoutInfo, nullptr, &pipelineLayout) != VK_SUCCESS) {
        throw std::runtime_error("Failed to create pipeline layout");
    }
    
    return pipelineLayout;
}

void PipelineManager::initializePipelines() {
    createDescriptorSetLayouts();
    createPlanetPipeline();
    createPointParticlePipeline();
    createOrbitTrailPipeline();
}

void PipelineManager::cleanup() {
    if (orbitTrailPipeline_ != VK_NULL_HANDLE) {
        vkDestroyPipeline(device_, orbitTrailPipeline_, nullptr);
        orbitTrailPipeline_ = VK_NULL_HANDLE;
    }
    
    if (pointParticlePipeline_ != VK_NULL_HANDLE) {
        vkDestroyPipeline(device_, pointParticlePipeline_, nullptr);
        pointParticlePipeline_ = VK_NULL_HANDLE;
    }
    
    if (planetPipeline_ != VK_NULL_HANDLE) {
        vkDestroyPipeline(device_, planetPipeline_, nullptr);
        planetPipeline_ = VK_NULL_HANDLE;
    }
    
    if (orbitTrailPipelineLayout_ != VK_NULL_HANDLE) {
        vkDestroyPipelineLayout(device_, orbitTrailPipelineLayout_, nullptr);
        orbitTrailPipelineLayout_ = VK_NULL_HANDLE;
    }
    
    if (pointParticlePipelineLayout_ != VK_NULL_HANDLE) {
        vkDestroyPipelineLayout(device_, pointParticlePipelineLayout_, nullptr);
        pointParticlePipelineLayout_ = VK_NULL_HANDLE;
    }
    
    if (planetPipelineLayout_ != VK_NULL_HANDLE) {
        vkDestroyPipelineLayout(device_, planetPipelineLayout_, nullptr);
        planetPipelineLayout_ = VK_NULL_HANDLE;
    }
    
    if (trailPropertiesDescriptorSetLayout_ != VK_NULL_HANDLE) {
        vkDestroyDescriptorSetLayout(device_, trailPropertiesDescriptorSetLayout_, nullptr);
        trailPropertiesDescriptorSetLayout_ = VK_NULL_HANDLE;
    }
    
    if (planetPropertiesDescriptorSetLayout_ != VK_NULL_HANDLE) {
        vkDestroyDescriptorSetLayout(device_, planetPropertiesDescriptorSetLayout_, nullptr);
        planetPropertiesDescriptorSetLayout_ = VK_NULL_HANDLE;
    }
    
    if (uniformDescriptorSetLayout_ != VK_NULL_HANDLE) {
        vkDestroyDescriptorSetLayout(device_, uniformDescriptorSetLayout_, nullptr);
        uniformDescriptorSetLayout_ = VK_NULL_HANDLE;
    }
}

} // namespace sdt::vulkan

