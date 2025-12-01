const canvas = document.getElementById('simCanvas');
const ctx = canvas.getContext('2d');

// --- State ---
let width, height;
let zoom = 1.0; // Pixels per billion meters (approx)
let offsetX = 0;
let offsetY = 0;
let time = 0;
let timeSpeed = 10;
let isPaused = false;
let isDragging = false;
let lastMouseX, lastMouseY;
let hoveredBody = null;
let hoveredLine = null;
let selectedLine = null;
let focusedBodyName = "Sun";

// Feature Flags
const features = {
    wireframe: true,
    flow: true,
    grid: true,
    moons: true,
    compass: true
};

// --- Initialization ---
function resize() {
    width = window.innerWidth;
    height = window.innerHeight;
    canvas.width = width;
    canvas.height = height;
    if (focusedBodyName === "Sun") {
        offsetX = width / 2;
        offsetY = height / 2;
    }
}

window.addEventListener('resize', resize);
resize();

// --- Input Handling ---
canvas.addEventListener('mousedown', e => {
    isDragging = true;
    lastMouseX = e.clientX;
    lastMouseY = e.clientY;
    
    // Stop focusing if user drags
    if (focusedBodyName !== "Free") {
        // focusedBodyName = "Free"; // Optional: Unlock focus on drag
    }
    
    if (hoveredLine) {
        selectedLine = hoveredLine;
        updateDataPanel(selectedLine);
    } else if (!hoveredBody) {
        selectedLine = null;
        document.getElementById('data-panel').classList.add('hidden');
    }
});

canvas.addEventListener('mousemove', e => {
    if (isDragging) {
        offsetX += e.clientX - lastMouseX;
        offsetY += e.clientY - lastMouseY;
        lastMouseX = e.clientX;
        lastMouseY = e.clientY;
        focusedBodyName = "Free"; // Unlock focus on drag
        document.getElementById('focusSelect').value = "Free";
    }
    
    checkHover(e.clientX, e.clientY);
});

canvas.addEventListener('mouseup', () => isDragging = false);
canvas.addEventListener('wheel', e => {
    e.preventDefault();
    const zoomFactor = e.deltaY > 0 ? 0.9 : 1.1;
    zoom *= zoomFactor;
    document.getElementById('zoomSlider').value = zoom * 10;
});

// UI Controls
document.getElementById('zoomSlider').addEventListener('input', e => {
    zoom = e.target.value / 10;
});
document.getElementById('speedSlider').addEventListener('input', e => {
    timeSpeed = parseInt(e.target.value);
});
document.getElementById('focusSelect').addEventListener('change', e => {
    focusedBodyName = e.target.value;
});
document.getElementById('togglePause').addEventListener('click', e => {
    isPaused = !isPaused;
    e.target.innerText = isPaused ? "Play" : "Pause";
    e.target.classList.toggle('active');
});

// Feature Toggles
['wireframe', 'flow', 'grid', 'moons', 'compass'].forEach(feat => {
    const btn = document.getElementById('toggle' + feat.charAt(0).toUpperCase() + feat.slice(1));
    if (btn) {
        btn.addEventListener('click', e => {
            features[feat] = !features[feat];
            e.target.classList.toggle('active');
        });
    }
});

document.getElementById('close-panel').addEventListener('click', () => {
    document.getElementById('data-panel').classList.add('hidden');
    selectedLine = null;
});

// --- Simulation Loop ---
function update() {
    if (isPaused) return;

    // Update positions
    SOLAR_SYSTEM_DATA.forEach(body => {
        if (body.distance > 0) {
            const omega = body.velocity / body.distance;
            const angleChange = omega * timeSpeed * 100000; 
            
            if (!body.angle) body.angle = Math.random() * Math.PI * 2;
            body.angle += angleChange;
            
            body.x = Math.cos(body.angle) * body.distance;
            body.y = Math.sin(body.angle) * body.distance;
        } else {
            body.x = 0;
            body.y = 0;
        }

        // Update Moons
        if (body.moons) {
            body.moons.forEach(moon => {
                const omega = moon.velocity / moon.distance;
                const angleChange = omega * timeSpeed * 100000; // Same time scale
                
                if (!moon.angle) moon.angle = Math.random() * Math.PI * 2;
                moon.angle += angleChange;
                
                // Moon position relative to planet
                // Visual scale for moons needs to be exaggerated or they are inside the planet dot
                // Let's scale moon distance by a factor for visibility if zoom is low
                const visualMoonDist = moon.distance * 50; // Exaggerate orbit
                
                moon.relX = Math.cos(moon.angle) * visualMoonDist;
                moon.relY = Math.sin(moon.angle) * visualMoonDist;
                
                moon.x = body.x + moon.relX;
                moon.y = body.y + moon.relY;
            });
        }
    });
    
    time++;
}

// --- Rendering ---
function worldToScreen(x, y) {
    const scale = 1e-9 * zoom; // 1 pixel = 1 Gm
    return {
        x: x * scale + offsetX,
        y: y * scale + offsetY
    };
}

function updateCamera() {
    if (focusedBodyName !== "Free") {
        const body = SOLAR_SYSTEM_DATA.find(b => b.name === focusedBodyName);
        if (body && body.x !== undefined) {
            // We want body at center (width/2, height/2)
            // body.x * scale + offsetX = width/2
            // offsetX = width/2 - body.x * scale
            const scale = 1e-9 * zoom;
            offsetX = width / 2 - body.x * scale;
            offsetY = height / 2 - body.y * scale;
        }
    }
}

function drawPressureGrid() {
    if (!features.grid) return;
    
    const gridSize = 50;
    const cols = Math.ceil(width / gridSize) + 2;
    const rows = Math.ceil(height / gridSize) + 2;
    
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.03)';
    ctx.lineWidth = 1;
    
    ctx.beginPath();
    // Vertical
    for (let i = -1; i < cols; i++) {
        let xBase = (i * gridSize) - (offsetX % gridSize);
        ctx.moveTo(xBase, 0);
        ctx.lineTo(xBase, height);
    }
    // Horizontal
    for (let j = -1; j < rows; j++) {
        let yBase = (j * gridSize) - (offsetY % gridSize);
        ctx.moveTo(0, yBase);
        ctx.lineTo(width, yBase);
    }
    ctx.stroke();
    
    // Radial Gradient centered on Sun
    const sun = SOLAR_SYSTEM_DATA[0];
    const sunPos = worldToScreen(sun.x, sun.y);
    
    // Only draw gradient if sun is somewhat on screen or close
    const gradient = ctx.createRadialGradient(sunPos.x, sunPos.y, 10 * zoom, sunPos.x, sunPos.y, Math.max(width, height));
    gradient.addColorStop(0, 'rgba(0, 0, 0, 0.8)'); 
    gradient.addColorStop(0.2, 'rgba(10, 10, 20, 0.5)');
    gradient.addColorStop(1, 'rgba(20, 20, 40, 0.0)');
    
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, width, height);
}

function drawWireframes() {
    if (!features.wireframe) return;
    
    const earth = SOLAR_SYSTEM_DATA.find(b => b.name === "Earth");
    if (!earth) return;
    const earthPos = worldToScreen(earth.x, earth.y);
    
    // Draw lines from Earth to all other planets
    SOLAR_SYSTEM_DATA.forEach(body => {
        if (body.name === "Earth" || body.name === "Sun") return; // Skip Earth and Sun
        
        const bodyPos = worldToScreen(body.x, body.y);
        
        // Check hover
        // We need to update checkHover to detect these new lines if we want interaction
        // For now, just drawing
        
        ctx.lineWidth = 1.5;
        ctx.strokeStyle = body.wireframeColor || 'rgba(255, 255, 255, 0.2)';
        
        ctx.beginPath();
        ctx.moveTo(earthPos.x, earthPos.y);
        ctx.lineTo(bodyPos.x, bodyPos.y);
        ctx.stroke();
        
        // Optional: Draw a small dot at the intersection or midpoint?
    });
    
    // Draw Sun-Earth line separately?
    const sun = SOLAR_SYSTEM_DATA[0];
    const sunPos = worldToScreen(sun.x, sun.y);
    ctx.strokeStyle = 'rgba(255, 255, 0, 0.3)';
    ctx.beginPath();
    ctx.moveTo(sunPos.x, sunPos.y);
    ctx.lineTo(earthPos.x, earthPos.y);
    ctx.stroke();
}

function drawOrbitalFlows() {
    if (!features.flow) return;
    
    SOLAR_SYSTEM_DATA.slice(1).forEach(planet => {
        const planetPos = worldToScreen(planet.x, planet.y);
        const sunPos = worldToScreen(0,0); // Sun is at 0,0 world
        
        // Radius in screen pixels
        const radius = Math.sqrt(Math.pow(planetPos.x - sunPos.x, 2) + Math.pow(planetPos.y - sunPos.y, 2));
        const currentAngle = Math.atan2(planetPos.y - sunPos.y, planetPos.x - sunPos.x);
        
        ctx.lineWidth = 2 * zoom;
        
        for (let i = 0; i < 30; i++) {
            const alpha = 0.3 * (1 - i/30);
            ctx.strokeStyle = `rgba(255, 255, 255, ${alpha})`;
            ctx.beginPath();
            const startA = currentAngle - (i * 0.02);
            const endA = currentAngle - ((i+1) * 0.02);
            ctx.arc(sunPos.x, sunPos.y, radius, endA, startA);
            ctx.stroke();
        }
    });
}

function drawSagACompass() {
    if (!features.compass) return;
    
    // Sag A* is at Galactic Center.
    // In Solar System coords, it's at RA 17h 45m, Dec -29deg.
    // For a top-down view (Ecliptic plane), it's in a specific direction.
    // Let's pick a fixed direction for visualization (e.g., Top-Right).
    
    const compassSize = 60;
    const padding = 40;
    const cx = width - padding - compassSize/2;
    const cy = height - padding - compassSize/2;
    
    // Draw Kite Shape
    ctx.save();
    ctx.translate(cx, cy);
    ctx.rotate(-Math.PI / 4); // Pointing roughly towards Sag A* (Symbolic)
    
    ctx.beginPath();
    ctx.moveTo(0, -compassSize/2); // Tip
    ctx.lineTo(compassSize/4, 0);
    ctx.lineTo(0, compassSize/2); // Tail
    ctx.lineTo(-compassSize/4, 0);
    ctx.closePath();
    
    ctx.fillStyle = 'rgba(255, 0, 255, 0.2)';
    ctx.strokeStyle = '#ff00ff';
    ctx.lineWidth = 2;
    ctx.fill();
    ctx.stroke();
    
    // Label
    ctx.rotate(Math.PI / 4); // Reset rotation for text
    ctx.fillStyle = '#ff00ff';
    ctx.font = '12px Inter';
    ctx.textAlign = 'center';
    ctx.fillText("Sag A*", 0, compassSize/2 + 15);
    
    ctx.restore();
}

function drawBodies() {
    SOLAR_SYSTEM_DATA.forEach(body => {
        const pos = worldToScreen(body.x, body.y);
        
        // Visual Radius
        let vRad = body.type === 'star' ? 20 : 8; // Increased planet size
        vRad *= zoom;
        if (vRad < 3) vRad = 3; // Minimum size
        
        // Glow
        const gradient = ctx.createRadialGradient(pos.x, pos.y, vRad * 0.2, pos.x, pos.y, vRad * 2);
        gradient.addColorStop(0, body.color);
        gradient.addColorStop(1, 'rgba(0,0,0,0)');
        
        ctx.fillStyle = gradient;
        ctx.beginPath();
        ctx.arc(pos.x, pos.y, vRad * 2, 0, Math.PI * 2);
        ctx.fill();
        
        // Core
        ctx.fillStyle = body.color;
        ctx.beginPath();
        ctx.arc(pos.x, pos.y, vRad, 0, Math.PI * 2);
        ctx.fill();
        
        // Moons
        if (features.moons && body.moons) {
            body.moons.forEach(moon => {
                const moonPos = worldToScreen(moon.x, moon.y);
                let mRad = 2 * zoom;
                if (mRad < 1) mRad = 1;
                
                ctx.fillStyle = moon.color;
                ctx.beginPath();
                ctx.arc(moonPos.x, moonPos.y, mRad, 0, Math.PI * 2);
                ctx.fill();
            });
        }
        
        // Label
        if (zoom > 0.5 || hoveredBody === body || focusedBodyName === body.name) {
            ctx.fillStyle = '#fff';
            ctx.font = '10px Inter';
            ctx.fillText(body.name, pos.x + vRad + 5, pos.y + 3);
        }
    });
}

function render() {
    updateCamera();
    
    ctx.fillStyle = '#050508';
    ctx.fillRect(0, 0, width, height);
    
    drawPressureGrid();
    drawOrbitalFlows();
    drawWireframes();
    drawBodies();
    drawSagACompass();
    
    requestAnimationFrame(render);
}

// --- Interaction Logic ---
function checkHover(mx, my) {
    hoveredBody = null;
    hoveredLine = null;
    document.body.style.cursor = 'default';
    
    // Check Bodies
    for (const body of SOLAR_SYSTEM_DATA) {
        const pos = worldToScreen(body.x, body.y);
        const vRad = (body.type === 'star' ? 20 : 8) * zoom;
        const dx = mx - pos.x;
        const dy = my - pos.y;
        if (dx*dx + dy*dy < vRad*vRad * 4) {
            hoveredBody = body;
            document.body.style.cursor = 'pointer';
            showTooltip(mx, my, body);
            return;
        }
    }
    
    // Check Lines
    const sun = SOLAR_SYSTEM_DATA[0];
    const sunPos = worldToScreen(sun.x, sun.y);
    
    for (const planet of SOLAR_SYSTEM_DATA.slice(1)) {
        const planetPos = worldToScreen(planet.x, planet.y);
        const d = pointToLineDist(mx, my, sunPos.x, sunPos.y, planetPos.x, planetPos.y);
        if (d < 10) {
            hoveredLine = { bodyA: sun, bodyB: planet };
            document.body.style.cursor = 'pointer';
            hideTooltip();
            return;
        }
    }
    
    hideTooltip();
}

function pointToLineDist(x, y, x1, y1, x2, y2) {
    const A = x - x1;
    const B = y - y1;
    const C = x2 - x1;
    const D = y2 - y1;
    
    const dot = A * C + B * D;
    const len_sq = C * C + D * D;
    let param = -1;
    if (len_sq != 0) param = dot / len_sq;
    
    let xx, yy;
    if (param < 0) { xx = x1; yy = y1; }
    else if (param > 1) { xx = x2; yy = y2; }
    else { xx = x1 + param * C; yy = y1 + param * D; }
    
    const dx = x - xx;
    const dy = y - yy;
    return Math.sqrt(dx * dx + dy * dy);
}

function showTooltip(x, y, body) {
    const tooltip = document.getElementById('tooltip');
    tooltip.classList.remove('hidden');
    tooltip.style.left = x + 10 + 'px';
    tooltip.style.top = y + 10 + 'px';
    
    let html = `<strong>${body.name}</strong><br>`;
    if (body.k) {
        html += `k: ${body.k.toFixed(2)}<br>`;
        html += `v: ${(body.velocity/1000).toFixed(1)} km/s`;
    }
    tooltip.innerHTML = html;
}

function hideTooltip() {
    document.getElementById('tooltip').classList.add('hidden');
}

function updateDataPanel(line) {
    const panel = document.getElementById('data-panel');
    panel.classList.remove('hidden');
    
    const planet = line.bodyB;
    
    document.getElementById('panel-title').innerText = `${line.bodyA.name} - ${line.bodyB.name} Link`;
    document.getElementById('val-body-a').innerText = line.bodyA.name;
    document.getElementById('val-body-b').innerText = line.bodyB.name;
    
    document.getElementById('val-r').innerText = planet.distance.toExponential(2) + ' m';
    document.getElementById('val-v').innerText = planet.velocity.toLocaleString() + ' m/s';
    document.getElementById('val-k').innerText = planet.k.toFixed(2);
    document.getElementById('val-reff').innerText = planet.central_reff.toFixed(1) + ' m';
    
    const check = planet.z * planet.k_sq;
    document.getElementById('val-check').innerText = check.toFixed(6);
    
    const l1Ratio = 1 - Math.pow(planet.intrinsic_reff / (3 * line.bodyA.intrinsic_reff), 1/3);
    const l1Dist = planet.distance * l1Ratio;
    document.getElementById('val-l1').innerText = l1Dist.toExponential(2) + ' m';
}

// Start
setInterval(update, 16);
render();
