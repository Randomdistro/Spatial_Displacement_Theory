// UI Controls - Handle user input and update simulation parameters

export class UIControls {
    constructor(simulation) {
        this.simulation = simulation;
        this.setupControls();
    }
    
    setupControls() {
        // Timestep slider (logarithmic scale: 0-8 maps to 1s to 1 year)
        const timestepSlider = document.getElementById('timestepSlider');
        const timestepValue = document.getElementById('timestepValue');
        
        timestepSlider.addEventListener('input', (e) => {
            const logValue = parseFloat(e.target.value);
            // Map 0-8 to 1s to 1 year (logarithmic)
            const dt = Math.pow(10, logValue - 2);  // 0 -> 0.01s, 8 -> 1e6s (~11.6 days)
            this.simulation.setTimestep(dt);
            timestepValue.textContent = this.formatTime(dt);
        });
        
        // Initial timestep value
        const initialDt = Math.pow(10, parseFloat(timestepSlider.value) - 2);
        timestepValue.textContent = this.formatTime(initialDt);
        
        // Speed slider
        const speedSlider = document.getElementById('speedSlider');
        const speedValue = document.getElementById('speedValue');
        
        speedSlider.addEventListener('input', (e) => {
            const speed = parseFloat(e.target.value);
            this.simulation.setSpeed(speed);
            speedValue.textContent = `${speed}x`;
        });
        
        // Play/Pause button
        const playPauseBtn = document.getElementById('playPauseBtn');
        playPauseBtn.addEventListener('click', () => {
            this.simulation.togglePause();
            playPauseBtn.textContent = this.simulation.getIsPaused() ? 'Play' : 'Pause';
        });
        
        // Reset button
        const resetBtn = document.getElementById('resetBtn');
        resetBtn.addEventListener('click', () => {
            this.simulation.reset();
        });
        
        // Focus select
        const focusSelect = document.getElementById('focusSelect');
        focusSelect.addEventListener('change', (e) => {
            const value = e.target.value;
            if (value === 'free') {
                this.simulation.setFocusMode('free');
            } else {
                this.simulation.focusOnBody(value);
            }
        });
        
        // Visualization toggles
        document.getElementById('toggleParticles').addEventListener('change', (e) => {
            this.simulation.setParticlesVisible(e.target.checked);
        });
        
        document.getElementById('toggleMarkers').addEventListener('change', (e) => {
            this.simulation.setMarkersVisible(e.target.checked);
        });
        
        document.getElementById('toggleShells').addEventListener('change', (e) => {
            this.simulation.setShellsVisible(e.target.checked);
        });
        
        document.getElementById('toggleTrails').addEventListener('change', (e) => {
            this.simulation.setTrailsVisible(e.target.checked);
        });
        
        document.getElementById('toggleGrid').addEventListener('change', (e) => {
            this.simulation.setGridVisible(e.target.checked);
        });
        
        // Close info panel
        document.getElementById('closeInfo').addEventListener('click', () => {
            this.simulation.hideInfo();
        });
    }
    
    formatTime(seconds) {
        if (seconds < 60) {
            return `${seconds.toFixed(0)}s`;
        } else if (seconds < 3600) {
            return `${(seconds / 60).toFixed(1)}min`;
        } else if (seconds < 86400) {
            return `${(seconds / 3600).toFixed(2)}h`;
        } else {
            return `${(seconds / 86400).toFixed(2)}d`;
        }
    }
}

