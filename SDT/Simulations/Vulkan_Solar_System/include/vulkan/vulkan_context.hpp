#pragma once

#include <vulkan/vulkan.h>
#include <vector>
#include <string>
#include <memory>

namespace sdt::vulkan {

struct QueueFamilyIndices {
    uint32_t graphicsFamily = UINT32_MAX;
    bool hasGraphicsFamily = false;
    
    bool isComplete() const {
        return hasGraphicsFamily;
    }
};

class VulkanContext {
public:
    VulkanContext();
    ~VulkanContext();
    
    // Initialize Vulkan instance and device
    bool initialize(VkInstance instance, VkSurfaceKHR surface);
    
    // Getters
    VkPhysicalDevice getPhysicalDevice() const { return physicalDevice_; }
    VkDevice getDevice() const { return device_; }
    VkQueue getGraphicsQueue() const { return graphicsQueue_; }
    QueueFamilyIndices getQueueFamilyIndices() const { return queueFamilyIndices_; }
    
    // Check if device supports required extensions
    bool checkDeviceExtensionSupport(VkPhysicalDevice device);
    
private:
    VkInstance instance_ = VK_NULL_HANDLE;
    VkPhysicalDevice physicalDevice_ = VK_NULL_HANDLE;
    VkDevice device_ = VK_NULL_HANDLE;
    VkQueue graphicsQueue_ = VK_NULL_HANDLE;
    
    QueueFamilyIndices queueFamilyIndices_;
    
    // Required device extensions
    const std::vector<const char*> deviceExtensions_ = {
        VK_KHR_SWAPCHAIN_EXTENSION_NAME
    };
    
    // Select best physical device
    VkPhysicalDevice selectPhysicalDevice();
    
    // Find queue families
    QueueFamilyIndices findQueueFamilies(VkPhysicalDevice device);
    
    // Rate physical device suitability
    int rateDeviceSuitability(VkPhysicalDevice device);
    
    // Check if device has required features
    bool isDeviceSuitable(VkPhysicalDevice device);
};

} // namespace sdt::vulkan

