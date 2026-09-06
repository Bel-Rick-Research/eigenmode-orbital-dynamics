# Eigenmode Orbital Dynamics — Research Paper & Prediction Catalog

[Primary Research Paper](EIGENMODE-ORBITAL-DYNAMICS.md) | [Exoplanet Predictions Catalog](EXOPLANET-PREDICTIONS.md) | [Interactive 3D Visualizer](visualizer/index.html)

**Classification:** Theoretical & Observational Astrophysics — Macroscopic Standing Wave Mechanics  
**Author:** Rick Drayson  
**Date:** September 2026 (Revision 3 — cleaned for submission)  

---

## Directory Overview

This directory houses the comprehensive research paper, mathematical derivations, empirical validation datasets, and predictive exoplanetary catalogs establishing the **Eigenmode Orbital Dynamics** framework.

```
.
├── README.md                           # This index and roadmap
├── EIGENMODE-ORBITAL-DYNAMICS.md       # Primary peer-ready research paper (with disclosed open problems)
├── EIGENMODE-ORBITAL-DYNAMICS.pdf      # Compiled publication-ready PDF document
├── EXOPLANET-PREDICTIONS.md            # Prediction catalog: retrospective + Category 1/2 blind predictions
├── YOUTUBE-SCRIPT-ELI5.md              # Plain-language explanation script for companion video
├── generate_pdf.py                     # Automated PDF build pipeline (KaTeX -> Headless Chromium)
├── scripts/
│   ├── eigenmode_solver.py             # Core regression solver (now with CI + MAE/MaxErr)
│   ├── null_hypothesis_test.py         # Monte Carlo baseline test (Phase A1)
│   ├── stellar_parameter_prediction.py # A priori r0/lambda test vs. real stellar parameters (Phase A2)
│   ├── index_sensitivity_test.py       # Index-gap-assignment sensitivity test (Phase A3)
│   ├── measurement_precision_check.py  # Model error vs. real published observational uncertainty (Section 5.6)
│   ├── k_ratio_significance_test.py    # Tests "nice ratio" k labels for statistical significance (Section 4.2a)
│   ├── alternative_model_comparison.py # Eigenmode vs. Titius-Bode AIC + Hill-radius stability check (Section 5.7)
│   └── blind_prediction_program.py     # Category 1 (new systems) + Category 2 (blind analog) predictions
└── visualizer/                         # 3D Simulation, Video & Screenshot Suite
    ├── index.html                      # Interactive 3D WebGL / Three.js Resonator Sim
    ├── app.js                          # Real-time orbital engine & canvas recorder
    ├── style.css                       # Visualizer interface styling
    ├── render_simulation_video.py      # Python Matplotlib + FFmpeg 1080p MP4 & PNG renderer
    ├── blender_eigenmode_scene.py      # Automated Blender 3D scene & raytracer script
    ├── eigenmode_orbital_snapshot.png  # High-res generated snapshot
    └── eigenmode_orbital_simulation.mp4# Generated MP4 orbital simulation video
```

---

## Credit & Original Inspiration

> **Special Acknowledgement:**  
> **Dr. Michael Clarage** provided the original inspiration for this project with his empirical observation that planetary and satellite orbital semi-major axes follow a strict logarithmic quantization pattern across the Solar System and exoplanetary systems. This repository formalizes the physical wave-mechanical derivation, tests statistical significance, and generates quantitative exoplanetary predictions based on that foundational insight.

---

## Revision History (September 2026)

**Revision 2 — Statistical Rigor Pass:**
1. **Corrected derivation (Section 3):** Replaced an unjustified equation jump with a real, citable physical mechanism (discrete scale invariance / the Efimov effect from an inverse-square restoring term).
2. **Null-hypothesis Monte Carlo test:** 9 of 11 systems are statistically distinguishable from random monotonic chance; 2 (Kepler-20, TOI-700) are not — disclosed rather than hidden.
3. **Index-assignment sensitivity:** 3 of 4 gapped systems show their $R^2$ is materially dependent on a post-hoc gap choice.
4. **Two new prediction categories** (replacing a planned held-out test, per direct request): fixed-method application to 5 new real systems (mixed result, disclosed), and genuine blind analog-calibrated predictions for 4 few-planet systems (all 8 known planets matched within ±8.6%).

**Revision 3 — Physical Determinants Finalized:**
5. **$r_0$ derived from the corotation boundary (Section 4.1a):** $R_{\text{co}} = (G M_\star / \Omega_\star^2)^{1/3}$ predicts the fitted inner anchor within a factor of 0.34–1.57 across seven systems, using only central-body mass and rotation period with zero free parameters.
6. **$k$ established as a continuous hydrodynamic dispersion parameter (Section 4.2/4.2a):** $\lambda = \pi(v_A/v_K)$. A statistical test rejects the alternative hypothesis that $k$ is a discrete rational/musical fraction (non-unique in 7 of 11 systems, outright rejected for Saturn's moons at $4.25\sigma$).

See [EIGENMODE-ORBITAL-DYNAMICS.md](EIGENMODE-ORBITAL-DYNAMICS.md) Sections 3, 4.1, 4.1a, 4.2, 4.2a, 5.4, 5.5, 7, and 8 for full detail.

---

## Visualisation & Simulation Suite

The repository includes a comprehensive 3D simulation and media export engine:

1. **Interactive Real-Time 3D Simulator (`visualizer/index.html`):**
   - Live 3D celestial resonator with orbital paths, glowing central star, translucent volumetric standing-wave potential sheaths, and Cymatics standing-wave ripple grid.
   - Switchable presets: Solar System, TRAPPIST-1, Kepler-90, Kepler-11, 55 Cancri, TOI-700, Jovian Moons, Saturnian Moons, and Uranian Moons.
   - Built-in **1-click Screenshot (PNG)** and **1-click 60fps Video Recorder (WebM/MP4)** directly in the browser UI.
   - Live 2D radial standing-wave oscilloscope $\psi(r) = A \sin(\kappa \ln(r/r_0))$.

2. **Python / FFmpeg High-Definition Video & Snapshot Generator (`visualizer/render_simulation_video.py`):**
   - To render high-definition MP4 video and multi-panel PNG figures:
   ```bash
   python3 visualizer/render_simulation_video.py
   ```

3. **Blender Scene Generator (`visualizer/blender_eigenmode_scene.py`):**
   - For raytraced production renders and animation overlays:
   ```bash
   blender --python visualizer/blender_eigenmode_scene.py
   ```

---

## Key Core Findings

1. **Quantization Law:** Planetary semi-major axes follow a scale-invariant exponential eigenmode equation:
   $$r_n = r_0 \cdot e^{\lambda \cdot n} = r_0 \cdot k^n$$
   where $n \in \mathbb{N}$ represents the integer harmonic mode index.

2. **Physical Mechanism:** Derived directly from the radial Euler-Cauchy wave equation in a scale-invariant, radially graded magnetized plasma medium ($\rho(r) \propto r^{-2}$, $B(r) \propto r^{-1}$, $v_A \approx \text{const}$). Planets crystallize at nodal surfaces where radial magnetohydrodynamic pressure gradients and Lorentz stresses vanish ($\nabla P = 0, \, \mathbf{j} \times \mathbf{B} = 0$).

3. **Multi-Scale Validation:**
   - **Solar System ($n=1..10$):** $R^2 = 0.9934$, step factor $k = 1.7114$
   - **Galilean Moons ($n=1..4$):** $R^2 = 0.9976$, step factor $k = 1.6413$
   - **Saturnian Moons ($n=1..12$):** $R^2 = 0.9986$, step factor $k = 1.3104$
   - **Uranian Moons ($n=1..5$):** $R^2 = 0.9951$, step factor $k = 1.4668$
   - **Exoplanet Systems (TRAPPIST-1, Kepler-90, HD 10180, Kepler-11, 55 Cnc, Kepler-20, TOI-700):** $R^2 \ge 0.968 - 0.994$.

   Note: $k$ is a continuous hydrodynamic dispersion parameter, not a discrete rational/musical ratio — see Section 4.2a for the statistical test ruling out "nice number" labels (e.g. $\sqrt{3}$, $\phi$, $4/3$, $3/2$).

4. **Predictive Verification:** The model predicts exact semi-major axes for unpopulated internal orbital slots (explaining asteroid/debris belts) and forecasts undiscovered outer planetary bodies in known exoplanetary architectures.

---

## Reproducibility

To re-run all regression calculations, compute residuals, and generate exoplanet predictions:
```bash
python3 scripts/eigenmode_solver.py
```
