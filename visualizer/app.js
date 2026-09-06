/**
 * Eigenmode Orbital Dynamics — 3D Resonator Simulation Engine
 * Author: Rick Drayson
 * 
 * Implements real-time 3D simulation of macroscopic standing wave eigenmodes,
 * logarithmic planetary shells, Keplerian orbits, wave potential scopes,
 * screenshot capture, and video recording.
 */

const SYSTEM_DATA = {
    sol: {
        name: "Solar System (Sol / G2V)",
        hostName: "Sol",
        hostColor: 0xffaa00,
        hostSize: 2.5,
        unit: "AU",
        r0: 0.21355,
        lambda: 0.5373,
        k: 1.7114,
        r2: 0.9934,
        formula: "r_n = 0.2136 · (1.7114)ⁿ AU",
        bodies: [
            { name: "Mercury", n: 1, r: 0.3871, size: 0.6, color: 0xa0a0a0 },
            { name: "Venus", n: 2, r: 0.7233, size: 0.9, color: 0xe3bb76 },
            { name: "Earth", n: 3, r: 1.0000, size: 1.0, color: 0x2277ff },
            { name: "Mars", n: 4, r: 1.5237, size: 0.7, color: 0xcc4422 },
            { name: "Ceres / Belt", n: 5, r: 2.7675, size: 0.5, color: 0xd4a373, isBelt: true },
            { name: "Jupiter", n: 6, r: 5.2044, size: 2.2, color: 0xd4a373 },
            { name: "Saturn", n: 7, r: 9.5826, size: 1.8, color: 0xf4e2bb, hasRings: true },
            { name: "Uranus", n: 8, r: 19.2184, size: 1.4, color: 0x70d6ff },
            { name: "Neptune", n: 9, r: 30.1104, size: 1.3, color: 0x3a86ff },
            { name: "Pluto", n: 10, r: 39.4820, size: 0.5, color: 0xc8b6ff }
        ],
        predictedNodes: [
            { n: 11, r: 78.753, name: "Outer Shell (n=11)" },
            { n: 12, r: 134.775, name: "Outer Shell (n=12)" }
        ]
    },
    trappist1: {
        name: "TRAPPIST-1 (M8V Red Dwarf)",
        hostName: "TRAPPIST-1",
        hostColor: 0xff3b30,
        hostSize: 1.8,
        unit: "AU",
        r0: 0.00922,
        lambda: 0.2771,
        k: 1.3193,
        r2: 0.9943,
        formula: "r_n = 0.0092 · (1.3193)ⁿ AU",
        bodies: [
            { name: "TRAPPIST-1b", n: 1, r: 0.01154, size: 0.8, color: 0x8ecae6 },
            { name: "TRAPPIST-1c", n: 2, r: 0.01580, size: 0.8, color: 0x219ebc },
            { name: "TRAPPIST-1d", n: 3, r: 0.02227, size: 0.7, color: 0x023047 },
            { name: "TRAPPIST-1e", n: 4, r: 0.02925, size: 0.9, color: 0x588157 },
            { name: "TRAPPIST-1f", n: 5, r: 0.03849, size: 0.9, color: 0x3a5a40 },
            { name: "TRAPPIST-1g", n: 6, r: 0.04683, size: 1.0, color: 0xa3b18a },
            { name: "TRAPPIST-1h", n: 7, r: 0.06189, size: 0.6, color: 0xdad7cd }
        ],
        predictedNodes: [
            { n: 8, r: 0.0846, name: "Predicted (n=8)" },
            { n: 9, r: 0.1116, name: "Predicted (n=9)" }
        ]
    },
    kepler90: {
        name: "Kepler-90 (G0V Star)",
        hostName: "Kepler-90",
        hostColor: 0xffd166,
        hostSize: 2.6,
        unit: "AU",
        r0: 0.04990,
        lambda: 0.3364,
        k: 1.3999,
        r2: 0.9886,
        formula: "r_n = 0.0499 · (1.4000)ⁿ AU",
        bodies: [
            { name: "Kepler-90b", n: 1, r: 0.0740, size: 0.7, color: 0xe76f51 },
            { name: "Kepler-90c", n: 2, r: 0.0890, size: 0.7, color: 0xf4a261 },
            { name: "Kepler-90i", n: 3, r: 0.1234, size: 0.8, color: 0xe9c46a },
            { name: "Kepler-90d", n: 5, r: 0.3200, size: 1.2, color: 0x2a9d8f },
            { name: "Kepler-90e", n: 6, r: 0.4200, size: 1.2, color: 0x264653 },
            { name: "Kepler-90f", n: 7, r: 0.4800, size: 1.4, color: 0x457b9d },
            { name: "Kepler-90g", n: 8, r: 0.7100, size: 1.8, color: 0x1d3557 },
            { name: "Kepler-90h", n: 9, r: 1.0100, size: 2.0, color: 0xe63946 }
        ],
        predictedNodes: [
            { n: 4, r: 0.1917, name: "Gap Slot (n=4)" },
            { n: 10, r: 1.4427, name: "Outer Shell (n=10)" }
        ]
    },
    kepler11: {
        name: "Kepler-11 (G6V Star)",
        hostName: "Kepler-11",
        hostColor: 0xffe89e,
        hostSize: 2.4,
        unit: "AU",
        r0: 0.06571,
        lambda: 0.2752,
        k: 1.3168,
        r2: 0.9942,
        formula: "r_n = 0.0657 · (1.3168)ⁿ AU",
        bodies: [
            { name: "Kepler-11b", n: 1, r: 0.0910, size: 0.8, color: 0xb5e2fa },
            { name: "Kepler-11c", n: 2, r: 0.1070, size: 1.0, color: 0x0fa3b1 },
            { name: "Kepler-11d", n: 3, r: 0.1550, size: 1.2, color: 0xeddea4 },
            { name: "Kepler-11e", n: 4, r: 0.1950, size: 1.3, color: 0xf7a072 },
            { name: "Kepler-11f", n: 5, r: 0.2500, size: 1.1, color: 0xff9b54 },
            { name: "Kepler-11g", n: 7, r: 0.4660, size: 1.4, color: 0x706993 }
        ],
        predictedNodes: [
            { n: 6, r: 0.3425, name: "Gap Slot (n=6)" },
            { n: 8, r: 0.5939, name: "Outer Shell (n=8)" }
        ]
    },
    cancri55: {
        name: "55 Cancri A (K0IV Star)",
        hostName: "55 Cnc A",
        hostColor: 0xffaa44,
        hostSize: 2.3,
        unit: "AU",
        r0: 0.01045,
        lambda: 0.7178,
        k: 2.0498,
        r2: 0.9873,
        formula: "r_n = 0.0105 · (2.050)ⁿ AU",
        bodies: [
            { name: "55 Cnc e", n: 1, r: 0.0154, size: 0.8, color: 0xcc3300 },
            { name: "55 Cnc b", n: 3, r: 0.1134, size: 1.6, color: 0x336699 },
            { name: "55 Cnc c", n: 4, r: 0.2373, size: 1.3, color: 0x6699cc },
            { name: "55 Cnc f", n: 6, r: 0.7708, size: 1.4, color: 0x99ccff },
            { name: "55 Cnc d", n: 9, r: 5.7600, size: 2.2, color: 0xcc9933 }
        ],
        predictedNodes: [
            { n: 2, r: 0.0439, name: "Gap (n=2)" },
            { n: 5, r: 0.3783, name: "Gap (n=5)" },
            { n: 7, r: 1.5897, name: "Gap (n=7)" },
            { n: 8, r: 3.2585, name: "Gap (n=8)" }
        ]
    },
    jovian: {
        name: "Jovian Galilean System",
        hostName: "Jupiter",
        hostColor: 0xd4a373,
        hostSize: 3.2,
        unit: "10³ km",
        r0: 251.83,
        lambda: 0.4955,
        k: 1.6413,
        r2: 0.9976,
        formula: "r_n = 251.83 · (1.6413)ⁿ × 10³ km",
        bodies: [
            { name: "Io", n: 1, r: 421.8, size: 0.8, color: 0xffd166 },
            { name: "Europa", n: 2, r: 671.1, size: 0.7, color: 0xe0e8f5 },
            { name: "Ganymede", n: 3, r: 1070.4, size: 1.1, color: 0x9a8c98 },
            { name: "Callisto", n: 4, r: 1882.7, size: 1.0, color: 0x4a4e69 }
        ],
        predictedNodes: [
            { n: 5, r: 2999.17, name: "Outer Shell (n=5)" }
        ]
    },
    saturnian: {
        name: "Saturnian Major Satellite System",
        hostName: "Saturn",
        hostColor: 0xf4e2bb,
        hostSize: 2.8,
        unit: "10³ km",
        r0: 135.56,
        lambda: 0.2703,
        k: 1.3104,
        r2: 0.9986,
        formula: "r_n = 135.56 · (1.3104)ⁿ × 10³ km",
        bodies: [
            { name: "Mimas", n: 1, r: 185.54, size: 0.5, color: 0xd8d8d8 },
            { name: "Enceladus", n: 2, r: 238.04, size: 0.5, color: 0xffffff },
            { name: "Tethys", n: 3, r: 294.67, size: 0.6, color: 0xd0d0d0 },
            { name: "Dione", n: 4, r: 377.42, size: 0.6, color: 0xb8b8b8 },
            { name: "Rhea", n: 5, r: 527.07, size: 0.7, color: 0xa8a8a8 },
            { name: "Titan", n: 8, r: 1221.87, size: 1.2, color: 0xe0a96d },
            { name: "Hyperion", n: 9, r: 1481.10, size: 0.5, color: 0x8a7968 },
            { name: "Iapetus", n: 12, r: 3560.80, size: 0.7, color: 0x5a504a }
        ],
        predictedNodes: [
            { n: 6, r: 686.25, name: "Gap Slot (n=6)" },
            { n: 7, r: 899.23, name: "Gap Slot (n=7)" },
            { n: 10, r: 2023.23, name: "Gap Slot (n=10)" },
            { n: 11, r: 2651.16, name: "Gap Slot (n=11)" }
        ]
    },
    uranian: {
        name: "Uranus Major Satellite System",
        hostName: "Uranus",
        hostColor: 0x70d6ff,
        hostSize: 2.2,
        unit: "10³ km",
        r0: 88.28,
        lambda: 0.3831,
        k: 1.4668,
        r2: 0.9951,
        formula: "r_n = 88.28 · (1.4668)ⁿ × 10³ km",
        bodies: [
            { name: "Miranda", n: 1, r: 129.9, size: 0.5, color: 0xced4da },
            { name: "Ariel", n: 2, r: 190.9, size: 0.6, color: 0xe9ecef },
            { name: "Umbriel", n: 3, r: 266.0, size: 0.6, color: 0x6c757d },
            { name: "Titania", n: 4, r: 436.3, size: 0.8, color: 0xdee2e6 },
            { name: "Oberon", n: 5, r: 583.5, size: 0.8, color: 0xadb5bd }
        ],
        predictedNodes: [
            { n: 6, r: 879.38, name: "Outer Shell (n=6)" }
        ]
    },
    toi700: {
        name: "TOI-700 (M2V Dwarf)",
        hostName: "TOI-700",
        hostColor: 0xff5a36,
        hostSize: 1.9,
        unit: "AU",
        r0: 0.05106,
        lambda: 0.3008,
        k: 1.3509,
        r2: 0.9871,
        formula: "r_n = 0.0511 · (1.3509)ⁿ AU",
        bodies: [
            { name: "TOI-700 b", n: 1, r: 0.0677, size: 0.7, color: 0x48cae4 },
            { name: "TOI-700 c", n: 2, r: 0.0929, size: 0.9, color: 0x0096c7 },
            { name: "TOI-700 e", n: 3, r: 0.1340, size: 0.8, color: 0x52b788 },
            { name: "TOI-700 d", n: 4, r: 0.1633, size: 0.9, color: 0x2d6a4f }
        ],
        predictedNodes: [
            { n: 5, r: 0.2298, name: "Outer Shell (n=5)" },
            { n: 6, r: 0.3104, name: "Outer Shell (n=6)" }
        ]
    }
};

let currentSystemKey = "sol";
let currentSystem = SYSTEM_DATA.sol;
let simSpeed = 1.0;
let isPaused = false;
let simTime = 0;
let useLogScale = false;

// Three.js Core
let scene, camera, renderer, controls;
let starMesh, starGlow, starLabel, cymaticMesh;
let orbitalObjects = [];
let shellMeshes = [];
let predictedShellMeshes = [];

// Video Recording Globals
let mediaRecorder = null;
let recordedChunks = [];
let isRecording = false;
let recordStartTime = 0;
let recordTimerInterval = null;

function init() {
    const container = document.getElementById("canvas-container");
    
    // Scene setup
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0x02040a);
    scene.fog = new THREE.FogExp2(0x02040a, 0.003);

    // Camera setup
    camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.1, 2000);
    camera.position.set(0, 75, 110);

    // Renderer setup
    renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.2;
    container.appendChild(renderer.domElement);

    // Controls
    controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.maxDistance = 600;
    controls.minDistance = 5;

    // Lighting
    const ambientLight = new THREE.AmbientLight(0x223344, 0.6);
    scene.add(ambientLight);

    const pointLight = new THREE.PointLight(0xffffff, 2.5, 500);
    scene.add(pointLight);

    buildCymaticRippleGrid();
    loadSystem(currentSystemKey);
    initEventListeners();
    animate();
}

/**
 * Maps physical distance to simulation coordinate radius
 */
function getSimRadius(r, n) {
    if (useLogScale) {
        // Logarithmic scale: r_sim is proportional to mode index n
        return (n + 0.8) * 12.0;
    } else {
        // Linear scale with normalized power compression for visual clarity
        const r_min = currentSystem.bodies[0].r;
        const r_max = currentSystem.bodies[currentSystem.bodies.length - 1].r;
        const norm = (r - r_min) / (r_max - r_min + 0.0001);
        return 12 + Math.pow(norm, 0.55) * 110;
    }
}

/**
 * Creates background cymatics standing wave ripple mesh
 */
function buildCymaticRippleGrid() {
    const size = 300;
    const segments = 120;
    const geometry = new THREE.PlaneGeometry(size, size, segments, segments);
    geometry.rotateX(-Math.PI / 2);

    const material = new THREE.MeshBasicMaterial({
        color: 0x0a3254,
        wireframe: true,
        transparent: true,
        opacity: 0.18
    });

    cymaticMesh = new THREE.Mesh(geometry, material);
    cymaticMesh.position.y = -0.5;
    scene.add(cymaticMesh);
}

function updateCymaticMesh(time) {
    if (!cymaticMesh || !document.getElementById("toggle-cymatic-mesh").checked) {
        if (cymaticMesh) cymaticMesh.visible = false;
        return;
    }
    cymaticMesh.visible = true;
    const pos = cymaticMesh.geometry.attributes.position;
    const kappa = Math.PI / currentSystem.lambda;
    
    for (let i = 0; i < pos.count; i++) {
        const x = pos.getX(i);
        const z = pos.getZ(i);
        const r = Math.sqrt(x * x + z * z) + 0.1;
        // Logarithmic standing wave ripple formula
        const wave = Math.sin(kappa * Math.log(r / 5.0) - time * 0.8) / (1.0 + r * 0.03);
        pos.setY(i, wave * 1.8);
    }
    pos.needsUpdate = true;
}

/**
 * Loads a celestial/satellite resonator system
 */
function loadSystem(key) {
    currentSystemKey = key;
    currentSystem = SYSTEM_DATA[key];

    // Update UI Stats
    document.getElementById("stat-name").innerText = currentSystem.name;
    document.getElementById("stat-formula").innerText = currentSystem.formula;
    document.getElementById("stat-k").innerText = `${currentSystem.k.toFixed(4)} (continuous dispersion parameter)`;
    document.getElementById("stat-r2").innerText = currentSystem.r2.toFixed(4);

    // Clear old objects
    if (starMesh) scene.remove(starMesh);
    if (starGlow) scene.remove(starGlow);
    if (starLabel) scene.remove(starLabel);
    orbitalObjects.forEach(obj => {
        scene.remove(obj.mesh);
        scene.remove(obj.orbitLine);
        if (obj.labelSprite) scene.remove(obj.labelSprite);
        if (obj.ringMesh) scene.remove(obj.ringMesh);
    });
    orbitalObjects = [];

    shellMeshes.forEach(m => scene.remove(m));
    shellMeshes = [];
    predictedShellMeshes.forEach(m => scene.remove(m));
    predictedShellMeshes = [];

    // 1. Central Star / Resonator Core
    const starGeo = new THREE.SphereGeometry(currentSystem.hostSize, 32, 32);
    const starMat = new THREE.MeshBasicMaterial({ color: currentSystem.hostColor });
    starMesh = new THREE.Mesh(starGeo, starMat);
    scene.add(starMesh);

    // Glowing corona
    const glowGeo = new THREE.SphereGeometry(currentSystem.hostSize * 1.5, 32, 32);
    const glowMat = new THREE.MeshBasicMaterial({
        color: currentSystem.hostColor,
        transparent: true,
        opacity: 0.35,
        side: THREE.BackSide
    });
    starGlow = new THREE.Mesh(glowGeo, glowMat);
    scene.add(starGlow);

    // Central body label, raised clear above the glow so it never overlaps the sphere
    starLabel = makeTextSprite(`${currentSystem.hostName} (Central Resonator Core)`, {
        fontsize: 20,
        textColor: { r: 255, g: 214, b: 102, a: 1.0 }
    });
    starLabel.position.set(0, currentSystem.hostSize * 1.5 + 4.0, 0);
    scene.add(starLabel);

    // 2. Build Occupied Standing-Wave Shells & Orbiting Bodies
    currentSystem.bodies.forEach(body => {
        const simR = getSimRadius(body.r, body.n);

        // Translucent 3D Potential Shell
        const shellGeo = new THREE.CylinderGeometry(simR, simR, 1.2, 64, 1, true);
        const shellMat = new THREE.MeshBasicMaterial({
            color: 0x00f0ff,
            transparent: true,
            opacity: 0.12,
            side: THREE.DoubleSide
        });
        const shellMesh = new THREE.Mesh(shellGeo, shellMat);
        scene.add(shellMesh);
        shellMeshes.push(shellMesh);

        // Orbit Line
        const orbitCurve = new THREE.EllipseCurve(0, 0, simR, simR, 0, 2 * Math.PI, false, 0);
        const points = orbitCurve.getPoints(128);
        const orbitGeo = new THREE.BufferGeometry().setFromPoints(points.map(p => new THREE.Vector3(p.x, 0, p.y)));
        const orbitMat = new THREE.LineBasicMaterial({
            color: body.isBelt ? 0xd4a373 : 0x00f0ff,
            transparent: true,
            opacity: body.isBelt ? 0.6 : 0.35
        });
        const orbitLine = new THREE.Line(orbitGeo, orbitMat);
        scene.add(orbitLine);

        // Body Sphere
        let bodyMesh;
        if (body.isBelt) {
            // Asteroid / Debris Ring
            const beltGeo = new THREE.RingGeometry(simR - 1.5, simR + 1.5, 64);
            beltGeo.rotateX(-Math.PI / 2);
            const beltMat = new THREE.MeshBasicMaterial({
                color: 0xaa8855,
                side: THREE.DoubleSide,
                transparent: true,
                opacity: 0.4
            });
            bodyMesh = new THREE.Mesh(beltGeo, beltMat);
        } else {
            const bodyGeo = new THREE.SphereGeometry(body.size, 24, 24);
            const bodyMat = new THREE.MeshStandardMaterial({
                color: body.color,
                roughness: 0.4,
                metalness: 0.2
            });
            bodyMesh = new THREE.Mesh(bodyGeo, bodyMat);
        }
        scene.add(bodyMesh);

        // Label Sprite
        const labelSprite = makeTextSprite(`${body.name} (n=${body.n})`, {
            fontsize: 20,
            textColor: { r: 200, g: 240, b: 255, a: 1.0 }
        });
        scene.add(labelSprite);

        orbitalObjects.push({
            data: body,
            mesh: bodyMesh,
            orbitLine: orbitLine,
            shellMesh: shellMesh,
            labelSprite: labelSprite,
            simR: simR,
            // Keplerian speed: omega proportional to r^(-3/2)
            omega: (2.0 * Math.PI) / (Math.pow(body.n, 1.2) * 10.0),
            angle: Math.random() * Math.PI * 2
        });
    });

    // 3. Build Predicted / Empty Resonant Shells (Amber / Gold)
    if (currentSystem.predictedNodes) {
        const predAngleStep = (Math.PI * 2) / (currentSystem.predictedNodes.length + 1);
        currentSystem.predictedNodes.forEach((pred, predIndex) => {
            const simR = getSimRadius(pred.r, pred.n);
            const predGeo = new THREE.CylinderGeometry(simR, simR, 0.8, 64, 1, true);
            const predMat = new THREE.MeshBasicMaterial({
                color: 0xffd166,
                transparent: true,
                opacity: 0.25,
                side: THREE.DoubleSide
            });
            const pMesh = new THREE.Mesh(predGeo, predMat);
            scene.add(pMesh);

            const orbitCurve = new THREE.EllipseCurve(0, 0, simR, simR, 0, 2 * Math.PI, false, 0);
            const points = orbitCurve.getPoints(128);
            const orbitGeo = new THREE.BufferGeometry().setFromPoints(points.map(p => new THREE.Vector3(p.x, 0, p.y)));
            const orbitMat = new THREE.LineDashedMaterial({
                color: 0xffd166,
                dashSize: 2,
                gapSize: 1.5,
                transparent: true,
                opacity: 0.7
            });
            const pLine = new THREE.Line(orbitGeo, orbitMat);
            pLine.computeLineDistances();
            scene.add(pLine);

            // Position on the ring itself (staggered angle per node) so it never stacks at the origin
            const pLabel = makeTextSprite(`[Predicted] ${pred.name}`, {
                fontsize: 18,
                textColor: { r: 255, g: 209, b: 102, a: 1.0 }
            });
            const labelAngle = predAngleStep * (predIndex + 1);
            pLabel.position.set(simR * Math.cos(labelAngle), 4.0, simR * Math.sin(labelAngle));
            scene.add(pLabel);

            predictedShellMeshes.push(pMesh, pLine, pLabel);
        });
    }

    drawWaveScope();
}

/**
 * Creates 2D text billboard sprite for 3D label rendering
 */
function makeTextSprite(message, parameters) {
    parameters = parameters || {};
    const fontface = parameters.fontface || "Courier New, monospace";
    const fontsize = parameters.fontsize || 22;
    const canvas = document.createElement('canvas');
    canvas.width = 256;
    canvas.height = 64;
    const context = canvas.getContext('2d');
    context.font = "Bold " + fontsize + "px " + fontface;
    
    context.fillStyle = "rgba(10, 20, 35, 0.75)";
    context.strokeStyle = "rgba(72, 202, 228, 0.5)";
    context.lineWidth = 2;
    context.roundRect(4, 4, 248, 56, 8);
    context.fill();
    context.stroke();

    context.fillStyle = `rgba(${parameters.textColor.r},${parameters.textColor.g},${parameters.textColor.b},${parameters.textColor.a})`;
    context.textAlign = "center";
    context.textBaseline = "middle";
    context.fillText(message, 128, 32);

    const texture = new THREE.CanvasTexture(canvas);
    const spriteMaterial = new THREE.SpriteMaterial({ map: texture, transparent: true });
    const sprite = new THREE.Sprite(spriteMaterial);
    sprite.scale.set(12, 3, 1);
    return sprite;
}

/**
 * Draws the 1D radial standing wave profile ψ(r) on the 2D HTML5 Canvas Oscilloscope
 */
function drawWaveScope() {
    const canvas = document.getElementById("wave-canvas");
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    const w = canvas.width;
    const h = canvas.height;

    ctx.clearRect(0, 0, w, h);

    // Grid lines
    ctx.strokeStyle = "rgba(72, 202, 228, 0.15)";
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(0, h / 2);
    ctx.lineTo(w, h / 2);
    ctx.stroke();

    // Standing wave curve: psi(u) = A * sin(kappa * u)
    const kappa = Math.PI / currentSystem.lambda;
    const maxN = currentSystem.bodies[currentSystem.bodies.length - 1].n + 2;

    ctx.strokeStyle = "#48cae4";
    ctx.lineWidth = 2;
    ctx.beginPath();

    for (let x = 0; x < w; x++) {
        const u = (x / w) * (maxN * currentSystem.lambda);
        const psi = Math.sin(kappa * u);
        const y = h / 2 - psi * (h * 0.38);
        if (x === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
    }
    ctx.stroke();

    // Occupied Nodal markers
    currentSystem.bodies.forEach(body => {
        const u = body.n * currentSystem.lambda;
        const x = (u / (maxN * currentSystem.lambda)) * w;
        const y = h / 2;

        ctx.fillStyle = "#00f0ff";
        ctx.shadowColor = "#00f0ff";
        ctx.shadowBlur = 8;
        ctx.beginPath();
        ctx.arc(x, y, 4.5, 0, Math.PI * 2);
        ctx.fill();
        ctx.shadowBlur = 0;

        ctx.fillStyle = "#e0e8f5";
        ctx.font = "9px monospace";
        ctx.fillText(`n=${body.n}`, x - 8, y + 15);
    });

    // Predicted / Empty slots
    if (currentSystem.predictedNodes) {
        currentSystem.predictedNodes.forEach(pred => {
            const u = pred.n * currentSystem.lambda;
            const x = (u / (maxN * currentSystem.lambda)) * w;
            const y = h / 2;

            ctx.fillStyle = "#ffd166";
            ctx.shadowColor = "#ffd166";
            ctx.shadowBlur = 8;
            ctx.beginPath();
            ctx.arc(x, y, 4, 0, Math.PI * 2);
            ctx.fill();
            ctx.shadowBlur = 0;
        });
    }
}

/**
 * Simulation Animation Loop
 */
function animate() {
    requestAnimationFrame(animate);

    if (!isPaused) {
        simTime += 0.015 * simSpeed;

        // Orbit planets
        orbitalObjects.forEach(obj => {
            if (!obj.data.isBelt) {
                obj.angle += obj.omega * 0.015 * simSpeed;
                const x = Math.cos(obj.angle) * obj.simR;
                const z = Math.sin(obj.angle) * obj.simR;
                obj.mesh.position.set(x, 0, z);

                if (obj.labelSprite) {
                    obj.labelSprite.position.set(x, obj.data.size + 2.5, z);
                }
            }
        });

        updateCymaticMesh(simTime);
    }

    // Toggle Visibility Layers
    const showWaves = document.getElementById("toggle-standing-waves").checked;
    const showPred = document.getElementById("toggle-predicted-shells").checked;
    const showOrbits = document.getElementById("toggle-orbits").checked;
    const showLabels = document.getElementById("toggle-labels").checked;

    shellMeshes.forEach(m => m.visible = showWaves);
    predictedShellMeshes.forEach(m => m.visible = showPred);
    orbitalObjects.forEach(obj => {
        obj.orbitLine.visible = showOrbits;
        if (obj.labelSprite) obj.labelSprite.visible = showLabels;
    });
    if (starLabel) starLabel.visible = showLabels;

    controls.update();
    renderer.render(scene, camera);
}

/**
 * Screenshot Capture (One-Click High-Res PNG)
 */
function takeScreenshot() {
    renderer.render(scene, camera);
    const dataURL = renderer.domElement.toDataURL("image/png");
    const link = document.createElement("a");
    const timestamp = new Date().toISOString().replace(/[:.]/g, "-");
    link.download = `eigenmode-simulation-${currentSystemKey}-${timestamp}.png`;
    link.href = dataURL;
    link.click();
}

/**
 * Video Recording Engine (HTML5 MediaRecorder API)
 */
function toggleVideoRecording() {
    const recordBtn = document.getElementById("btn-record");
    const statusBox = document.getElementById("recording-status");
    const timerText = document.getElementById("recording-timer");

    if (!isRecording) {
        // Start Recording
        recordedChunks = [];
        const canvas = renderer.domElement;
        const stream = canvas.captureStream(60); // 60 FPS capture

        const mimeTypes = [
            'video/webm;codecs=vp9',
            'video/webm;codecs=vp8',
            'video/webm',
            'video/mp4'
        ];
        let selectedMime = mimeTypes.find(t => MediaRecorder.isTypeSupported(t)) || 'video/webm';

        mediaRecorder = new MediaRecorder(stream, { mimeType: selectedMime });

        mediaRecorder.ondataavailable = function(e) {
            if (e.data.size > 0) {
                recordedChunks.push(e.data);
            }
        };

        mediaRecorder.onstop = function() {
            const blob = new Blob(recordedChunks, { type: selectedMime });
            const url = URL.createObjectURL(blob);
            const a = document.createElement("a");
            const timestamp = new Date().toISOString().replace(/[:.]/g, "-");
            a.href = url;
            a.download = `eigenmode-orbit-simulation-${currentSystemKey}-${timestamp}.webm`;
            a.click();
            window.URL.revokeObjectURL(url);
        };

        mediaRecorder.start();
        isRecording = true;
        recordStartTime = Date.now();
        recordBtn.innerText = "⏹ Stop Recording";
        recordBtn.classList.add("recording");
        statusBox.classList.remove("hidden");

        recordTimerInterval = setInterval(() => {
            const elapsedSec = Math.floor((Date.now() - recordStartTime) / 1000);
            const mins = String(Math.floor(elapsedSec / 60)).padStart(2, '0');
            const secs = String(elapsedSec % 60).padStart(2, '0');
            timerText.innerText = `${mins}:${secs}`;
        }, 500);

    } else {
        // Stop Recording
        mediaRecorder.stop();
        isRecording = false;
        clearInterval(recordTimerInterval);
        recordBtn.innerText = "🎥 Start Video Recording";
        recordBtn.classList.remove("recording");
        statusBox.classList.add("hidden");
    }
}

/**
 * Event Listeners & Camera Controls
 */
function initEventListeners() {
    window.addEventListener("resize", () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    });

    document.getElementById("system-select").addEventListener("change", (e) => {
        loadSystem(e.target.value);
    });

    document.getElementById("speed-slider").addEventListener("input", (e) => {
        simSpeed = parseFloat(e.target.value);
        document.getElementById("speed-val").innerText = `${simSpeed.toFixed(1)}x`;
    });

    document.getElementById("btn-pause").addEventListener("click", () => {
        isPaused = !isPaused;
        document.getElementById("btn-pause").innerText = isPaused ? "▶ Resume" : "⏸ Pause";
    });

    document.getElementById("btn-reset").addEventListener("click", () => {
        simTime = 0;
        orbitalObjects.forEach(obj => obj.angle = 0);
    });

    document.getElementById("toggle-log-scale").addEventListener("change", (e) => {
        useLogScale = e.target.checked;
        loadSystem(currentSystemKey);
    });

    // Camera views
    document.getElementById("cam-perspective").addEventListener("click", () => {
        camera.position.set(0, 75, 110);
        controls.target.set(0, 0, 0);
    });

    document.getElementById("cam-top").addEventListener("click", () => {
        camera.position.set(0, 150, 0.01);
        controls.target.set(0, 0, 0);
    });

    document.getElementById("cam-edge").addEventListener("click", () => {
        camera.position.set(0, 2, 130);
        controls.target.set(0, 0, 0);
    });

    // Capture buttons
    document.getElementById("btn-screenshot").addEventListener("click", takeScreenshot);
    document.getElementById("btn-record").addEventListener("click", toggleVideoRecording);

    // Video modal controls
    const videoModal = document.getElementById("video-modal");
    const videoPlayer = document.getElementById("sim-video-player");
    document.getElementById("btn-watch-mp4").addEventListener("click", () => {
        videoModal.classList.remove("hidden");
        videoPlayer.currentTime = 0;
        videoPlayer.play();
    });

    document.getElementById("btn-close-modal").addEventListener("click", () => {
        videoModal.classList.add("hidden");
        videoPlayer.pause();
    });

    videoModal.addEventListener("click", (e) => {
        if (e.target === videoModal) {
            videoModal.classList.add("hidden");
            videoPlayer.pause();
        }
    });
}

window.onload = init;
