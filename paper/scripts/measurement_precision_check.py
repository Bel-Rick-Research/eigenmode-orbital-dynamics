#!/usr/bin/env python3
"""
Measurement Precision Check — Eigenmode Orbital Dynamics
Rick Drayson | Statistical Rigor Validation (Section 5.6)

PURPOSE
-------
Model residuals reported throughout this paper (Sections 5.1-5.3, 7.1) compare
predicted semi-major axes against a single "observed" value with no reference to
that value's own published measurement uncertainty. A 5% model residual is a real
physical disagreement if the observation is known to +/-1%, but is statistically
meaningless if the observation itself carries a +/-20% uncertainty.

This script compares |model error %| against the actual published +/- uncertainty
(sigma_r / r_obs, as percent) for every system where such uncertainties are
available in the primary literature / NASA Exoplanet Archive / Wikipedia infoboxes.

Two categories are computed differently, deliberately:
  1. Fitted systems (original 11-system set + Category 1): model r0, k are fit
     to the system's own data, then compared per-body against sigma_obs.
  2. Category 2 blind analog predictions: r0 is scaled from the TRAPPIST-1
     analog (NOT fit to the target's own planets) and k is held fixed; residuals
     are computed against that fixed prediction, not a fresh per-system fit.
     (Fitting a fresh 2-parameter model to systems with only 1-3 known planets
     is statistically degenerate and was avoided here for exactly that reason.)
"""

import numpy as np

def fit_full(n_arr, r_arr):
    n_arr = np.array(n_arr, dtype=float)
    ln_r = np.log(r_arr)
    p = np.polyfit(n_arr, ln_r, 1)
    lam, ln_r0 = p[0], p[1]
    r0 = np.exp(ln_r0)
    k = np.exp(lam)
    r_pred = r0 * (k ** n_arr)
    err = (r_pred - r_arr) / r_arr * 100.0
    return r_pred, err

# name: (planet_names, n, r_obs [AU], sigma_obs [AU])
FITTED_SYSTEMS = {
    'Kepler-90': (['b', 'c', 'i', 'd', 'e', 'f', 'g', 'h'], [1, 2, 3, 5, 6, 7, 8, 9],
                  [0.074, 0.089, 0.107, 0.32, 0.42, 0.48, 0.71, 1.01],
                  [0.016, 0.012, 0.03, 0.05, 0.06, 0.09, 0.08, 0.11]),
    'Kepler-11': (['b', 'c', 'd', 'e', 'f', 'g'], [1, 2, 3, 4, 5, 7],
                  [0.091, 0.107, 0.155, 0.195, 0.250, 0.466],
                  [0.001, 0.001, 0.001, 0.002, 0.002, 0.004]),
    'HD 10180': (['b', 'c', 'i', 'd', 'e', 'f', 'g', 'h'], [1, 2, 3, 4, 5, 6, 7, 8],
                 [0.0222, 0.06412, 0.0904, 0.12859, 0.2699, 0.4929, 1.427, 3.381],
                 [0.0011, 0.00101, 0.0045, 0.00202, 0.0043, 0.0078, 0.028, 0.121]),
    'Kepler-444': (['b', 'c', 'd', 'e', 'f'], [1, 2, 3, 4, 5],
                   [0.04178, 0.04881, 0.0600, 0.0696, 0.0811],
                   [0.00079, 0.00093, 0.0011, 0.0013, 0.0015]),
    'Kepler-102': (['b', 'c', 'd', 'e', 'f'], [1, 2, 3, 4, 5],
                   [0.05521, 0.06702, 0.08618, 0.1162, 0.1656],
                   [0.00049, 0.00059, 0.00076, 0.0010, 0.0015]),
    'K2-138': (['b', 'c', 'd', 'e', 'f', 'g'], [1, 2, 3, 4, 5, 6],
               [0.03385, 0.04461, 0.05893, 0.07820, 0.10447, 0.23109],
               [0.00026, 0.00034, 0.00045, 0.0006, 0.00079, 0.00175]),
    'TOI-178': (['b', 'c', 'd', 'e', 'f', 'g'], [1, 2, 3, 4, 5, 6],
                [0.02607, 0.0370, 0.0592, 0.0783, 0.1039, 0.1275],
                [0.00078, 0.0011, 0.0018, 0.0024, 0.0031, 0.0039]),
    'Kepler-80': (['f', 'd', 'e', 'b', 'c', 'g'], [1, 2, 3, 4, 5, 6],
                  [0.0175, 0.0372, 0.0491, 0.0658, 0.0792, 0.142],
                  [0.0002, 0.0005, 0.0007, 0.0009, 0.0011, 0.044]),
}

# Category 2: analog-calibrated (NOT fit to own data). r0_scaled, k held fixed at 1.3193.
ANALOG_K = 1.3193
BLIND_TARGETS = {
    'Ross 128':          {'r0': 0.01532, 'planets': {'b': (0.04964, 0.000004, 4)}},
    "Teegarden's Star":  {'r0': 0.00928, 'planets': {'b': (0.0259, 0.00085, 4), 'c': (0.0455, 0.0016, 6), 'd': (0.0791, 0.0026, 8)}},
    'LHS 1140':          {'r0': 0.01670, 'planets': {'c': (0.0270, 0.0005, 2), 'b': (0.0946, 0.0017, 6)}},
    'GJ 1002':           {'r0': 0.01060, 'planets': {'b': (0.0457, 0.0013, 5), 'c': (0.0738, 0.0021, 7)}},
}

def main():
    print("=" * 90)
    print("FITTED SYSTEMS: MODEL ERROR vs. PUBLISHED OBSERVATIONAL UNCERTAINTY")
    print("=" * 90)
    print(f"{'System':<15}{'Mean |ModelErr%|':<20}{'Mean ObsUncert%':<20}{'Ratio':<10}")
    print("-" * 65)
    for name, (names, n, r, sig) in FITTED_SYSTEMS.items():
        r_pred, err = fit_full(n, r)
        model_err_pct = np.abs(err)
        obs_uncert_pct = np.array(sig) / np.array(r) * 100
        ratio = model_err_pct.mean() / obs_uncert_pct.mean()
        print(f"{name:<15}{model_err_pct.mean():<20.2f}{obs_uncert_pct.mean():<20.2f}{ratio:<10.1f}x")

    print("\n" + "=" * 90)
    print("CATEGORY 2 BLIND PREDICTIONS: ANALOG ERROR vs. PUBLISHED OBSERVATIONAL UNCERTAINTY")
    print("=" * 90)
    print(f"{'System':<18}{'Planet':<8}{'Obs (AU)':<12}{'Analog Pred':<14}{'ModelErr%':<12}{'ObsUncert%':<12}{'Ratio':<8}")
    for name, t in BLIND_TARGETS.items():
        r0 = t['r0']
        for pname, (robs, sig, n) in t['planets'].items():
            rpred = r0 * (ANALOG_K ** n)
            err_pct = abs(rpred - robs) / robs * 100
            obs_pct = sig / robs * 100
            ratio = err_pct / obs_pct if obs_pct > 0 else float('inf')
            print(f"{name:<18}{pname:<8}{robs:<12.4f}{rpred:<14.4f}{err_pct:<12.2f}{obs_pct:<12.2f}{ratio:<8.1f}x")

    print("\nINTERPRETATION: Ratio <= 1 means model error is consistent with measurement")
    print("noise (no real disagreement demonstrable). Ratio >> 1 means the model residual")
    print("is a genuine physical disagreement beyond what measurement precision can explain.")

if __name__ == '__main__':
    main()
