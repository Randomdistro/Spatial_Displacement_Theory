#include "vulkan/vulkan_renderer.hpp"
#include <iostream>
#include <stdexcept>

int main() {
    try {
        sdt::vulkan::VulkanRenderer renderer;
        
        if (!renderer.initialize(1920, 1080, "SDT Solar System - Vulkan")) {
            std::cerr << "Failed to initialize renderer" << std::endl;
            return 1;
        }
        
        std::cout << "Vulkan renderer initialized successfully" << std::endl;
        std::cout << "Rendering loop starting..." << std::endl;
        
        // Main loop
        while (!renderer.shouldClose()) {
            renderer.render();
        }
        
        renderer.cleanup();
        std::cout << "Renderer cleaned up successfully" << std::endl;
        
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }
    
    return 0;
}

