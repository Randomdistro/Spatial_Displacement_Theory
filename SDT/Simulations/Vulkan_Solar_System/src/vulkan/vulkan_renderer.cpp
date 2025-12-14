#include "vulkan/vulkan_renderer.hpp"
#include <stdexcept>
#include <iostream>
#include <set>
#include <algorithm>
#include <cstring>

namespace sdt::vulkan {

VulkanRenderer::VulkanRenderer() {
}

VulkanRenderer::~VulkanRenderer() {
    cleanup();
}

bool VulkanRenderer::initialize(uint32_t width, uint32_t height, const char* title) {
    width_ = width;
    height_ = height;
    
    // Initialize GLFW
    if (!glfwInit()) {
        std::cerr << "Failed to initialize GLFW" << std::endl;
        return false;
    }
    
    // Don't create OpenGL context
    glfwWindowHint(GLFW_CLIENT_API, GLFW_NO_API);
    glfwWindowHint(GLFW_RESIZABLE, GLFW_TRUE);
    
    window_ = glfwCreateWindow(width_, height_, title, nullptr, nullptr);
    if (!window_) {
        std::cerr << "Failed to create GLFW window" << std::endl;
        glfwTerminate();
        return false;
    }
    
    glfwSetWindowUserPointer(window_, this);
    glfwSetFramebufferSizeCallback(window_, framebufferResizeCallback);
    
    // Create Vulkan instance
    if (!createInstance()) {
        return false;
    }
    
    // Create surface
    if (!createSurface()) {
        return false;
    }
    
    // Initialize context (device)
    context_ = std::make_unique<VulkanContext>();
    if (!context_->initialize(instance_, surface_)) {
        return false;
    }
    
    // Initialize buffers helper
    buffers_ = std::make_unique<VulkanBuffers>(
        context_->getDevice(),
        context_->getPhysicalDevice()
    );
    
    // Initialize command pool for buffer operations
    buffers_->initializeCommandPool(
        context_->getGraphicsQueue(),
        context_->getQueueFamilyIndices().graphicsFamily
    );
    
    // Initialize descriptors helper
    descriptors_ = std::make_unique<VulkanDescriptors>(context_->getDevice());
    
    // Create swapchain
    if (!createSwapchain()) {
        return false;
    }
    
    // Create image views
    if (!createImageViews()) {
        return false;
    }
    
    // Create render pass
    if (!createRenderPass()) {
        return false;
    }
    
    // Create framebuffers
    if (!createFramebuffers()) {
        return false;
    }
    
    // Create command pool
    if (!createCommandPool()) {
        return false;
    }
    
    // Create command buffers
    if (!createCommandBuffers()) {
        return false;
    }
    
    // Create sync objects
    if (!createSyncObjects()) {
        return false;
    }
    
    // Create descriptor resources
    if (!createDescriptorResources()) {
        return false;
    }
    
    return true;
}

void VulkanRenderer::render() {
    glfwPollEvents();
    
    // Wait for fence
    vkWaitForFences(context_->getDevice(), 1, &inFlightFences_[currentFrame_], VK_TRUE, UINT64_MAX);
    
    // Acquire next image
    uint32_t imageIndex;
    VkResult result = vkAcquireNextImageKHR(
        context_->getDevice(),
        swapchain_,
        UINT64_MAX,
        imageAvailableSemaphores_[currentFrame_],
        VK_NULL_HANDLE,
        &imageIndex
    );
    
    if (result == VK_ERROR_OUT_OF_DATE_KHR || framebufferResized_) {
        framebufferResized_ = false;
        recreateSwapchain();
        return;
    } else if (result != VK_SUCCESS && result != VK_SUBOPTIMAL_KHR) {
        throw std::runtime_error("Failed to acquire swapchain image");
    }
    
    // Reset fence
    vkResetFences(context_->getDevice(), 1, &inFlightFences_[currentFrame_]);
    
    // Reset command buffer
    vkResetCommandBuffer(commandBuffers_[currentFrame_], 0);
    
    // Record command buffer
    VkCommandBufferBeginInfo beginInfo{};
    beginInfo.sType = VK_STRUCTURE_TYPE_COMMAND_BUFFER_BEGIN_INFO;
    
    if (vkBeginCommandBuffer(commandBuffers_[currentFrame_], &beginInfo) != VK_SUCCESS) {
        throw std::runtime_error("Failed to begin recording command buffer");
    }
    
    // Begin render pass
    VkRenderPassBeginInfo renderPassInfo{};
    renderPassInfo.sType = VK_STRUCTURE_TYPE_RENDER_PASS_BEGIN_INFO;
    renderPassInfo.renderPass = renderPass_;
    renderPassInfo.framebuffer = swapchainFramebuffers_[imageIndex];
    renderPassInfo.renderArea.offset = {0, 0};
    renderPassInfo.renderArea.extent = swapchainExtent_;
    
    VkClearValue clearColor = {{{0.0f, 0.0f, 0.1f, 1.0f}}};
    renderPassInfo.clearValueCount = 1;
    renderPassInfo.pClearValues = &clearColor;
    
    vkCmdBeginRenderPass(commandBuffers_[currentFrame_], &renderPassInfo, VK_SUBPASS_CONTENTS_INLINE);
    
    // Bind descriptor sets (camera)
    vkCmdBindDescriptorSets(
        commandBuffers_[currentFrame_],
        VK_PIPELINE_BIND_POINT_GRAPHICS,
        VK_NULL_HANDLE, // Pipeline layout (will be set by Agent 2)
        0,
        1,
        &cameraDescriptorSet_,
        0,
        nullptr
    );
    
    // TODO: Draw commands will be added by Agent 2
    
    vkCmdEndRenderPass(commandBuffers_[currentFrame_]);
    
    if (vkEndCommandBuffer(commandBuffers_[currentFrame_]) != VK_SUCCESS) {
        throw std::runtime_error("Failed to record command buffer");
    }
    
    // Submit command buffer
    VkSubmitInfo submitInfo{};
    submitInfo.sType = VK_STRUCTURE_TYPE_SUBMIT_INFO;
    
    VkSemaphore waitSemaphores[] = {imageAvailableSemaphores_[currentFrame_]};
    VkPipelineStageFlags waitStages[] = {VK_PIPELINE_STAGE_COLOR_ATTACHMENT_OUTPUT_BIT};
    submitInfo.waitSemaphoreCount = 1;
    submitInfo.pWaitSemaphores = waitSemaphores;
    submitInfo.pWaitDstStageMask = waitStages;
    submitInfo.commandBufferCount = 1;
    submitInfo.pCommandBuffers = &commandBuffers_[currentFrame_];
    
    VkSemaphore signalSemaphores[] = {renderFinishedSemaphores_[currentFrame_]};
    submitInfo.signalSemaphoreCount = 1;
    submitInfo.pSignalSemaphores = signalSemaphores;
    
    if (vkQueueSubmit(context_->getGraphicsQueue(), 1, &submitInfo, inFlightFences_[currentFrame_]) != VK_SUCCESS) {
        throw std::runtime_error("Failed to submit draw command buffer");
    }
    
    // Present
    VkPresentInfoKHR presentInfo{};
    presentInfo.sType = VK_STRUCTURE_TYPE_PRESENT_INFO_KHR;
    presentInfo.waitSemaphoreCount = 1;
    presentInfo.pWaitSemaphores = signalSemaphores;
    
    VkSwapchainKHR swapchains[] = {swapchain_};
    presentInfo.swapchainCount = 1;
    presentInfo.pSwapchains = swapchains;
    presentInfo.pImageIndices = &imageIndex;
    presentInfo.pResults = nullptr;
    
    result = vkQueuePresentKHR(context_->getGraphicsQueue(), &presentInfo);
    
    if (result == VK_ERROR_OUT_OF_DATE_KHR || result == VK_SUBOPTIMAL_KHR || framebufferResized_) {
        framebufferResized_ = false;
        recreateSwapchain();
    } else if (result != VK_SUCCESS) {
        throw std::runtime_error("Failed to present swapchain image");
    }
    
    currentFrame_ = (currentFrame_ + 1) % MAX_FRAMES_IN_FLIGHT;
}

void VulkanRenderer::cleanup() {
    if (context_ && context_->getDevice() != VK_NULL_HANDLE) {
        vkDeviceWaitIdle(context_->getDevice());
        
        cleanupSwapchain();
        
        if (cameraUniformBuffer_ != VK_NULL_HANDLE) {
            vkDestroyBuffer(context_->getDevice(), cameraUniformBuffer_, nullptr);
        }
        if (cameraUniformBufferMemory_ != VK_NULL_HANDLE) {
            vkFreeMemory(context_->getDevice(), cameraUniformBufferMemory_, nullptr);
        }
        
        if (descriptorPool_ != VK_NULL_HANDLE) {
            vkDestroyDescriptorPool(context_->getDevice(), descriptorPool_, nullptr);
        }
        
        if (cameraDescriptorSetLayout_ != VK_NULL_HANDLE) {
            vkDestroyDescriptorSetLayout(context_->getDevice(), cameraDescriptorSetLayout_, nullptr);
        }
        
        for (size_t i = 0; i < MAX_FRAMES_IN_FLIGHT; i++) {
            vkDestroySemaphore(context_->getDevice(), imageAvailableSemaphores_[i], nullptr);
            vkDestroySemaphore(context_->getDevice(), renderFinishedSemaphores_[i], nullptr);
            vkDestroyFence(context_->getDevice(), inFlightFences_[i], nullptr);
        }
        
        if (commandPool_ != VK_NULL_HANDLE) {
            vkDestroyCommandPool(context_->getDevice(), commandPool_, nullptr);
        }
    }
    
    if (surface_ != VK_NULL_HANDLE) {
        vkDestroySurfaceKHR(instance_, surface_, nullptr);
    }
    
    if (instance_ != VK_NULL_HANDLE) {
        vkDestroyInstance(instance_, nullptr);
    }
    
    if (window_) {
        glfwDestroyWindow(window_);
        glfwTerminate();
    }
}

bool VulkanRenderer::shouldClose() const {
    return glfwWindowShouldClose(window_);
}

void VulkanRenderer::getFramebufferSize(int& width, int& height) const {
    glfwGetFramebufferSize(window_, &width, &height);
}

bool VulkanRenderer::createInstance() {
    #ifdef DEBUG
    if (!checkValidationLayerSupport()) {
        std::cerr << "Validation layers requested but not available" << std::endl;
    }
    #endif
    
    VkApplicationInfo appInfo{};
    appInfo.sType = VK_STRUCTURE_TYPE_APPLICATION_INFO;
    appInfo.pApplicationName = "SDT Solar System";
    appInfo.applicationVersion = VK_MAKE_VERSION(1, 0, 0);
    appInfo.pEngineName = "SDT Engine";
    appInfo.engineVersion = VK_MAKE_VERSION(1, 0, 0);
    appInfo.apiVersion = VK_API_VERSION_1_3;
    
    VkInstanceCreateInfo createInfo{};
    createInfo.sType = VK_STRUCTURE_TYPE_INSTANCE_CREATE_INFO;
    createInfo.pApplicationInfo = &appInfo;
    
    // Get required extensions
    uint32_t glfwExtensionCount = 0;
    const char** glfwExtensions = glfwGetRequiredInstanceExtensions(&glfwExtensionCount);
    
    std::vector<const char*> extensions(glfwExtensions, glfwExtensions + glfwExtensionCount);
    #ifdef DEBUG
    extensions.push_back(VK_EXT_DEBUG_UTILS_EXTENSION_NAME);
    #endif
    
    createInfo.enabledExtensionCount = static_cast<uint32_t>(extensions.size());
    createInfo.ppEnabledExtensionNames = extensions.data();
    
    #ifdef DEBUG
    createInfo.enabledLayerCount = static_cast<uint32_t>(validationLayers_.size());
    createInfo.ppEnabledLayerNames = validationLayers_.data();
    #else
    createInfo.enabledLayerCount = 0;
    #endif
    
    if (vkCreateInstance(&createInfo, nullptr, &instance_) != VK_SUCCESS) {
        std::cerr << "Failed to create Vulkan instance" << std::endl;
        return false;
    }
    
    return true;
}

bool VulkanRenderer::createSurface() {
    if (glfwCreateWindowSurface(instance_, window_, nullptr, &surface_) != VK_SUCCESS) {
        std::cerr << "Failed to create window surface" << std::endl;
        return false;
    }
    return true;
}

bool VulkanRenderer::createSwapchain() {
    SwapchainSupportDetails swapchainSupport = querySwapchainSupport(context_->getPhysicalDevice());
    
    if (swapchainSupport.formats.empty() || swapchainSupport.presentModes.empty()) {
        return false;
    }
    
    VkSurfaceFormatKHR surfaceFormat = chooseSwapSurfaceFormat(swapchainSupport.formats);
    VkPresentModeKHR presentMode = chooseSwapPresentMode(swapchainSupport.presentModes);
    VkExtent2D extent = chooseSwapExtent(swapchainSupport.capabilities);
    
    uint32_t imageCount = swapchainSupport.capabilities.minImageCount + 1;
    if (swapchainSupport.capabilities.maxImageCount > 0 && 
        imageCount > swapchainSupport.capabilities.maxImageCount) {
        imageCount = swapchainSupport.capabilities.maxImageCount;
    }
    
    VkSwapchainCreateInfoKHR createInfo{};
    createInfo.sType = VK_STRUCTURE_TYPE_SWAPCHAIN_CREATE_INFO_KHR;
    createInfo.surface = surface_;
    createInfo.minImageCount = imageCount;
    createInfo.imageFormat = surfaceFormat.format;
    createInfo.imageColorSpace = surfaceFormat.colorSpace;
    createInfo.imageExtent = extent;
    createInfo.imageArrayLayers = 1;
    createInfo.imageUsage = VK_IMAGE_USAGE_COLOR_ATTACHMENT_BIT;
    
    QueueFamilyIndices indices = context_->getQueueFamilyIndices();
    uint32_t queueFamilyIndices[] = {indices.graphicsFamily};
    
    if (indices.graphicsFamily != UINT32_MAX) {
        createInfo.imageSharingMode = VK_SHARING_MODE_EXCLUSIVE;
        createInfo.queueFamilyIndexCount = 0;
        createInfo.pQueueFamilyIndices = nullptr;
    } else {
        createInfo.imageSharingMode = VK_SHARING_MODE_CONCURRENT;
        createInfo.queueFamilyIndexCount = 2;
        createInfo.pQueueFamilyIndices = queueFamilyIndices;
    }
    
    createInfo.preTransform = swapchainSupport.capabilities.currentTransform;
    createInfo.compositeAlpha = VK_COMPOSITE_ALPHA_OPAQUE_BIT_KHR;
    createInfo.presentMode = presentMode;
    createInfo.clipped = VK_TRUE;
    createInfo.oldSwapchain = VK_NULL_HANDLE;
    
    if (vkCreateSwapchainKHR(context_->getDevice(), &createInfo, nullptr, &swapchain_) != VK_SUCCESS) {
        std::cerr << "Failed to create swapchain" << std::endl;
        return false;
    }
    
    vkGetSwapchainImagesKHR(context_->getDevice(), swapchain_, &imageCount, nullptr);
    swapchainImages_.resize(imageCount);
    vkGetSwapchainImagesKHR(context_->getDevice(), swapchain_, &imageCount, swapchainImages_.data());
    
    swapchainImageFormat_ = surfaceFormat.format;
    swapchainExtent_ = extent;
    
    return true;
}

bool VulkanRenderer::createImageViews() {
    swapchainImageViews_.resize(swapchainImages_.size());
    
    for (size_t i = 0; i < swapchainImages_.size(); i++) {
        VkImageViewCreateInfo createInfo{};
        createInfo.sType = VK_STRUCTURE_TYPE_IMAGE_VIEW_CREATE_INFO;
        createInfo.image = swapchainImages_[i];
        createInfo.viewType = VK_IMAGE_VIEW_TYPE_2D;
        createInfo.format = swapchainImageFormat_;
        createInfo.components.r = VK_COMPONENT_SWIZZLE_IDENTITY;
        createInfo.components.g = VK_COMPONENT_SWIZZLE_IDENTITY;
        createInfo.components.b = VK_COMPONENT_SWIZZLE_IDENTITY;
        createInfo.components.a = VK_COMPONENT_SWIZZLE_IDENTITY;
        createInfo.subresourceRange.aspectMask = VK_IMAGE_ASPECT_COLOR_BIT;
        createInfo.subresourceRange.baseMipLevel = 0;
        createInfo.subresourceRange.levelCount = 1;
        createInfo.subresourceRange.baseArrayLayer = 0;
        createInfo.subresourceRange.layerCount = 1;
        
        if (vkCreateImageView(context_->getDevice(), &createInfo, nullptr, &swapchainImageViews_[i]) != VK_SUCCESS) {
            std::cerr << "Failed to create image view " << i << std::endl;
            return false;
        }
    }
    
    return true;
}

bool VulkanRenderer::createRenderPass() {
    VkAttachmentDescription colorAttachment{};
    colorAttachment.format = swapchainImageFormat_;
    colorAttachment.samples = VK_SAMPLE_COUNT_1_BIT;
    colorAttachment.loadOp = VK_ATTACHMENT_LOAD_OP_CLEAR;
    colorAttachment.storeOp = VK_ATTACHMENT_STORE_OP_STORE;
    colorAttachment.stencilLoadOp = VK_ATTACHMENT_LOAD_OP_DONT_CARE;
    colorAttachment.stencilStoreOp = VK_ATTACHMENT_STORE_OP_DONT_CARE;
    colorAttachment.initialLayout = VK_IMAGE_LAYOUT_UNDEFINED;
    colorAttachment.finalLayout = VK_IMAGE_LAYOUT_PRESENT_SRC_KHR;
    
    VkAttachmentReference colorAttachmentRef{};
    colorAttachmentRef.attachment = 0;
    colorAttachmentRef.layout = VK_IMAGE_LAYOUT_COLOR_ATTACHMENT_OPTIMAL;
    
    VkSubpassDescription subpass{};
    subpass.pipelineBindPoint = VK_PIPELINE_BIND_POINT_GRAPHICS;
    subpass.colorAttachmentCount = 1;
    subpass.pColorAttachments = &colorAttachmentRef;
    
    VkSubpassDependency dependency{};
    dependency.srcSubpass = VK_SUBPASS_EXTERNAL;
    dependency.dstSubpass = 0;
    dependency.srcStageMask = VK_PIPELINE_STAGE_COLOR_ATTACHMENT_OUTPUT_BIT;
    dependency.srcAccessMask = 0;
    dependency.dstStageMask = VK_PIPELINE_STAGE_COLOR_ATTACHMENT_OUTPUT_BIT;
    dependency.dstAccessMask = VK_ACCESS_COLOR_ATTACHMENT_WRITE_BIT;
    
    VkRenderPassCreateInfo renderPassInfo{};
    renderPassInfo.sType = VK_STRUCTURE_TYPE_RENDER_PASS_CREATE_INFO;
    renderPassInfo.attachmentCount = 1;
    renderPassInfo.pAttachments = &colorAttachment;
    renderPassInfo.subpassCount = 1;
    renderPassInfo.pSubpasses = &subpass;
    renderPassInfo.dependencyCount = 1;
    renderPassInfo.pDependencies = &dependency;
    
    if (vkCreateRenderPass(context_->getDevice(), &renderPassInfo, nullptr, &renderPass_) != VK_SUCCESS) {
        std::cerr << "Failed to create render pass" << std::endl;
        return false;
    }
    
    return true;
}

bool VulkanRenderer::createFramebuffers() {
    swapchainFramebuffers_.resize(swapchainImageViews_.size());
    
    for (size_t i = 0; i < swapchainImageViews_.size(); i++) {
        VkImageView attachments[] = {swapchainImageViews_[i]};
        
        VkFramebufferCreateInfo framebufferInfo{};
        framebufferInfo.sType = VK_STRUCTURE_TYPE_FRAMEBUFFER_CREATE_INFO;
        framebufferInfo.renderPass = renderPass_;
        framebufferInfo.attachmentCount = 1;
        framebufferInfo.pAttachments = attachments;
        framebufferInfo.width = swapchainExtent_.width;
        framebufferInfo.height = swapchainExtent_.height;
        framebufferInfo.layers = 1;
        
        if (vkCreateFramebuffer(context_->getDevice(), &framebufferInfo, nullptr, &swapchainFramebuffers_[i]) != VK_SUCCESS) {
            std::cerr << "Failed to create framebuffer " << i << std::endl;
            return false;
        }
    }
    
    return true;
}

bool VulkanRenderer::createCommandPool() {
    QueueFamilyIndices queueFamilyIndices = context_->getQueueFamilyIndices();
    
    VkCommandPoolCreateInfo poolInfo{};
    poolInfo.sType = VK_STRUCTURE_TYPE_COMMAND_POOL_CREATE_INFO;
    poolInfo.flags = VK_COMMAND_POOL_CREATE_RESET_COMMAND_BUFFER_BIT;
    poolInfo.queueFamilyIndex = queueFamilyIndices.graphicsFamily;
    
    if (vkCreateCommandPool(context_->getDevice(), &poolInfo, nullptr, &commandPool_) != VK_SUCCESS) {
        std::cerr << "Failed to create command pool" << std::endl;
        return false;
    }
    
    return true;
}

bool VulkanRenderer::createCommandBuffers() {
    commandBuffers_.resize(MAX_FRAMES_IN_FLIGHT);
    
    VkCommandBufferAllocateInfo allocInfo{};
    allocInfo.sType = VK_STRUCTURE_TYPE_COMMAND_BUFFER_ALLOCATE_INFO;
    allocInfo.commandPool = commandPool_;
    allocInfo.level = VK_COMMAND_BUFFER_LEVEL_PRIMARY;
    allocInfo.commandBufferCount = static_cast<uint32_t>(commandBuffers_.size());
    
    if (vkAllocateCommandBuffers(context_->getDevice(), &allocInfo, commandBuffers_.data()) != VK_SUCCESS) {
        std::cerr << "Failed to allocate command buffers" << std::endl;
        return false;
    }
    
    return true;
}

bool VulkanRenderer::createSyncObjects() {
    imageAvailableSemaphores_.resize(MAX_FRAMES_IN_FLIGHT);
    renderFinishedSemaphores_.resize(MAX_FRAMES_IN_FLIGHT);
    inFlightFences_.resize(MAX_FRAMES_IN_FLIGHT);
    
    VkSemaphoreCreateInfo semaphoreInfo{};
    semaphoreInfo.sType = VK_STRUCTURE_TYPE_SEMAPHORE_CREATE_INFO;
    
    VkFenceCreateInfo fenceInfo{};
    fenceInfo.sType = VK_STRUCTURE_TYPE_FENCE_CREATE_INFO;
    fenceInfo.flags = VK_FENCE_CREATE_SIGNALED_BIT;
    
    for (size_t i = 0; i < MAX_FRAMES_IN_FLIGHT; i++) {
        if (vkCreateSemaphore(context_->getDevice(), &semaphoreInfo, nullptr, &imageAvailableSemaphores_[i]) != VK_SUCCESS ||
            vkCreateSemaphore(context_->getDevice(), &semaphoreInfo, nullptr, &renderFinishedSemaphores_[i]) != VK_SUCCESS ||
            vkCreateFence(context_->getDevice(), &fenceInfo, nullptr, &inFlightFences_[i]) != VK_SUCCESS) {
            std::cerr << "Failed to create synchronization objects for frame " << i << std::endl;
            return false;
        }
    }
    
    return true;
}

bool VulkanRenderer::createDescriptorResources() {
    // Create camera descriptor set layout
    if (!descriptors_->createCameraDescriptorSetLayout(cameraDescriptorSetLayout_)) {
        return false;
    }
    
    // Create descriptor pool
    std::vector<VkDescriptorPoolSize> poolSizes;
    VkDescriptorPoolSize uniformBufferPoolSize{};
    uniformBufferPoolSize.type = VK_DESCRIPTOR_TYPE_UNIFORM_BUFFER;
    uniformBufferPoolSize.descriptorCount = static_cast<uint32_t>(MAX_FRAMES_IN_FLIGHT);
    poolSizes.push_back(uniformBufferPoolSize);
    
    if (!descriptors_->createDescriptorPool(MAX_FRAMES_IN_FLIGHT, poolSizes, descriptorPool_)) {
        return false;
    }
    
    // Allocate descriptor set
    std::vector<VkDescriptorSetLayout> layouts(MAX_FRAMES_IN_FLIGHT, cameraDescriptorSetLayout_);
    std::vector<VkDescriptorSet> descriptorSets;
    if (!descriptors_->allocateDescriptorSets(descriptorPool_, layouts, descriptorSets)) {
        return false;
    }
    cameraDescriptorSet_ = descriptorSets[0];
    
    // Create camera uniform buffer (view + projection matrices = 128 bytes)
    const VkDeviceSize bufferSize = sizeof(float) * 16 * 2; // 2 mat4s
    if (!buffers_->createUniformBuffer(bufferSize, cameraUniformBuffer_, cameraUniformBufferMemory_)) {
        return false;
    }
    
    // Update descriptor set
    descriptors_->updateDescriptorSet(
        cameraDescriptorSet_,
        0,
        cameraUniformBuffer_,
        0,
        bufferSize
    );
    
    return true;
}

SwapchainSupportDetails VulkanRenderer::querySwapchainSupport(VkPhysicalDevice device) {
    SwapchainSupportDetails details;
    
    vkGetPhysicalDeviceSurfaceCapabilitiesKHR(device, surface_, &details.capabilities);
    
    uint32_t formatCount;
    vkGetPhysicalDeviceSurfaceFormatsKHR(device, surface_, &formatCount, nullptr);
    
    if (formatCount != 0) {
        details.formats.resize(formatCount);
        vkGetPhysicalDeviceSurfaceFormatsKHR(device, surface_, &formatCount, details.formats.data());
    }
    
    uint32_t presentModeCount;
    vkGetPhysicalDeviceSurfacePresentModesKHR(device, surface_, &presentModeCount, nullptr);
    
    if (presentModeCount != 0) {
        details.presentModes.resize(presentModeCount);
        vkGetPhysicalDeviceSurfacePresentModesKHR(device, surface_, &presentModeCount, details.presentModes.data());
    }
    
    return details;
}

VkSurfaceFormatKHR VulkanRenderer::chooseSwapSurfaceFormat(const std::vector<VkSurfaceFormatKHR>& availableFormats) {
    for (const auto& availableFormat : availableFormats) {
        if (availableFormat.format == VK_FORMAT_B8G8R8A8_SRGB &&
            availableFormat.colorSpace == VK_COLOR_SPACE_SRGB_NONLINEAR_KHR) {
            return availableFormat;
        }
    }
    return availableFormats[0];
}

VkPresentModeKHR VulkanRenderer::chooseSwapPresentMode(const std::vector<VkPresentModeKHR>& availablePresentModes) {
    for (const auto& availablePresentMode : availablePresentModes) {
        if (availablePresentMode == VK_PRESENT_MODE_MAILBOX_KHR) {
            return availablePresentMode;
        }
    }
    return VK_PRESENT_MODE_FIFO_KHR;
}

VkExtent2D VulkanRenderer::chooseSwapExtent(const VkSurfaceCapabilitiesKHR& capabilities) {
    if (capabilities.currentExtent.width != UINT32_MAX) {
        return capabilities.currentExtent;
    } else {
        int width, height;
        glfwGetFramebufferSize(window_, &width, &height);
        
        VkExtent2D actualExtent = {
            static_cast<uint32_t>(width),
            static_cast<uint32_t>(height)
        };
        
        actualExtent.width = std::clamp(actualExtent.width,
            capabilities.minImageExtent.width,
            capabilities.maxImageExtent.width);
        actualExtent.height = std::clamp(actualExtent.height,
            capabilities.minImageExtent.height,
            capabilities.maxImageExtent.height);
        
        return actualExtent;
    }
}

void VulkanRenderer::cleanupSwapchain() {
    for (auto framebuffer : swapchainFramebuffers_) {
        vkDestroyFramebuffer(context_->getDevice(), framebuffer, nullptr);
    }
    
    for (auto imageView : swapchainImageViews_) {
        vkDestroyImageView(context_->getDevice(), imageView, nullptr);
    }
    
    vkDestroySwapchainKHR(context_->getDevice(), swapchain_, nullptr);
}

void VulkanRenderer::recreateSwapchain() {
    int width = 0, height = 0;
    glfwGetFramebufferSize(window_, &width, &height);
    while (width == 0 || height == 0) {
        glfwGetFramebufferSize(window_, &width, &height);
        glfwWaitEvents();
    }
    
    vkDeviceWaitIdle(context_->getDevice());
    
    cleanupSwapchain();
    
    createSwapchain();
    createImageViews();
    createFramebuffers();
}

#ifdef DEBUG
bool VulkanRenderer::checkValidationLayerSupport() {
    uint32_t layerCount;
    vkEnumerateInstanceLayerProperties(&layerCount, nullptr);
    
    std::vector<VkLayerProperties> availableLayers(layerCount);
    vkEnumerateInstanceLayerProperties(&layerCount, availableLayers.data());
    
    for (const char* layerName : validationLayers_) {
        bool layerFound = false;
        
        for (const auto& layerProperties : availableLayers) {
            if (strcmp(layerName, layerProperties.layerName) == 0) {
                layerFound = true;
                break;
            }
        }
        
        if (!layerFound) {
            return false;
        }
    }
    
    return true;
}
#endif

void VulkanRenderer::framebufferResizeCallback(GLFWwindow* window, int width, int height) {
    auto renderer = reinterpret_cast<VulkanRenderer*>(glfwGetWindowUserPointer(window));
    renderer->framebufferResized_ = true;
}

} // namespace sdt::vulkan

