#!/usr/bin/env python3
"""
Blind Prediction Program Reproducibility Script — Eigenmode Orbital Dynamics
Rick Drayson | Phase D1/D2 Reproducibility

Reproduces both new prediction categories added in Revision 2:
  - Category 1: fixed-method application to previously-unexamined exosystems
  - Category 2: spectral-type analog-calibrated blind predictions for few-planet systems

Run: python3 scripts/blind_prediction_program.py
"""

import numpy as np

# ----------------------------------------------------------------------
# CATEGORY 1: Explored-but-uncompared systems (fixed candidate list, no gaps)
# ----------------------------------------------------------------------
CATEGORY_1_SYSTEMS = {
    'Kepler-80 (M0V)':   (['f', 'd', 'e', 'b', 'c', 'g'], [1, 2, 3, 4, 5, 6],
                          [0.0175, 0.0372, 0.0491, 0.0658, 0.0792, 0.142]),
    'Kepler-444 (K0V)':  (['b', 'c', 'd', 'e', 'f'], [1, 2, 3, 4, 5],
                          [0.04178, 0.04881, 0.0600, 0.0696, 0.0811]),
    'K2-138 (K1V)':      (['b', 'c', 'd', 'e', 'f', 'g'], [1, 2, 3, 4, 5, 6],
                          [0.03385, 0.04461, 0.05893, 0.07820, 0.10447, 0.23109]),
    'Kepler-102 (K3V)':  (['b', 'c', 'd', 'e', 'f'], [1, 2, 3, 4, 5],
                          [0.05521, 0.06702, 0.08618, 0.1162, 0.1656]),
    'TOI-178 (K7V)':     (['b', 'c', 'd', 'e', 'f', 'g'], [1, 2, 3, 4, 5, 6],
                          [0.02607, 0.0370, 0.0592, 0.0783, 0.1039, 0.1275]),
}

# ----------------------------------------------------------------------
# CATEGORY 2: Few-planet ("unsurveyed") systems + TRAPPIST-1 analog reference
# ----------------------------------------------------------------------
ANALOG_R0 = 0.00922    # AU, TRAPPIST-1 fitted r0
ANALOG_K = 1.3193      # TRAPPIST-1 fitted k
ANALOG_R_STAR = 0.1192 # Solar radii, TRAPPIST-1

CATEGORY_2_TARGETS = {
    'Ross 128 (M4V)': {
        'R_star': 0.198,
        'planets': {'b': 0.04964}
    },
    "Teegarden's Star (M7.0V)": {
        'R_star': 0.120,
        'planets': {'b': 0.0259, 'c': 0.0455, 'd': 0.0791}
    },
    'LHS 1140 (M4.5V)': {
        'R_star': 0.2159,
        'planets': {'c': 0.0270, 'b': 0.0946}
    },
    'GJ 1002 (M5.5V)': {
        'R_star': 0.137,
        'planets': {'b': 0.0457, 'c': 0.0738}
    }
}

def fit_full(n_arr, r_arr):
    n_arr = np.array(n_arr, dtype=float)
    ln_r = np.log(r_arr)
    p = np.polyfit(n_arr, ln_r, 1)
    lam, ln_r0 = p[0], p[1]
    r0 = np.exp(ln_r0)
    k = np.exp(lam)
    r_pred = r0 * (k ** n_arr)
    err = (r_pred - r_arr) / r_arr * 100.0
    ss_res = np.sum((ln_r - (lam * n_arr + ln_r0)) ** 2)
    ss_tot = np.sum((ln_r - np.mean(ln_r)) ** 2)
    r2 = 1.0 - (ss_res / ss_tot)
    return r0, k, r2, r_pred, err

def run_category_1():
    print("=" * 90)
    print("CATEGORY 1: FIXED-METHOD APPLICATION TO PREVIOUSLY-UNEXAMINED SYSTEMS")
    print("=" * 90)
    for name, (names, n, r) in CATEGORY_1_SYSTEMS.items():
        r0, k, r2, r_pred, err = fit_full(n, r)
        print(f"\n{name}: r0={r0:.5f} AU, k={k:.4f}, R2={r2:.4f}")
        for nm, ni, ro, rp, e in zip(names, n, r, r_pred, err):
            print(f"  n={ni} {nm:4s} obs={ro:.5f} pred={rp:.5f} err={e:+.2f}%")
        for extra_n in [n[-1] + 1, n[-1] + 2]:
            rn = r0 * (k ** extra_n)
            print(f"  PREDICTED outer shell n={extra_n}: r_n={rn:.5f} AU")

def run_category_2():
    print("\n" + "=" * 90)
    print("CATEGORY 2: ANALOG-CALIBRATED BLIND PREDICTIONS (TRAPPIST-1 as M-dwarf reference)")
    print("=" * 90)
    for name, t in CATEGORY_2_TARGETS.items():
        r0_scaled = ANALOG_R0 * (t['R_star'] / ANALOG_R_STAR)
        print(f"\n{name}: r0_scaled={r0_scaled:.5f} AU, k={ANALOG_K} (held fixed from analog)")
        shells = {n: r0_scaled * (ANALOG_K ** n) for n in range(1, 11)}
        matched_n = set()
        for pname, robs in t['planets'].items():
            best_n, best_err = None, 1e9
            for n, rn in shells.items():
                e = abs(rn - robs) / robs * 100
                if e < best_err:
                    best_err, best_n = e, n
            matched_n.add(best_n)
            print(f"  Known planet {pname}: obs={robs:.4f} AU -> n={best_n} "
                  f"(pred {shells[best_n]:.4f} AU, err {best_err:+.1f}%)")
        print("  BLIND predicted shells:")
        for n, rn in shells.items():
            if n not in matched_n:
                print(f"    n={n}: r_n = {rn:.4f} AU")

if __name__ == '__main__':
    run_category_1()
    run_category_2()
