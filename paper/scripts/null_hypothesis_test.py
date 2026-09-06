#!/usr/bin/env python3
"""
Null-Hypothesis Monte Carlo Baseline Test — Eigenmode Orbital Dynamics
Rick Drayson | Statistical Rigor Validation (Phase A1)

PURPOSE
-------
The eigenmode model fits r_n = r0 * k^n to each system using two free parameters
(r0, k) against only 4-12 data points. High R^2 values in this regime are not
automatically meaningful: almost ANY monotonically increasing sequence of a few
numbers will fit an exponential curve on a log axis with a high R^2. This script
tests whether the real systems' R^2 values are actually distinguishable from what
random monotonic sequences would produce by chance.

METHOD
------
For each real system:
  1. Take the same number of bodies (N) and the same [r_min, r_max] range.
  2. Generate 10,000 random monotonically-increasing sequences of N values within
     that range (uniform-random order statistics, NOT log-uniform, to avoid
     baking in the answer).
  3. Fit the same 2-parameter log-linear model to each random sequence.
  4. Build the null distribution of R^2 values.
  5. Report the percentile rank of the REAL system's R^2 within that null
     distribution, and the null distribution's mean/median/95th percentile.
  6. Also fit a zero-free-parameter baseline: uniform log-spacing
     ln(r_n) = ln(r_min) + (n-1)/(N-1) * ln(r_max/r_min), i.e. the trivial
     "evenly spaced in log space" hypothesis with NO fitted parameters at all.

INTERPRETATION
--------------
If a real system's R^2 sits within the bulk of the null distribution (not above
roughly the 90th-95th percentile), the eigenmode fit's R^2 carries little to no
evidentiary weight beyond "these numbers are monotonically increasing" — which
is true of any set of planetary or satellite orbits by definition.
"""

import numpy as np

np.random.seed(42)  # Reproducibility of the Monte Carlo draw

SYSTEMS = [
    {'name': 'Solar System',        'n_bodies': 10, 'r_obs': [0.3871, 0.7233, 1.0000, 1.5237, 2.7675, 5.2044, 9.5826, 19.2184, 30.1104, 39.4820], 'real_r2': 0.9934},
    {'name': 'Jovian Galilean',      'n_bodies': 4,  'r_obs': [421.8, 671.1, 1070.4, 1882.7], 'real_r2': 0.9976},
    {'name': 'Saturnian Moons',      'n_bodies': 8,  'r_obs': [185.54, 238.04, 294.67, 377.42, 527.07, 1221.87, 1481.1, 3560.8], 'real_r2': 0.9986},
    {'name': 'Uranian Moons',        'n_bodies': 5,  'r_obs': [129.9, 190.9, 266.0, 436.3, 583.5], 'real_r2': 0.9951},
    {'name': 'TRAPPIST-1',           'n_bodies': 7,  'r_obs': [0.01154, 0.01580, 0.02227, 0.02925, 0.03849, 0.04683, 0.06189], 'real_r2': 0.9943},
    {'name': 'Kepler-90',            'n_bodies': 8,  'r_obs': [0.074, 0.089, 0.1234, 0.32, 0.42, 0.48, 0.71, 1.01], 'real_r2': 0.9886},
    {'name': 'Kepler-11',            'n_bodies': 6,  'r_obs': [0.091, 0.107, 0.155, 0.195, 0.250, 0.466], 'real_r2': 0.9942},
    {'name': 'HD 10180',             'n_bodies': 8,  'r_obs': [0.02222, 0.0641, 0.1284, 0.2684, 0.4929, 1.415, 2.59, 3.4], 'real_r2': 0.9883},
    {'name': '55 Cancri A',          'n_bodies': 5,  'r_obs': [0.01544, 0.1134, 0.2373, 0.7708, 5.76], 'real_r2': 0.9873},
    {'name': 'Kepler-20',            'n_bodies': 6,  'r_obs': [0.04537, 0.0507, 0.0930, 0.1100, 0.3450, 0.4780], 'real_r2': 0.9681},
    {'name': 'TOI-700',              'n_bodies': 4,  'r_obs': [0.0677, 0.0929, 0.1340, 0.1633], 'real_r2': 0.9871},
]

N_TRIALS = 10000

def fit_r2(n_arr, r_arr):
    """Fit ln(r) = lambda*n + ln(r0), return R^2."""
    ln_r = np.log(r_arr)
    p = np.polyfit(n_arr, ln_r, 1)
    lam, ln_r0 = p[0], p[1]
    ss_res = np.sum((ln_r - (lam * n_arr + ln_r0)) ** 2)
    ss_tot = np.sum((ln_r - np.mean(ln_r)) ** 2)
    if ss_tot == 0:
        return 1.0
    return 1.0 - (ss_res / ss_tot)

def zero_param_baseline_r2(n_arr, r_arr):
    """Zero-free-parameter baseline: uniform log-spacing between observed min/max."""
    r_min, r_max = np.min(r_arr), np.max(r_arr)
    n_min, n_max = np.min(n_arr), np.max(n_arr)
    ln_r_obs = np.log(r_arr)
    ln_r_pred = np.log(r_min) + (n_arr - n_min) / (n_max - n_min) * np.log(r_max / r_min)
    ss_res = np.sum((ln_r_obs - ln_r_pred) ** 2)
    ss_tot = np.sum((ln_r_obs - np.mean(ln_r_obs)) ** 2)
    if ss_tot == 0:
        return 1.0
    return 1.0 - (ss_res / ss_tot)

def run_monte_carlo(n_bodies, r_min, r_max, n_trials=N_TRIALS):
    """Generate random monotonic sequences in [r_min, r_max] and fit the 2-param model."""
    n_arr = np.arange(1, n_bodies + 1, dtype=float)
    r2_null = np.zeros(n_trials)
    for i in range(n_trials):
        # Uniform random draw in [r_min, r_max], sorted ascending (order statistics)
        raw = np.random.uniform(r_min, r_max, size=n_bodies)
        raw.sort()
        r2_null[i] = fit_r2(n_arr, raw)
    return r2_null

def main():
    print("=" * 92)
    print("NULL-HYPOTHESIS MONTE CARLO BASELINE TEST (N = {} trials per system)".format(N_TRIALS))
    print("=" * 92)
    print(f"{'System':<20}{'N':<4}{'Real R2':<10}{'Null Mean':<11}{'Null P50':<10}{'Null P95':<10}{'Percentile':<12}{'0-Param R2':<12}")
    print("-" * 92)

    results = []
    for s in SYSTEMS:
        r_arr = np.array(s['r_obs'])
        n_arr = np.arange(1, s['n_bodies'] + 1, dtype=float)
        r_min, r_max = np.min(r_arr), np.max(r_arr)

        null_r2 = run_monte_carlo(s['n_bodies'], r_min, r_max)
        percentile_rank = (null_r2 < s['real_r2']).mean() * 100.0
        zero_param_r2 = zero_param_baseline_r2(n_arr, r_arr)

        results.append({
            'name': s['name'],
            'real_r2': s['real_r2'],
            'null_mean': null_r2.mean(),
            'null_p50': np.percentile(null_r2, 50),
            'null_p95': np.percentile(null_r2, 95),
            'percentile_rank': percentile_rank,
            'zero_param_r2': zero_param_r2
        })

        print(f"{s['name']:<20}{s['n_bodies']:<4}{s['real_r2']:<10.4f}{null_r2.mean():<11.4f}"
              f"{np.percentile(null_r2, 50):<10.4f}{np.percentile(null_r2, 95):<10.4f}"
              f"{percentile_rank:<12.1f}{zero_param_r2:<12.4f}")

    print("-" * 92)
    print("\nINTERPRETATION GUIDE:")
    print("  - 'Percentile' = where the REAL system's R2 falls within 10,000 random monotonic")
    print("    sequences of the same size and range. >95 = clearly distinguishable from chance.")
    print("  - '0-Param R2' = R2 of the trivial 'evenly log-spaced, no fitted parameters' model.")
    print("    If this is close to the real eigenmode R2, the 2-parameter fit adds little value.")
    print("=" * 92)

    return results

if __name__ == '__main__':
    main()
