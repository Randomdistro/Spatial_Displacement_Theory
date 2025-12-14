// Hover Information System
// Displays distances, velocities, Lagrange points, and SDT parameters on hover

import { calculateLagrangePoints } from '../physics/lagrange_points.js';
import { totalPressure } from '../physics/sdt_physics.js';
import { SDT_CONSTANTS } from '../data/constants.js';

export class HoverInfo {
    constructor(infoPanel) {
        this.infoPanel = infoPanel;
        this.infoTitle = infoPanel.querySelector('#info-title');
        this.infoContent = infoPanel.querySelector('#info-content');
        this.currentBody = null;
        this.currentPair = null;
    }
    
    /**
     * Show information for a single body
     * @param {Object} body - Celestial body
     * @param {Array} allBodies - All bodies in system
     */
    showBodyInfo(body, allBodies) {
        this.currentBody = body;
        this.currentPair = null;
        
        this.infoTitle.textContent = body.name;
        this.infoContent.innerHTML = '';
        
        // Basic info section
        const basicSection = this.createSection('Basic Information');
        this.addInfoRow(basicSection, 'Type', body.type);
        this.addInfoRow(basicSection, 'Radius', `${(body.radius / 1000).toExponential(2)} km`);
        this.addInfoRow(basicSection, 'Position', this.formatVector(body.position));
        this.addInfoRow(basicSection, 'Velocity', `${(body.velocity.length() / 1000).toFixed(2)} km/s`);
        
        // SDT Parameters section
        const sdtSection = this.createSection('SDT Parameters');
        this.addInfoRow(sdtSection, 'κ (kappa)', body.sdt_params.kappa.toFixed(2));
        this.addInfoRow(sdtSection, 'R_eff', `${body.sdt_params.R_eff.toExponential(2)} m`);
        this.addInfoRow(sdtSection, 'β (beta)', `${body.sdt_params.beta().toExponential(2)}`);
        
        // Pressure field section
        const pressureSection = this.createSection('Pressure Field');
        const pressure = totalPressure(body.position, allBodies);
        this.addInfoRow(pressureSection, 'CMB Pressure', `${SDT_CONSTANTS.P_CMB.toExponential(2)} Pa`);
        this.addInfoRow(pressureSection, 'Local Pressure', `${pressure.toExponential(2)} Pa`);
        this.addInfoRow(pressureSection, 'Pressure Deficit', `${((SDT_CONSTANTS.P_CMB - pressure) / SDT_CONSTANTS.P_CMB * 100).toFixed(6)}%`);
        
        this.infoPanel.classList.remove('hidden');
    }
    
    /**
     * Show information for a body pair (with Lagrange points)
     * @param {Object} primary - Primary body
     * @param {Object} secondary - Secondary body
     */
    showPairInfo(primary, secondary) {
        this.currentBody = null;
        this.currentPair = { primary, secondary };
        
        this.infoTitle.textContent = `${primary.name} - ${secondary.name}`;
        this.infoContent.innerHTML = '';
        
        // Distance section
        const distanceSection = this.createSection('Distance');
        const distance = primary.position.distanceTo(secondary.position);
        this.addInfoRow(distanceSection, 'Distance', `${(distance / SDT_CONSTANTS.AU).toFixed(4)} AU`);
        this.addInfoRow(distanceSection, 'Distance', `${distance.toExponential(2)} m`);
        
        // Velocity section
        const velocitySection = this.createSection('Relative Velocity');
        const relVel = primary.velocity.clone().sub(secondary.velocity);
        this.addInfoRow(velocitySection, 'Relative Speed', `${(relVel.length() / 1000).toFixed(2)} km/s`);
        this.addInfoRow(velocitySection, 'Relative Velocity', this.formatVector(relVel));
        
        // Lagrange Points section
        const lagrangeSection = this.createSection('Lagrange Points');
        const lagrangePoints = calculateLagrangePoints(primary, secondary);
        
        for (const [key, point] of Object.entries(lagrangePoints)) {
            const distToPrimary = point.distanceTo(primary.position);
            const distToSecondary = point.distanceTo(secondary.position);
            this.addInfoRow(lagrangeSection, `${key} Position`, this.formatVector(point));
            this.addInfoRow(lagrangeSection, `${key} Distance (Primary)`, `${(distToPrimary / SDT_CONSTANTS.AU).toFixed(4)} AU`);
            this.addInfoRow(lagrangeSection, `${key} Distance (Secondary)`, `${(distToSecondary / SDT_CONSTANTS.AU).toFixed(4)} AU`);
        }
        
        this.infoPanel.classList.remove('hidden');
    }
    
    /**
     * Hide information panel
     */
    hide() {
        this.infoPanel.classList.add('hidden');
        this.currentBody = null;
        this.currentPair = null;
    }
    
    /**
     * Create a section element
     * @param {string} title - Section title
     * @returns {HTMLElement} Section element
     */
    createSection(title) {
        const section = document.createElement('div');
        section.className = 'info-section';
        
        const h4 = document.createElement('h4');
        h4.textContent = title;
        section.appendChild(h4);
        
        this.infoContent.appendChild(section);
        return section;
    }
    
    /**
     * Add an info row to a section
     * @param {HTMLElement} section - Section element
     * @param {string} label - Label text
     * @param {string} value - Value text
     */
    addInfoRow(section, label, value) {
        const row = document.createElement('div');
        row.className = 'info-row';
        
        const labelSpan = document.createElement('span');
        labelSpan.className = 'info-label';
        labelSpan.textContent = label + ':';
        
        const valueSpan = document.createElement('span');
        valueSpan.className = 'info-value';
        valueSpan.textContent = value;
        
        row.appendChild(labelSpan);
        row.appendChild(valueSpan);
        section.appendChild(row);
    }
    
    /**
     * Format a THREE.Vector3 as string
     * @param {THREE.Vector3} vec - Vector to format
     * @returns {string} Formatted string
     */
    formatVector(vec) {
        return `(${(vec.x / SDT_CONSTANTS.AU).toFixed(4)}, ${(vec.y / SDT_CONSTANTS.AU).toFixed(4)}, ${(vec.z / SDT_CONSTANTS.AU).toFixed(4)}) AU`;
    }
}

// Import SDT_CONSTANTS for pressure calculations
import { SDT_CONSTANTS } from '../data/constants.js';

