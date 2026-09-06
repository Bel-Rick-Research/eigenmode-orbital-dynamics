#!/usr/bin/env python3
"""
Index-Assignment Sensitivity Test — Eigenmode Orbital Dynamics
Rick Drayson | Statistical Rigor Validation (Phase A3)

PURPOSE
-------
Four systems in the dataset (Kepler-90, Kepler-11, Kepler-20, 55 Cancri A) skip
integer values of n (e.g. Kepler-90 uses n = 1,2,3,5,6,7,8,9, omitting n=4).
Choosing WHICH integers to skip, after seeing the data, is a hidden free
parameter that can artificially inflate R^2. This script tests each system's
ORIGINAL index assignment against alternative contiguous assignments (no gaps)
and reports how much R^2 changes, to make this choice's impact visible and
explicit rather than silently baked into the headline numbers.
"""

import numpy as np

def fit_r2(n_arr, r_arr):
    n_arr = np.asarray(n_arr, dtype=float)
    ln_r = np.log(r_arr)
    p = np.polyfit(n_arr, ln_r, 1)
    lam, ln_r0 = p[0], p[1]
    ss_res = np.sum((ln_r - (lam * n_arr + ln_r0)) ** 2)
    ss_tot = np.sum((ln_r - np.mean(ln_r)) ** 2)
    r2 = 1.0 - (ss_res / ss_tot)
    return r2, lam, np.exp(ln_r0), np.exp(lam)

GAPPED_SYSTEMS = [
    {
        'name': 'Kepler-90',
        'bodies': ['b', 'c', 'i', 'd', 'e', 'f', 'g', 'h'],
        'r_obs': [0.074, 0.089, 0.1234, 0.32, 0.42, 0.48, 0.71, 1.01],
        'n_original': [1, 2, 3, 5, 6, 7, 8, 9],  # skips n=4
    },
    {
        'name': 'Kepler-11',
        'bodies': ['b', 'c', 'd', 'e', 'f', 'g'],
        'r_obs': [0.091, 0.107, 0.155, 0.195, 0.250, 0.466],
        'n_original': [1, 2, 3, 4, 5, 7],  # skips n=6
    },
    {
        'name': 'Kepler-20',
        'bodies': ['b', 'e', 'c', 'f', 'd', 'g'],
        'r_obs': [0.04537, 0.0507, 0.0930, 0.1100, 0.3450, 0.4780],
        'n_original': [1, 2, 3, 4, 6, 8],  # skips n=5, 7
    },
    {
        'name': '55 Cancri A',
        'bodies': ['e', 'b', 'c', 'f', 'd'],
        'r_obs': [0.01544, 0.1134, 0.2373, 0.7708, 5.76],
        'n_original': [1, 3, 4, 6, 9],  # skips n=2, 5, 7, 8
    },
]

def main():
    print("=" * 100)
    print("INDEX-ASSIGNMENT SENSITIVITY TEST")
    print("=" * 100)

    for s in GAPPED_SYSTEMS:
        r_arr = np.array(s['r_obs'])
        n_orig = s['n_original']
        n_contig = list(range(1, len(r_arr) + 1))  # naive: no gaps at all

        r2_orig, lam_orig, r0_orig, k_orig = fit_r2(n_orig, r_arr)
        r2_contig, lam_contig, r0_contig, k_contig = fit_r2(n_contig, r_arr)

        print(f"\n--- {s['name']} ---")
        print(f"  Bodies: {s['bodies']}")
        print(f"  Original (gapped) index assignment: n = {n_orig}")
        print(f"    -> R2 = {r2_orig:.4f}, k = {k_orig:.4f}, r0 = {r0_orig:.5f}")
        print(f"  Naive contiguous assignment (no gaps): n = {n_contig}")
        print(f"    -> R2 = {r2_contig:.4f}, k = {k_contig:.4f}, r0 = {r0_contig:.5f}")
        delta_r2 = r2_orig - r2_contig
        print(f"  Delta R2 (gapped - contiguous) = {delta_r2:+.4f}")
        if delta_r2 > 0.02:
            print(f"  FLAG: gap assignment improves fit by >0.02 R2 -- this choice materially")
            print(f"        affects the headline statistic and should be justified independently")
            print(f"        (e.g. by an a priori dynamical stability argument for WHY those specific")
            print(f"        slots are predicted to be empty), not selected post-hoc for best fit.")
        else:
            print(f"  Gap choice has minor impact on R2 (<0.02) -- low sensitivity concern.")

    print("\n" + "=" * 100)
    print("CONCLUSION: Where Delta R2 is large, the reported R2 for that system should be read")
    print("as conditional on the index-gap choice, and the gap slots reported in Section 7 as")
    print("'predicted empty shells' are, for those systems, partially a restatement of the fitting")
    print("choice rather than an independent discovery. This is disclosed explicitly per system.")
    print("=" * 100)

if __name__ == '__main__':
    main()
