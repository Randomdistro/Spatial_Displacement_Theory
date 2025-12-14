#include "vulkan/vulkan_descriptors.hpp"
#include <stdexcept>

namespace sdt::vulkan {

VulkanDescriptors::VulkanDescriptors(VkDevice device) : device_(device) {
}

VulkanDescriptors::~VulkanDescriptors() {
    // Descriptor sets and layouts are managed externally
}

bool VulkanDescriptors::createDescriptorSetLayout(
    const std::vector<VkDescriptorSetLayoutBinding>& bindings,
    VkDescriptorSetLayout& layout
) {
    VkDescriptorSetLayoutCreateInfo layoutInfo{};
    layoutInfo.sType = VK_STRUCTURE_TYPE_DESCRIPTOR_SET_LAYOUT_CREATE_INFO;
    layoutInfo.bindingCount = static_cast<uint32_t>(bindings.size());
    layoutInfo.pBindings = bindings.data();
    
    return vkCreateDescriptorSetLayout(device_, &layoutInfo, nullptr, &layout) == VK_SUCCESS;
}

bool VulkanDescriptors::createDescriptorPool(
    uint32_t maxSets,
    const std::vector<VkDescriptorPoolSize>& poolSizes,
    VkDescriptorPool& pool
) {
    VkDescriptorPoolCreateInfo poolInfo{};
    poolInfo.sType = VK_STRUCTURE_TYPE_DESCRIPTOR_POOL_CREATE_INFO;
    poolInfo.poolSizeCount = static_cast<uint32_t>(poolSizes.size());
    poolInfo.pPoolSizes = poolSizes.data();
    poolInfo.maxSets = maxSets;
    
    return vkCreateDescriptorPool(device_, &poolInfo, nullptr, &pool) == VK_SUCCESS;
}

bool VulkanDescriptors::allocateDescriptorSets(
    VkDescriptorPool pool,
    const std::vector<VkDescriptorSetLayout>& layouts,
    std::vector<VkDescriptorSet>& descriptorSets
) {
    descriptorSets.resize(layouts.size());
    
    VkDescriptorSetAllocateInfo allocInfo{};
    allocInfo.sType = VK_STRUCTURE_TYPE_DESCRIPTOR_SET_ALLOCATE_INFO;
    allocInfo.descriptorPool = pool;
    allocInfo.descriptorSetCount = static_cast<uint32_t>(layouts.size());
    allocInfo.pSetLayouts = layouts.data();
    
    return vkAllocateDescriptorSets(device_, &allocInfo, descriptorSets.data()) == VK_SUCCESS;
}

void VulkanDescriptors::updateDescriptorSet(
    VkDescriptorSet descriptorSet,
    uint32_t binding,
    VkBuffer buffer,
    VkDeviceSize offset,
    VkDeviceSize range
) {
    VkDescriptorBufferInfo bufferInfo{};
    bufferInfo.buffer = buffer;
    bufferInfo.offset = offset;
    bufferInfo.range = range;
    
    VkWriteDescriptorSet descriptorWrite{};
    descriptorWrite.sType = VK_STRUCTURE_TYPE_WRITE_DESCRIPTOR_SET;
    descriptorWrite.dstSet = descriptorSet;
    descriptorWrite.dstBinding = binding;
    descriptorWrite.dstArrayElement = 0;
    descriptorWrite.descriptorType = VK_DESCRIPTOR_TYPE_UNIFORM_BUFFER;
    descriptorWrite.descriptorCount = 1;
    descriptorWrite.pBufferInfo = &bufferInfo;
    
    vkUpdateDescriptorSets(device_, 1, &descriptorWrite, 0, nullptr);
}

bool VulkanDescriptors::createCameraDescriptorSetLayout(VkDescriptorSetLayout& layout) {
    // Camera uniform buffer: view matrix (64 bytes) + projection matrix (64 bytes) = 128 bytes
    std::vector<VkDescriptorSetLayoutBinding> bindings;
    
    VkDescriptorSetLayoutBinding cameraBinding{};
    cameraBinding.binding = 0;
    cameraBinding.descriptorType = VK_DESCRIPTOR_TYPE_UNIFORM_BUFFER;
    cameraBinding.descriptorCount = 1;
    cameraBinding.stageFlags = VK_SHADER_STAGE_VERTEX_BIT;
    cameraBinding.pImmutableSamplers = nullptr;
    
    bindings.push_back(cameraBinding);
    
    return createDescriptorSetLayout(bindings, layout);
}

} // namespace sdt::vulkan

