#pragma once

#include "vulkan/vulkan_context.hpp"
#include "vulkan/vulkan_buffers.hpp"
#include "vulkan/vulkan_descriptors.hpp"
#include <vulkan/vulkan.h>
#include <GLFW/glfw3.h>
#include <vector>
#include <memory>

namespace sdt::vulkan {

struct SwapchainSupportDetails {
    VkSurfaceCapabilitiesKHR capabilities;
    std::vector<VkSurfaceFormatKHR> formats;
    std::vector<VkPresentModeKHR> presentModes;
};

class VulkanRenderer {
public:
    VulkanRenderer();
    ~VulkanRenderer();
    
    // Initialize Vulkan and create window
    bool initialize(uint32_t width, uint32_t height, const char* title);
    
    // Main render loop
    void render();
    
    // Cleanup
    void cleanup();
    
    // Check if window should close
    bool shouldClose() const;
    
    // Get window for input handling
    GLFWwindow* getWindow() const { return window_; }
    
    // Get current framebuffer size
    void getFramebufferSize(int& width, int& height) const;
    
private:
    // Window
    GLFWwindow* window_ = nullptr;
    uint32_t width_ = 1920;
    uint32_t height_ = 1080;
    
    // Vulkan core
    VkInstance instance_ = VK_NULL_HANDLE;
    VkSurfaceKHR surface_ = VK_NULL_HANDLE;
    std::unique_ptr<VulkanContext> context_;
    std::unique_ptr<VulkanBuffers> buffers_;
    std::unique_ptr<VulkanDescriptors> descriptors_;
    
    // Swapchain
    VkSwapchainKHR swapchain_ = VK_NULL_HANDLE;
    std::vector<VkImage> swapchainImages_;
    std::vector<VkImageView> swapchainImageViews_;
    VkFormat swapchainImageFormat_;
    VkExtent2D swapchainExtent_;
    
    // Render pass and framebuffers
    VkRenderPass renderPass_ = VK_NULL_HANDLE;
    std::vector<VkFramebuffer> swapchainFramebuffers_;
    
    // Command buffers
    VkCommandPool commandPool_ = VK_NULL_HANDLE;
    std::vector<VkCommandBuffer> commandBuffers_;
    
    // Synchronization
    std::vector<VkSemaphore> imageAvailableSemaphores_;
    std::vector<VkSemaphore> renderFinishedSemaphores_;
    std::vector<VkFence> inFlightFences_;
    size_t currentFrame_ = 0;
    const int MAX_FRAMES_IN_FLIGHT = 2;
    
    // Descriptor sets
    VkDescriptorSetLayout cameraDescriptorSetLayout_ = VK_NULL_HANDLE;
    VkDescriptorPool descriptorPool_ = VK_NULL_HANDLE;
    VkDescriptorSet cameraDescriptorSet_ = VK_NULL_HANDLE;
    
    // Camera uniform buffer
    VkBuffer cameraUniformBuffer_ = VK_NULL_HANDLE;
    VkDeviceMemory cameraUniformBufferMemory_ = VK_NULL_HANDLE;
    
    // Initialization methods
    bool createInstance();
    bool createSurface();
    bool createSwapchain();
    bool createImageViews();
    bool createRenderPass();
    bool createFramebuffers();
    bool createCommandPool();
    bool createCommandBuffers();
    bool createSyncObjects();
    bool createDescriptorResources();
    
    // Helper methods
    SwapchainSupportDetails querySwapchainSupport(VkPhysicalDevice device);
    VkSurfaceFormatKHR chooseSwapSurfaceFormat(const std::vector<VkSurfaceFormatKHR>& availableFormats);
    VkPresentModeKHR chooseSwapPresentMode(const std::vector<VkPresentModeKHR>& availablePresentModes);
    VkExtent2D chooseSwapExtent(const VkSurfaceCapabilitiesKHR& capabilities);
    
    // Cleanup methods
    void cleanupSwapchain();
    void recreateSwapchain();
    
    // Validation layers
    #ifdef DEBUG
    bool checkValidationLayerSupport();
    const std::vector<const char*> validationLayers_ = {"VK_LAYER_KHRONOS_validation"};
    #endif
    
    // Required extensions
    const std::vector<const char*> requiredExtensions_ = {
        VK_KHR_SURFACE_EXTENSION_NAME,
        #ifdef _WIN32
        VK_KHR_WIN32_SURFACE_EXTENSION_NAME,
        #elif defined(__linux__)
        VK_KHR_XLIB_SURFACE_EXTENSION_NAME,
        #endif
        VK_KHR_SWAPCHAIN_EXTENSION_NAME
    };
    
    // Static callbacks
    static void framebufferResizeCallback(GLFWwindow* window, int width, int height);
    bool framebufferResized_ = false;
};

} // namespace sdt::vulkan

