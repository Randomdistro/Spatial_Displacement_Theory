const SDT_CONSTANTS = {
    c: 299792458, // m/s
    G: 6.67430e-11 // m^3 kg^-1 s^-2
};

// Data from SDT_Electron_Datasheets.md
// Note: Radii are scaled for visualization (not to scale with distance)
// Distances are in meters.
const SOLAR_SYSTEM_DATA = [
    {
        name: "Sun",
        type: "star",
        intrinsic_reff: 1476.6, // GM/c^2
        radius: 696340000,
        distance: 0,
        velocity: 0,
        color: "#FFD700",
        glow: "#FFA500"
    },
    {
        name: "Mercury",
        type: "planet",
        intrinsic_reff: 0.000244,
        radius: 2439700,
        distance: 5.79e10,
        velocity: 47400,
        color: "#A5A5A5",
        glow: "#E0E0E0",
        wireframeColor: "#8B4513" // Brown
    },
    {
        name: "Venus",
        type: "planet",
        intrinsic_reff: 0.00361,
        radius: 6051800,
        distance: 1.08e11,
        velocity: 35020,
        color: "#E3BB76",
        glow: "#F5D08E",
        wireframeColor: "#D8BFD8" // Light Purple
    },
    {
        name: "Earth",
        type: "planet",
        intrinsic_reff: 0.00443,
        radius: 6371000,
        distance: 1.50e11,
        velocity: 29780,
        color: "#4F97A3",
        glow: "#7AC1CD",
        moons: [
            {
                name: "Moon",
                type: "moon",
                intrinsic_reff: 0.000000055, // Tiny
                radius: 1737000,
                distance: 3.84e8, // Distance from Earth
                velocity: 1022, // Orbital velocity around Earth
                color: "#CCCCCC",
                glow: "#FFFFFF"
            }
        ],
        wireframeColor: "#00FF00" // Self
    },
    {
        name: "Mars",
        type: "planet",
        intrinsic_reff: 0.000474,
        radius: 3389500,
        distance: 2.28e11,
        velocity: 24070,
        color: "#FF6B6B",
        glow: "#FF8E8E",
        wireframeColor: "#FF0000" // Red
    },
    {
        name: "Jupiter",
        type: "planet",
        intrinsic_reff: 1.409,
        radius: 69911000,
        distance: 7.79e11,
        velocity: 13070,
        color: "#C88B3A",
        glow: "#E0A858",
        wireframeColor: "#4B0082" // Dark Purple
    },
    {
        name: "Saturn",
        type: "planet",
        intrinsic_reff: 0.422,
        radius: 58232000,
        distance: 1.43e12,
        velocity: 9680,
        color: "#C5AB6E",
        glow: "#E0C88C",
        wireframeColor: "#C0C0C0" // Silver
    },
    {
        name: "Uranus",
        type: "planet",
        intrinsic_reff: 0.0644,
        radius: 25362000,
        distance: 2.87e12,
        velocity: 6800,
        color: "#4FD0E7",
        glow: "#7FE0F0",
        wireframeColor: "#00FFFF" // Aqua
    },
    {
        name: "Neptune",
        type: "planet",
        intrinsic_reff: 0.0760,
        radius: 24622000,
        distance: 4.50e12,
        velocity: 5430,
        color: "#4B70DD",
        glow: "#6E8EF5",
        wireframeColor: "#0000FF" // Blue
    }
];

// Pre-calculate SDT values
SOLAR_SYSTEM_DATA.forEach(body => {
    body.x = 0; // Initialize to prevent NaN
    body.y = 0;
    if (body.velocity > 0) {
        body.k = SDT_CONSTANTS.c / body.velocity;
        body.k_sq = body.k * body.k;
        body.z = 1 / body.k_sq;
        body.central_reff = body.z * body.distance; // The Sun's Reff felt at this distance
    } else {
        // Sun
        body.k = Infinity;
        body.central_reff = body.intrinsic_reff;
    }
});
