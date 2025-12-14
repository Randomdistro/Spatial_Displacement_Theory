#pragma once

#include <vulkan/vulkan.h>
#include <vector>

namespace sdt::vulkan {

class VulkanBuffers {
public:
    VulkanBuffers(VkDevice device, VkPhysicalDevice physicalDevice);
    ~VulkanBuffers();
    
    // Create buffer
    bool createBuffer(
        VkDeviceSize size,
        VkBufferUsageFlags usage,
        VkMemoryPropertyFlags properties,
        VkBuffer& buffer,
        VkDeviceMemory& bufferMemory
    );
    
    // Copy buffer data
    void copyBuffer(VkBuffer srcBuffer, VkBuffer dstBuffer, VkDeviceSize size);
    
    // Create uniform buffer
    bool createUniformBuffer(VkDeviceSize size, VkBuffer& buffer, VkDeviceMemory& bufferMemory);
    
    // Update buffer data
    void updateBuffer(VkDeviceMemory memory, const void* data, VkDeviceSize size);
    
    // Find memory type
    uint32_t findMemoryType(uint32_t typeFilter, VkMemoryPropertyFlags properties);
    
    // Initialize command pool (needed for buffer copies)
    void initializeCommandPool(VkQueue graphicsQueue, uint32_t queueFamilyIndex);
    
private:
    VkDevice device_ = VK_NULL_HANDLE;
    VkPhysicalDevice physicalDevice_ = VK_NULL_HANDLE;
    VkCommandPool commandPool_ = VK_NULL_HANDLE;
    VkQueue graphicsQueue_ = VK_NULL_HANDLE;
    
    void createCommandPool(VkQueue graphicsQueue, uint32_t queueFamilyIndex);
};

} // namespace sdt::vulkan

