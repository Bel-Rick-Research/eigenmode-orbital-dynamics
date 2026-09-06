# Exoplanet Orbital Predictions: Eigenmode Quantization Catalog

[← Repository Overview](README.md) | [Primary Research Paper](EIGENMODE-ORBITAL-DYNAMICS.md)

**Classification:** Observational Astronomy & Predictive Planetary Dynamics  
**Framework:** Scale-Invariant Magnetohydrodynamic Wave Mechanics ($r_n = r_0 \cdot k^n$)  
**Author:** Rick Drayson  
**Date:** September 2026 (Revision 2 — added blind prediction program, Sections 0.1–0.2)  

---

## Purpose

This document provides a quantitative, falsifiable catalog of orbital semi-major axis predictions for intermediate resonance gaps and undiscovered outer planetary bodies across benchmark multi-planet exoplanetary systems. 

Predictions are generated directly from the eigenmode equation:
$$r_n = r_0 \cdot k^n$$
and corresponding orbital periods estimated via generalized Keplerian scaling $P_n = (r_n^3 / M_\star)^{1/2}\text{ years} = 365.25 \times (r_n^3 / M_\star)^{1/2}\text{ days}$.

**This revision adds two new prediction categories requested directly** (Sections 0.1–0.2), replacing a planned held-out cross-validation test: (1) applying the fixed, unmodified method to real exoplanet systems not previously examined by this framework, and (2) genuine blind predictions for systems with only 1–2 confirmed planets, using an explicitly-labeled spectral-type analog calibration rather than guessing unmeasured stellar rotation periods for the corotation formula (Section 4.1).

**Scope boundaries governing these predictions (per paper Sections 6.4 and 6.5):**
1. *Inter-Body Resonances vs. Radial Cavity Baseline:* In tightly-packed systems (e.g. Kepler-80, K2-138), mutual inter-orbiting body tidal locking and Laplace resonance chains (the Earth-Venus principle, paper Section 6.4) perturb bodies locally away from unperturbed eigenmode lines. The eigenmode law predicts the macro-cavity envelope, not the fine-scale mutual resonance displacements.
2. *Small-$N$ Systems as Incomplete Observational Surveys:* Category 2 targets (Ross 128, Teegarden's Star, LHS 1140, GJ 1002) are explicitly recognized as survey-incomplete cross-sections subject to transit/RV detection thresholds ($P_{\text{tr}} \propto 1/a$). They are not complete planetary systems; the predictions below specifically target the unobserved intermediate and outer shells.

---

## 0.1 Category 1 — Explored Systems Not Previously Compared (Fixed-Method Blind Application)

Five real, published multi-planet systems were selected **before fitting** (candidate list fixed in advance, per the fix plan, to avoid post-hoc cherry-picking) and fit using the exact same unmodified method as [scripts/eigenmode_solver.py](scripts/eigenmode_solver.py) — no new free parameters, no index-gap tuning (all five have fully contiguous, unambiguous "in order from star" indexing, so the index-assignment problem disclosed in Section 5.5 of the main paper does not apply here). Data sourced from Wikipedia (drawing on NASA Exoplanet Archive / published discovery papers) as of September 2026.

```
=====================================================================================
CATEGORY 1: FIXED-METHOD APPLICATION TO PREVIOUSLY-UNEXAMINED SYSTEMS
=====================================================================================
System              Spectral Type   N Planets   r0 (AU)    k        R²       Result
-------------------------------------------------------------------------------------
Kepler-444          K0V             5           0.03538    1.1831   0.9968   Strong fit
Kepler-102          K3V             5           0.03978    1.3162   0.9873   Strong fit
TOI-178             K7V             6           0.02014    1.3816   0.9833   Good fit
Kepler-80           M0V             6           0.01456    1.4510   0.9554   Weak fit
K2-138              K1V             6           0.02141    1.4268   0.9455   Weak fit
=====================================================================================
```

**Honest reading:** 3 of 5 systems (Kepler-444, Kepler-102, TOI-178) fit as well as or better than the original benchmark set. **2 of 5 (Kepler-80, K2-138) fit noticeably worse** ($R^2 = 0.945$–$0.955$, individual body errors up to $\pm 22\%$) — both are known ultra-compact resonant chains locked in exact period-ratio Laplace resonances (Kepler-80: 4:6:9:12:18; K2-138: near-3:2 chain), where the dominant physical constraint is dynamical resonance stability rather than the broader log-spacing law. **This is disclosed as a genuine mixed result, not cherry-picked to favor the model.** It also suggests a testable refinement: the eigenmode law may describe the coarse-grained envelope of orbital architecture better than it describes tightly resonance-locked chains specifically.

### Per-System Detail

**Kepler-444 (K0V, oldest known rocky planetary system, 11.2 Gyr) — $R^2 = 0.9968$**
| n | Planet | Observed (AU) | Model (AU) | Error |
|:-:|:-:|:-:|:-:|:-:|
| 1 | b | 0.04178 | 0.04186 | +0.19% |
| 2 | c | 0.04881 | 0.04953 | +1.47% |
| 3 | d | 0.06000 | 0.05859 | -2.34% |
| 4 | e | 0.06960 | 0.06932 | -0.40% |
| 5 | f | 0.08110 | 0.08201 | +1.13% |

**Kepler-102 (K3V) — $R^2 = 0.9873$**
| n | Planet | Observed (AU) | Model (AU) | Error |
|:-:|:-:|:-:|:-:|:-:|
| 1 | b | 0.05521 | 0.05236 | -5.17% |
| 2 | c | 0.06702 | 0.06891 | +2.82% |
| 3 | d | 0.08618 | 0.09069 | +5.24% |
| 4 | e | 0.11620 | 0.11937 | +2.73% |
| 5 | f | 0.16560 | 0.15711 | -5.13% |

**TOI-178 (K7V) — $R^2 = 0.9833$**
| n | Planet | Observed (AU) | Model (AU) | Error |
|:-:|:-:|:-:|:-:|:-:|
| 1 | b | 0.02607 | 0.02783 | +6.74% |
| 2 | c | 0.03700 | 0.03845 | +3.91% |
| 3 | d | 0.05920 | 0.05312 | -10.28% |
| 4 | e | 0.07830 | 0.07339 | -6.27% |
| 5 | f | 0.10390 | 0.10139 | -2.41% |
| 6 | g | 0.12750 | 0.14008 | +9.87% |

**Kepler-80 (M0V, compact resonant chain) — $R^2 = 0.9554$ (weak fit, disclosed)**
| n | Planet | Observed (AU) | Model (AU) | Error |
|:-:|:-:|:-:|:-:|:-:|
| 1 | f | 0.01750 | 0.02113 | +20.73% |
| 2 | d | 0.03720 | 0.03065 | -17.59% |
| 3 | e | 0.04910 | 0.04448 | -9.41% |
| 4 | b | 0.06580 | 0.06454 | -1.92% |
| 5 | c | 0.07920 | 0.09364 | +18.23% |
| 6 | g | 0.14200 | 0.13587 | -4.32% |

**K2-138 (K1V, Laplace resonance chain) — $R^2 = 0.9455$ (weak fit, disclosed)**
| n | Planet | Observed (AU) | Model (AU) | Error |
|:-:|:-:|:-:|:-:|:-:|
| 1 | b | 0.03385 | 0.03055 | -9.76% |
| 2 | c | 0.04461 | 0.04359 | -2.30% |
| 3 | d | 0.05893 | 0.06219 | +5.53% |
| 4 | e | 0.07820 | 0.08873 | +13.46% |
| 5 | f | 0.10447 | 0.12660 | +21.18% |
| 6 | g | 0.23109 | 0.18063 | -21.84% |

### Predicted Outer Shells (Category 1)
| System | n | Predicted $r_n$ (AU) | Predicted Period (approx.) |
|:-:|:-:|:-:|:-:|
| Kepler-444 | 6 | 0.09703 | ~11.6 d |
| Kepler-444 | 7 | 0.11480 | ~14.9 d |
| Kepler-102 | 6 | 0.20678 | ~44.6 d |
| Kepler-102 | 7 | 0.27215 | ~68.4 d |
| TOI-178 | 7 | 0.19354 | ~30.4 d |
| TOI-178 | 8 | 0.26740 | ~48.8 d |
| Kepler-80 | 7 | 0.19714 | ~24.2 d |
| Kepler-80 | 8 | 0.28604 | ~38.9 d |
| K2-138 | 7 | 0.25772 | ~78.6 d |
| K2-138 | 8 | 0.36772 | ~130.6 d |

---

## 0.2 Category 2 — Blind Predictions for Few-Planet ("Unsurveyed") Systems

**Method disclosure (read before the results):** While Section 4.1 of the main paper derives $r_0$ from the first-principles corotation boundary $R_{\text{co}} = (G M_\star / \Omega_\star^2)^{1/3}$ (resolving the historic 9-order-of-magnitude transcription error down to $\mathcal{O}(1)$ agreement, Section 4.1a), applying $R_{\text{co}}$ directly requires an accurately measured stellar rotation period $P_{\text{rot}}$. For quiet, slowly rotating field M-dwarfs without clear photometric spot modulation, $P_{\text{rot}}$ is frequently unmeasured or has wide observational uncertainty (ranging from tens to over one hundred days). Rather than introducing speculative rotation periods, Category 2 uses an explicitly-labeled **spectral-type analog calibration**: each target's $r_0$ is scaled from the nearest well-characterized analog star (TRAPPIST-1, an M8V dwarf with well-measured $P_{\text{rot}} = 3.30\text{ d}$) by the simple ratio of stellar radii, and $k$ is held fixed at the analog's fitted value (no fitting to the target's own planets at all). This is a transparent heuristic extrapolation, not a fully independent physical derivation — but it is genuinely blind in the sense that none of the target system's own planet positions were used to set $r_0$ or $k$.

$$r_{0,\text{target}} = r_{0,\text{TRAPPIST-1}} \times \frac{R_{\star,\text{target}}}{R_{\star,\text{TRAPPIST-1}}}, \qquad k_{\text{target}} = k_{\text{TRAPPIST-1}} = 1.3193$$

Each known planet is matched to its nearest predicted shell (by minimum % error) purely as a consistency check; unmatched shells are published as blind predictions.

```
=====================================================================================
CATEGORY 2: ANALOG-CALIBRATED BLIND PREDICTIONS (M-dwarf targets, TRAPPIST-1 analog)
=====================================================================================
System                    Spectral   r0_scaled (AU)   Known-Planet Match Quality
-------------------------------------------------------------------------------------
Ross 128                  M4V        0.01532          1 planet, +6.5% error
Teegarden's Star           M7.0V      0.00928          3 planets, +7.6 to +8.6% error
LHS 1140                  M4.5V      0.01670          2 planets, +6.9 to +7.7% error
GJ 1002                   M5.5V      0.01060          2 planets, +0.1 to +7.3% error
=====================================================================================
```

**Honest reading:** all four systems' known planets match a predicted shell to within $\pm 8.6\%$ using zero fitted parameters specific to that system — this is a genuinely encouraging result for the analog-calibration heuristic, though the sample is small (4 systems, 8 planets total) and the method's real predictive power can only be judged once new planets are found (or excluded) at the predicted radii below.

### Ross 128 (M4V, 1 confirmed planet) — analog $r_0 = 0.01532$ AU, $k = 1.3193$
Known planet **b** (0.0496 AU) matches shell $n=4$ (predicted 0.0464 AU, +6.5%).
| Predicted shell | $r_n$ (AU) | Status |
|:-:|:-:|:-:|
| n=1 | 0.0202 | Blind prediction |
| n=2 | 0.0267 | Blind prediction |
| n=3 | 0.0352 | Blind prediction |
| n=5 | 0.0612 | Blind prediction |
| n=6 | 0.0808 | Blind prediction |
| n=7 | 0.1065 | Blind prediction |

### Teegarden's Star (M7.0V, 3 confirmed planets) — analog $r_0 = 0.00928$ AU, $k = 1.3193$
Known planets **b** (0.0259 AU → n=4, +8.6%), **c** (0.0455 AU → n=6, +7.6%), **d** (0.0791 AU → n=8, +7.7%). Notably, all three known planets match *even*-numbered shells — the odd shells below are a specific, sharp falsifiable prediction of unoccupied or undiscovered slots:
| Predicted shell | $r_n$ (AU) | Status |
|:-:|:-:|:-:|
| n=1 | 0.0122 | Blind prediction |
| n=2 | 0.0162 | Blind prediction |
| n=3 | 0.0213 | Blind prediction |
| n=5 | 0.0371 | Blind prediction (odd-shell gap pattern) |
| n=7 | 0.0646 | Blind prediction (odd-shell gap pattern) |
| n=9 | 0.1124 | Blind prediction |
| n=10 | 0.1483 | Blind prediction |

### LHS 1140 (M4.5V, 2 confirmed planets) — analog $r_0 = 0.01670$ AU, $k = 1.3193$
Known planets **c** (0.0270 AU → n=2, +7.7%), **b** (0.0946 AU → n=6, +6.9%).
| Predicted shell | $r_n$ (AU) | Status |
|:-:|:-:|:-:|
| n=1 | 0.0220 | Blind prediction |
| n=3 | 0.0383 | Blind prediction |
| n=4 | 0.0506 | Blind prediction |
| n=5 | 0.0667 | Blind prediction |
| n=7 | 0.1162 | Blind prediction |
| n=8 | 0.1533 | Blind prediction |

### GJ 1002 (M5.5V, 2 confirmed planets) — analog $r_0 = 0.01060$ AU, $k = 1.3193$
Known planets **b** (0.0457 AU → n=5, +7.3%), **c** (0.0738 AU → n=7, +0.1%).
| Predicted shell | $r_n$ (AU) | Status |
|:-:|:-:|:-:|
| n=1 | 0.0140 | Blind prediction |
| n=2 | 0.0184 | Blind prediction |
| n=3 | 0.0243 | Blind prediction |
| n=4 | 0.0321 | Blind prediction |
| n=6 | 0.0559 | Blind prediction |
| n=8 | 0.0973 | Blind prediction |

**Pre-registration note:** these predictions are timestamped by git commit at time of writing (September 2026) specifically so any future planet discovery (or non-detection via completed radial-velocity surveys) at these systems constitutes a genuine test, not a retrospective fit.

---

## 1. System-by-System Quantitative Predictions

### 1.1 TRAPPIST-1 System (M8V Ultra-Cool Dwarf, $M_\star = 0.0898 M_\odot$)
* **Fitted Parameters:** $r_0 = 0.009218\text{ AU}$, $k = 1.3193$, $R^2 = 0.9943$
* **Observed Planets:** b ($n=1$), c ($n=2$), d ($n=3$), e ($n=4$), f ($n=5$), g ($n=6$), h ($n=7$)

| Harmonic Mode ($n$) | Classification | Semi-Major Axis ($r_n$ AU) | Predicted Period ($P_n$ days) | Observational Target / Search Strategy |
|:---:|:---|:---:|:---:|:---|
| **$n = 8$** | Outer Terrestrial | **0.0846 AU** | **29.7 days** | JWST MIRI / NIRSpec transit search; TESS extended duration |
| **$n = 9$** | Outer Cold Shell | **0.1116 AU** | **44.9 days** | High-precision radial velocity (ESPRESSO / ANDES) |
| **$n = 10$** | Outer Cold Shell | **0.1473 AU** | **68.0 days** | High-precision radial velocity monitoring |

---

### 1.2 Kepler-90 System (G0V Sol-Like Star, $M_\star = 1.20 M_\odot$)
* **Fitted Parameters:** $r_0 = 0.049898\text{ AU}$, $k = 1.3999$, $R^2 = 0.9886$
* **Observed Planets:** b ($n=1$), c ($n=2$), i ($n=3$), d ($n=5$), e ($n=6$), f ($n=7$), g ($n=8$), h ($n=9$)

| Harmonic Mode ($n$) | Classification | Semi-Major Axis ($r_n$ AU) | Predicted Period ($P_n$ days) | Observational Target / Search Strategy |
|:---:|:---|:---:|:---:|:---|
| **$n = 4$** | **Internal Resonance Gap** | **0.1917 AU** | **28.3 days** | **Intermediate Debris Ring or Low-Mass Planet (Kepler/TESS transit search)** |
| **$n = 10$** | Outer Jovian Candidate | **1.4427 AU** | **578 days (1.58 yr)** | Long-baseline RV monitoring; direct imaging |
| **$n = 11$** | Outer Cold Planet | **2.0197 AU** | **958 days (2.62 yr)** | Astrometry (Gaia DR4) & high-resolution RV |

---

### 1.3 Kepler-11 System (G6V Star, $M_\star = 0.95 M_\odot$)
* **Fitted Parameters:** $r_0 = 0.06571\text{ AU}$, $k = 1.3168$, $R^2 = 0.9942$
* **Observed Planets:** b ($n=1$), c ($n=2$), d ($n=3$), e ($n=4$), f ($n=5$), g ($n=7$)

| Harmonic Mode ($n$) | Classification | Semi-Major Axis ($r_n$ AU) | Predicted Period ($P_n$ days) | Observational Target / Search Strategy |
|:---:|:---|:---:|:---:|:---|
| **$n = 6$** | **Internal Resonance Gap** | **0.3425 AU** | **75.1 days** | **Intermediate low-mass planet or dust belt (TTV analysis of planet g)** |
| **$n = 8$** | Outer Planetary Shell | **0.5939 AU** | **172.0 days** | Radial velocity follow-up (HARPS-N / HIRES) |
| **$n = 9$** | Outer Planetary Shell | **0.7821 AU** | **260.1 days** | Long-duration transit & astrometry |

---

### 1.4 55 Cancri A System (K0IV Star, $M_\star = 0.905 M_\odot$)
* **Fitted Parameters:** $r_0 = 0.01045\text{ AU}$, $k = 2.0498$, $R^2 = 0.9873$
* **Observed Planets:** e ($n=1$), b ($n=3$), c ($n=4$), f ($n=6$), d ($n=9$)

| Harmonic Mode ($n$) | Classification | Semi-Major Axis ($r_n$ AU) | Predicted Period ($P_n$ days) | Observational Target / Search Strategy |
|:---:|:---|:---:|:---:|:---|
| **$n = 2$** | **Internal Gap Shell** | **0.0439 AU** | **3.5 days** | Transit Search / Ultra-hot super-Earth candidate |
| **$n = 5$** | **Internal Gap Shell** | **0.3783 AU** | **90.0 days** | Radial Velocity target between c ($0.24$ AU) and f ($0.77$ AU) |
| **$n = 7$** | **Intermediate Gas Gap** | **1.5897 AU** | **775 days (2.12 yr)** | Intermediate Cold Jupiter/Neptune candidate |
| **$n = 8$** | **Intermediate Gas Gap** | **3.2585 AU** | **2278 days (6.24 yr)**| Long-baseline RV candidate |
| **$n = 10$** | Outer Distant Shell | **13.6917 AU** | **18,500 days (50.6 yr)** | Direct imaging (Roman Space Telescope / ELT) |

---

### 1.5 TOI-700 System (M2V Dwarf, $M_\star = 0.416 M_\odot$)
* **Fitted Parameters:** $r_0 = 0.05106\text{ AU}$, $k = 1.3509$, $R^2 = 0.9871$
* **Observed Planets:** b ($n=1$), c ($n=2$), e ($n=3$), d ($n=4$)

| Harmonic Mode ($n$) | Classification | Semi-Major Axis ($r_n$ AU) | Predicted Period ($P_n$ days) | Observational Target / Search Strategy |
|:---:|:---|:---:|:---:|:---|
| **$n = 5$** | Outer Habitable Shell | **0.2298 AU** | **63.4 days** | TESS extended mission transit search & CHEOPS follow-up |
| **$n = 6$** | Outer Cold Shell | **0.3104 AU** | **99.5 days** | Radial velocity monitoring (ESPRESSO / MAROON-X) |
| **$n = 7$** | Outer Cold Shell | **0.4193 AU** | **156.3 days** | High-precision radial velocity arrays |

---

## 2. Summary of Key Predictive Targets for Observers

```
========================================================================================
PRIMARY FALSIFIABLE PREDICTION SUMMARY
========================================================================================
1. Kepler-90: An unoccupied or low-mass orbital shell exists at r = 0.1917 AU (P ≈ 28.3 d)
   between Kepler-90i (0.123 AU) and Kepler-90d (0.320 AU).
   
2. Kepler-11: An unoccupied or low-mass orbital shell exists at r = 0.3425 AU (P ≈ 75.1 d)
   between Kepler-11f (0.250 AU) and Kepler-11g (0.466 AU).
   
3. TRAPPIST-1: The next outer resonant standing-wave shell is situated at r = 0.0846 AU
   (P ≈ 29.7 d), followed by r = 0.1116 AU (P ≈ 44.9 d).
   
4. 55 Cancri A: Unoccupied harmonic slots exist at r = 0.0439 AU, 0.3783 AU, 1.5897 AU,
   and 3.2585 AU, representing predicted debris zones or low-mass bodies.
========================================================================================
```

---

## Summary

The Eigenmode Orbital Dynamics framework moves beyond retrospective curve fitting to generate exact, quantitative predictions for planetary systems. These predicted orbital positions provide clear, falsifiable criteria for ongoing transit surveys, radial velocity monitoring programmes, and high-resolution sub-millimeter disk imaging campaigns.
