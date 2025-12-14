// Performance Optimization Utilities
// Object pooling, LOD, culling, and other optimizations

export class PerformanceOptimizer {
    constructor() {
        this.objectPool = new Map();
        this.frameSkip = 0;
        this.maxFrameSkip = 2;  // Update shells every N frames
    }
    
    /**
     * Get object from pool or create new one
     * @param {string} type - Object type
     * @param {Function} createFn - Function to create new object
     * @returns {Object} Object from pool
     */
    getFromPool(type, createFn) {
        if (!this.objectPool.has(type)) {
            this.objectPool.set(type, []);
        }
        
        const pool = this.objectPool.get(type);
        if (pool.length > 0) {
            return pool.pop();
        }
        
        return createFn();
    }
    
    /**
     * Return object to pool
     * @param {string} type - Object type
     * @param {Object} obj - Object to return
     */
    returnToPool(type, obj) {
        if (!this.objectPool.has(type)) {
            this.objectPool.set(type, []);
        }
        
        const pool = this.objectPool.get(type);
        pool.push(obj);
    }
    
    /**
     * Check if update should be skipped (for performance)
     * @returns {boolean} True if update should be skipped
     */
    shouldSkipUpdate() {
        this.frameSkip++;
        if (this.frameSkip >= this.maxFrameSkip) {
            this.frameSkip = 0;
            return false;
        }
        return true;
    }
    
    /**
     * Calculate LOD level based on distance
     * @param {number} distance - Distance from camera
     * @param {number} maxDistance - Maximum distance for full detail
     * @returns {number} LOD level (0 = full detail, higher = less detail)
     */
    calculateLOD(distance, maxDistance) {
        const ratio = distance / maxDistance;
        if (ratio < 0.3) return 0;  // Full detail
        if (ratio < 0.6) return 1;  // Medium detail
        return 2;  // Low detail
    }
    
    /**
     * Frustum culling check
     * @param {THREE.Camera} camera - Camera object
     * @param {THREE.Vector3} position - Object position
     * @param {number} radius - Object radius
     * @returns {boolean} True if object is in frustum
     */
    isInFrustum(camera, position, radius) {
        // Simple distance-based culling
        const distance = camera.position.distanceTo(position);
        const maxDistance = camera.far;
        
        return distance - radius < maxDistance;
    }
}

