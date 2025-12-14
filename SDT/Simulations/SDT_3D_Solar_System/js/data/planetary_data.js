// Planetary Parameters - Loaded from SDT/data/planetary_parameters.csv
// SDT uses k_factor (Ϟ) directly - no beta, no GM, no mass

import { CelestialBody, SDTParameters, SDT_CONSTANTS } from './constants.js';
import * as THREE from 'three';

// Planetary data from verified sources
// Format: name, radius (m), semi-major axis (m), orbital period (s), k_factor, color
const PLANETARY_DATA = [
    {
        name: 'Sun',
        type: 'star',
        radius: 6.957e8,
        a: 0,
        T: 0,
        k_factor: 686.42,
        color: 0xffff00,
        size: 20
    },
    {
        name: 'Mercury',
        type: 'planet',
        radius: 2.439e6,
        a: 5.791e10,
        T: 7.600e6,
        k_factor: 686.42,
        color: 0x8c7853,
        size: 3
    },
    {
        name: 'Venus',
        type: 'planet',
        radius: 6.052e6,
        a: 1.082e11,
        T: 1.941e7,
        k_factor: 686.42,
        color: 0xffc649,
        size: 4
    },
    {
        name: 'Earth',
        type: 'planet',
        radius: 6.371e6,
        a: 1.496e11,
        T: 3.156e7,
        k_factor: 686.42,
        color: 0x6b93d6,
        size: 4
    },
    {
        name: 'Mars',
        type: 'planet',
        radius: 3.390e6,
        a: 2.279e11,
        T: 5.935e7,
        k_factor: 686.42,
        color: 0xc1440e,
        size: 3
    },
    {
        name: 'Jupiter',
        type: 'planet',
        radius: 6.991e7,
        a: 7.785e11,
        T: 3.743e8,
        k_factor: 686.42,
        color: 0xd8ca9d,
        size: 12
    },
    {
        name: 'Saturn',
        type: 'planet',
        radius: 5.823e7,
        a: 1.433e12,
        T: 9.293e8,
        k_factor: 686.42,
        color: 0xfad5a5,
        size: 10
    },
    {
        name: 'Uranus',
        type: 'planet',
        radius: 2.536e7,
        a: 2.867e12,
        T: 2.651e9,
        k_factor: 686.42,
        color: 0x4fd0e7,
        size: 7
    },
    {
        name: 'Neptune',
        type: 'planet',
        radius: 2.462e7,
        a: 4.515e12,
        T: 5.200e9,
        k_factor: 686.42,
        color: 0x4b70dd,
        size: 7
    }
];

// Moon data (Earth-Moon system)
const MOON_DATA = {
    name: 'Moon',
    type: 'moon',
    radius: 1.737e6,
    a: 3.844e8,
    T: 2.361e6,
    k_factor: 37902.41,  // Earth's k_factor for Moon orbit
    color: 0x999999,
    size: 2
};

/**
 * Create celestial bodies from planetary data
 * Uses SDT parameters and initializes positions/velocities
 */
export function createSolarSystem() {
    const bodies = [];
    const sun = new CelestialBody('Sun', 'star');
    
    // Initialize Sun
    const sunData = PLANETARY_DATA[0];
    sun.radius = sunData.radius;
    sun.sdt_params = new SDTParameters(sunData.k_factor, sunData.radius);
    sun.position.set(0, 0, 0);
    sun.velocity.set(0, 0, 0);
    sun.color = sunData.color;
    sun.size = sunData.size;
    bodies.push(sun);
    
    // Initialize planets
    for (let i = 1; i < PLANETARY_DATA.length; i++) {
        const data = PLANETARY_DATA[i];
        const body = new CelestialBody(data.name, data.type);
        
        body.radius = data.radius;
        body.sdt_params = new SDTParameters(data.k_factor, sun.radius);  // Use Sun's R_eff
        body.color = data.color;
        body.size = data.size;
        
        // Initialize circular orbit at semi-major axis
        // Position: at semi-major axis along x-axis
        body.position.set(data.a, 0, 0);
        
        // Velocity: perpendicular to position, magnitude from SDT orbital velocity
        const v_orb = sun.sdt_params.orbitalVelocity(data.a);
        body.velocity.set(0, v_orb, 0);
        
        bodies.push(body);
    }
    
    // Initialize Moon (orbiting Earth)
    const earth = bodies.find(b => b.name === 'Earth');
    if (earth) {
        const moon = new CelestialBody(MOON_DATA.name, MOON_DATA.type);
        moon.radius = MOON_DATA.radius;
        moon.sdt_params = new SDTParameters(MOON_DATA.k_factor, earth.radius);
        moon.color = MOON_DATA.color;
        moon.size = MOON_DATA.size;
        
        // Moon position relative to Earth
        const moon_a = MOON_DATA.a;
        moon.position.copy(earth.position);
        moon.position.x += moon_a;
        
        // Moon velocity (Earth's velocity + orbital velocity around Earth)
        const v_orb_moon = earth.sdt_params.orbitalVelocity(moon_a);
        moon.velocity.copy(earth.velocity);
        moon.velocity.y += v_orb_moon;
        
        bodies.push(moon);
    }
    
    return bodies;
}

/**
 * Calculate orbital marker positions
 * Returns array of {radius, label} for white point markers
 */
export function getOrbitalMarkers() {
    const markers = [];
    
    // Get orbital radii from planetary data
    const mercury_a = PLANETARY_DATA[1].a;
    const venus_a = PLANETARY_DATA[2].a;
    const earth_a = PLANETARY_DATA[3].a;
    const mars_a = PLANETARY_DATA[4].a;
    const jupiter_a = PLANETARY_DATA[5].a;
    const saturn_a = PLANETARY_DATA[6].a;
    const uranus_a = PLANETARY_DATA[7].a;
    const neptune_a = PLANETARY_DATA[8].a;
    
    // 50% Mercury orbital radius
    markers.push({ radius: mercury_a * 0.5, label: '50% Mercury' });
    
    // Mercury orbit (with 20% offset to avoid planet)
    markers.push({ radius: mercury_a * 1.2, label: 'Mercury Orbit' });
    
    // Halfway to Venus
    markers.push({ radius: (mercury_a + venus_a) / 2, label: 'Halfway to Venus' });
    
    // Venus orbit (20% offset)
    markers.push({ radius: venus_a * 1.2, label: 'Venus Orbit' });
    
    // Halfway Venus-Earth
    markers.push({ radius: (venus_a + earth_a) / 2, label: 'Halfway Venus-Earth' });
    
    // Earth orbit
    markers.push({ radius: earth_a * 1.2, label: 'Earth Orbit' });
    
    // 1/3 and 2/3 to Mars
    const earth_mars_dist = mars_a - earth_a;
    markers.push({ radius: earth_a + earth_mars_dist / 3, label: '1/3 to Mars' });
    markers.push({ radius: earth_a + earth_mars_dist * 2 / 3, label: '2/3 to Mars' });
    
    // Mars orbit
    markers.push({ radius: mars_a * 1.2, label: 'Mars Orbit' });
    
    // 1/3 and 2/3 to Jupiter
    const mars_jupiter_dist = jupiter_a - mars_a;
    markers.push({ radius: mars_a + mars_jupiter_dist / 3, label: '1/3 to Jupiter' });
    markers.push({ radius: mars_a + mars_jupiter_dist * 2 / 3, label: '2/3 to Jupiter' });
    
    // Jupiter orbit
    markers.push({ radius: jupiter_a * 1.2, label: 'Jupiter Orbit' });
    
    // 1/3 and 2/3 to Saturn
    const jupiter_saturn_dist = saturn_a - jupiter_a;
    markers.push({ radius: jupiter_a + jupiter_saturn_dist / 3, label: '1/3 to Saturn' });
    markers.push({ radius: jupiter_a + jupiter_saturn_dist * 2 / 3, label: '2/3 to Saturn' });
    
    // Saturn orbit
    markers.push({ radius: saturn_a * 1.2, label: 'Saturn Orbit' });
    
    // 1/3 and 2/3 to Uranus
    const saturn_uranus_dist = uranus_a - saturn_a;
    markers.push({ radius: saturn_a + saturn_uranus_dist / 3, label: '1/3 to Uranus' });
    markers.push({ radius: saturn_a + saturn_uranus_dist * 2 / 3, label: '2/3 to Uranus' });
    
    // Uranus orbit
    markers.push({ radius: uranus_a * 1.2, label: 'Uranus Orbit' });
    
    // 1/3 and 2/3 to Neptune
    const uranus_neptune_dist = neptune_a - uranus_a;
    markers.push({ radius: uranus_a + uranus_neptune_dist / 3, label: '1/3 to Neptune' });
    markers.push({ radius: uranus_a + uranus_neptune_dist * 2 / 3, label: '2/3 to Neptune' });
    
    // Neptune orbit
    markers.push({ radius: neptune_a * 1.2, label: 'Neptune Orbit' });
    
    return markers;
}

