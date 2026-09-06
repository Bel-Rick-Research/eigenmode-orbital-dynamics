#!/usr/bin/env python3
"""
Alternative Model Comparison: Titius-Bode & Hill-Radius Dynamical Packing
Rick Drayson | Statistical Rigor Validation (Phase F2)

PURPOSE
-------
The paper's introduction invokes the Titius-Bode law only conceptually, without
ever fitting it to the same benchmark systems and comparing quantitatively. This
script closes that gap directly, using AIC (equal parameter count, k=2 for both
models) on a common, untransformed observable (r_n in native units) so the
comparison is fair:

  Model A (this paper):  r_n = r0 * k^n            (exponential / log-linear)
  Model B (Titius-Bode):  r_n = A + B * 2^n          (classic empirical form)

AIC = 2*k_params + n*ln(RSS/n); lower AIC = better fit for the same data.

It also implements a simplified test against the mainstream Hill-radius orbital
stability explanation (Chambers 1996; Gladman 1993; Hayes & Tremaine 1998): the
observation that adjacent-planet spacing in units of mutual Hill radii clusters
around a roughly constant value (~10-20) is a NON-quantization explanation for
regular-looking spacing, requiring only a stability criterion, no wave mechanism.
This is computed for systems where planet mass estimates are available.
"""

import numpy as np

# name: (n, r_obs [native units])
SYSTEMS = {
    'Solar System':     ([1,2,3,4,5,6,7,8,9,10], [0.3871,0.7233,1.0000,1.5237,2.7675,5.2044,9.5826,19.2184,30.1104,39.4820]),
    'Jovian Galilean':  ([1,2,3,4], [421.8,671.1,1070.4,1882.7]),
    'Saturnian Moons':  ([1,2,3,4,5,8,9,12], [185.54,238.04,294.67,377.42,527.07,1221.87,1481.1,3560.8]),
    'Uranian Moons':    ([1,2,3,4,5], [129.9,190.9,266.0,436.3,583.5]),
    'TRAPPIST-1':       ([1,2,3,4,5,6,7], [0.01154,0.01580,0.02227,0.02925,0.03849,0.04683,0.06189]),
    'Kepler-90':        ([1,2,3,5,6,7,8,9], [0.074,0.089,0.1234,0.32,0.42,0.48,0.71,1.01]),
    'Kepler-11':        ([1,2,3,4,5,7], [0.091,0.107,0.155,0.195,0.250,0.466]),
    'HD 10180':         ([1,2,3,4,5,6,7,8], [0.02222,0.0641,0.1284,0.2684,0.4929,1.415,2.59,3.4]),
    '55 Cancri A':      ([1,3,4,6,9], [0.01544,0.1134,0.2373,0.7708,5.76]),
    'Kepler-20':        ([1,2,3,4,6,8], [0.04537,0.0507,0.0930,0.1100,0.3450,0.4780]),
    'TOI-700':          ([1,2,3,4], [0.0677,0.0929,0.1340,0.1633]),
}

def fit_eigenmode(n_arr, r_arr):
    n_arr = np.array(n_arr, dtype=float)
    ln_r = np.log(r_arr)
    p = np.polyfit(n_arr, ln_r, 1)
    lam, ln_r0 = p[0], p[1]
    r0, k = np.exp(ln_r0), np.exp(lam)
    r_pred = r0 * (k ** n_arr)
    rss = np.sum((r_pred - r_arr) ** 2)
    return rss, r_pred

def fit_titius_bode(n_arr, r_arr):
    """r_n = A + B * 2^n, linear regression on regressor x = 2^n."""
    n_arr = np.array(n_arr, dtype=float)
    r_arr = np.array(r_arr, dtype=float)
    x = 2.0 ** n_arr
    X = np.vstack([np.ones_like(x), x]).T
    coeffs, _, _, _ = np.linalg.lstsq(X, r_arr, rcond=None)
    A, B = coeffs
    r_pred = A + B * x
    rss = np.sum((r_pred - r_arr) ** 2)
    return rss, r_pred, A, B

def aic(rss, n_points, n_params=2):
    return 2 * n_params + n_points * np.log(rss / n_points)

def main():
    print("=" * 100)
    print("MODEL COMPARISON: EIGENMODE (r0*k^n) vs. TITIUS-BODE (A + B*2^n)")
    print("Both models have 2 free parameters; AIC computed on native-unit residuals.")
    print("=" * 100)
    print(f"{'System':<18}{'N':<4}{'AIC (Eigenmode)':<18}{'AIC (Titius-Bode)':<20}{'Delta AIC':<12}{'Preferred'}")
    print("-" * 90)

    eigen_wins, tb_wins = 0, 0
    for name, (n, r) in SYSTEMS.items():
        rss_e, _ = fit_eigenmode(n, r)
        rss_tb, _, A, B = fit_titius_bode(n, r)
        n_pts = len(n)
        aic_e = aic(rss_e, n_pts)
        aic_tb = aic(rss_tb, n_pts)
        delta = aic_tb - aic_e  # positive means eigenmode preferred (lower AIC)
        preferred = "Eigenmode" if delta > 2 else ("Titius-Bode" if delta < -2 else "Indistinguishable")
        if preferred == "Eigenmode":
            eigen_wins += 1
        elif preferred == "Titius-Bode":
            tb_wins += 1
        print(f"{name:<18}{n_pts:<4}{aic_e:<18.2f}{aic_tb:<20.2f}{delta:<12.2f}{preferred}")

    print("-" * 90)
    print(f"SUMMARY: Eigenmode preferred (|ΔAIC|>2) in {eigen_wins}/{len(SYSTEMS)} systems; "
          f"Titius-Bode preferred in {tb_wins}/{len(SYSTEMS)}; remainder indistinguishable.")

    print("\n" + "=" * 100)
    print("SUPPLEMENTARY: HILL-RADIUS DYNAMICAL PACKING CHECK (mainstream alternative, no wave mechanism)")
    print("Spacing in mutual Hill radii: Delta_ij = 2*(a_j-a_i)/(a_i+a_j) * (3*M_star/(m_i+m_j))^(1/3)")
    print("Stable multi-planet systems typically cluster around Delta ~ 10-20 (Chambers 1996; Gladman 1993).")
    print("=" * 100)

    # (a in AU, mass in Earth masses), M_star in Solar masses
    HILL_SYSTEMS = {
        'Kepler-11 (M_star=1.04 Msun)': {
            'M_star': 1.04,
            'planets': [('b', 0.091, 2.78), ('c', 0.107, 5.0), ('d', 0.155, 8.13),
                        ('e', 0.195, 9.48), ('f', 0.250, 2.43), ('g', 0.466, 15.0)]
        },
        'Kepler-90 (M_star=1.2 Msun)': {
            'M_star': 1.2,
            'planets': [('b', 0.074, 4.3), ('c', 0.089, 6.5), ('i', 0.107, 4.5),
                        ('d', 0.32, 7.2), ('e', 0.42, 6.6), ('f', 0.48, 6.9),
                        ('g', 0.71, 15.0), ('h', 1.01, 203.0)]
        },
        'Kepler-444 (M_star=0.754 Msun)': {
            'M_star': 0.754,
            'planets': [('b', 0.04178, 0.079), ('c', 0.04881, 0.16), ('d', 0.0600, 0.036),
                        ('e', 0.0696, 0.034), ('f', 0.0811, 0.22)]
        },
    }
    MSUN_PER_MEARTH = 1.0 / 333000.0

    for name, sysdata in HILL_SYSTEMS.items():
        M_star = sysdata['M_star']
        planets = sysdata['planets']
        print(f"\n{name}:")
        deltas = []
        for i in range(len(planets) - 1):
            name_i, a_i, m_i = planets[i]
            name_j, a_j, m_j = planets[i + 1]
            m_i_msun = m_i * MSUN_PER_MEARTH
            m_j_msun = m_j * MSUN_PER_MEARTH
            mutual_hill = ((m_i_msun + m_j_msun) / (3 * M_star)) ** (1/3)
            delta = 2 * (a_j - a_i) / (a_i + a_j) / mutual_hill
            deltas.append(delta)
            print(f"  {name_i}->{name_j}: Delta = {delta:.1f} mutual Hill radii")
        deltas = np.array(deltas)
        print(f"  Mean Delta = {deltas.mean():.1f}, Std Dev = {deltas.std():.1f} "
              f"(stability threshold ~8-10; observed range {'consistent' if deltas.min() > 8 else 'BELOW threshold for some pairs'})")

if __name__ == '__main__':
    main()
