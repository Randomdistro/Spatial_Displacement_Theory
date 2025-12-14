#pragma once

#include <vulkan/vulkan.h>
#include <vector>

namespace sdt::vulkan {

class VulkanDescriptors {
public:
    VulkanDescriptors(VkDevice device);
    ~VulkanDescriptors();
    
    // Create descriptor set layout
    bool createDescriptorSetLayout(
        const std::vector<VkDescriptorSetLayoutBinding>& bindings,
        VkDescriptorSetLayout& layout
    );
    
    // Create descriptor pool
    bool createDescriptorPool(
        uint32_t maxSets,
        const std::vector<VkDescriptorPoolSize>& poolSizes,
        VkDescriptorPool& pool
    );
    
    // Allocate descriptor sets
    bool allocateDescriptorSets(
        VkDescriptorPool pool,
        const std::vector<VkDescriptorSetLayout>& layouts,
        std::vector<VkDescriptorSet>& descriptorSets
    );
    
    // Update descriptor set with uniform buffer
    void updateDescriptorSet(
        VkDescriptorSet descriptorSet,
        uint32_t binding,
        VkBuffer buffer,
        VkDeviceSize offset,
        VkDeviceSize range
    );
    
    // Create camera descriptor set layout (view/projection matrices)
    bool createCameraDescriptorSetLayout(VkDescriptorSetLayout& layout);
    
private:
    VkDevice device_ = VK_NULL_HANDLE;
};

} // namespace sdt::vulkan

