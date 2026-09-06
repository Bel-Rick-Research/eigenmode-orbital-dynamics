#!/usr/bin/env python3
"""
Eigenmode Orbital Dynamics - Mathematical Validation & Exoplanet Predictor
Rick Drayson | Research Paper Reproducibility Code

Original Inspiration & Empirical Discovery:
  Dr. Michael Clarage — observational discovery that planetary and satellite
  orbitals follow a strict logarithmic quantization pattern across stellar systems.

This script computes:
1. Log-linear regression parameters (r0, lambda, k = e^lambda, R^2) across Solar System,
   satellite systems (Jupiter, Saturn, Uranus), and multi-planet exoplanetary systems.
2. Observed vs. predicted orbital semi-major axes with percentage residuals.
3. Quantized eigenmode predictions for unobserved / empty harmonic shells across exoplanet systems.
"""

import numpy as np

SYSTEMS = [
    {
        'id': 'solar_system',
        'name': 'Solar System',
        'host': 'Sol (Sun)',
        'type': 'G2V Main Sequence Star',
        'bodies': ['Mercury', 'Venus', 'Earth', 'Mars', 'Ceres/Belt', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto'],
        'n': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'r_obs': [0.3871, 0.7233, 1.0000, 1.5237, 2.7675, 5.2044, 9.5826, 19.2184, 30.1104, 39.4820],
        'unit': 'AU',
        'empty_nodes': [],
        'predict_outer': [11, 12, 13]
    },
    {
        'id': 'jupiter_galilean',
        'name': 'Jovian System (Galilean)',
        'host': 'Jupiter',
        'type': 'Gas Giant Core Resonator',
        'bodies': ['Io', 'Europa', 'Ganymede', 'Callisto'],
        'n': [1, 2, 3, 4],
        'r_obs': [421.8, 671.1, 1070.4, 1882.7],
        'unit': '10^3 km',
        'empty_nodes': [],
        'predict_outer': [5, 6]
    },
    {
        'id': 'saturnian_moons',
        'name': 'Saturnian Satellite System',
        'host': 'Saturn',
        'type': 'Gas Giant Core Resonator',
        'bodies': ['Mimas', 'Enceladus', 'Tethys', 'Dione', 'Rhea', 'Titan', 'Hyperion', 'Iapetus'],
        'n': [1, 2, 3, 4, 5, 8, 9, 12],
        'r_obs': [185.54, 238.04, 294.67, 377.42, 527.07, 1221.87, 1481.1, 3560.8],
        'unit': '10^3 km',
        'empty_nodes': [6, 7, 10, 11],
        'predict_outer': [13, 14]
    },
    {
        'id': 'uranian_moons',
        'name': 'Uranian Major Moons',
        'host': 'Uranus',
        'type': 'Ice Giant Core Resonator',
        'bodies': ['Miranda', 'Ariel', 'Umbriel', 'Titania', 'Oberon'],
        'n': [1, 2, 3, 4, 5],
        'r_obs': [129.9, 190.9, 266.0, 436.3, 583.5],
        'unit': '10^3 km',
        'empty_nodes': [],
        'predict_outer': [6, 7]
    },
    {
        'id': 'trappist_1',
        'name': 'TRAPPIST-1 System',
        'host': 'TRAPPIST-1',
        'type': 'M8V Ultra-Cool Dwarf',
        'bodies': ['TRAPPIST-1b', 'TRAPPIST-1c', 'TRAPPIST-1d', 'TRAPPIST-1e', 'TRAPPIST-1f', 'TRAPPIST-1g', 'TRAPPIST-1h'],
        'n': [1, 2, 3, 4, 5, 6, 7],
        'r_obs': [0.01154, 0.01580, 0.02227, 0.02925, 0.03849, 0.04683, 0.06189],
        'unit': 'AU',
        'empty_nodes': [],
        'predict_outer': [8, 9, 10]
    },
    {
        'id': 'kepler_90',
        'name': 'Kepler-90 System',
        'host': 'Kepler-90',
        'type': 'G0V Sol-like Star',
        'bodies': ['Kepler-90b', 'Kepler-90c', 'Kepler-90i', 'Kepler-90d', 'Kepler-90e', 'Kepler-90f', 'Kepler-90g', 'Kepler-90h'],
        'n': [1, 2, 3, 5, 6, 7, 8, 9],
        'r_obs': [0.074, 0.089, 0.1234, 0.32, 0.42, 0.48, 0.71, 1.01],
        'unit': 'AU',
        'empty_nodes': [4],
        'predict_outer': [10, 11]
    },
    {
        'id': 'kepler_11',
        'name': 'Kepler-11 System',
        'host': 'Kepler-11',
        'type': 'G6V Star',
        'bodies': ['Kepler-11b', 'Kepler-11c', 'Kepler-11d', 'Kepler-11e', 'Kepler-11f', 'Kepler-11g'],
        'n': [1, 2, 3, 4, 5, 7],
        'r_obs': [0.091, 0.107, 0.155, 0.195, 0.250, 0.466],
        'unit': 'AU',
        'empty_nodes': [6],
        'predict_outer': [8, 9]
    },
    {
        'id': 'hd_10180',
        'name': 'HD 10180 System',
        'host': 'HD 10180',
        'type': 'G1V Star',
        'bodies': ['HD 10180b', 'HD 10180c', 'HD 10180i', 'HD 10180d', 'HD 10180e', 'HD 10180f', 'HD 10180g', 'HD 10180h'],
        'n': [1, 2, 3, 4, 5, 6, 7, 8],
        'r_obs': [0.02222, 0.0641, 0.1284, 0.2684, 0.4929, 1.415, 2.59, 3.4],
        'unit': 'AU',
        'empty_nodes': [],
        'predict_outer': [9, 10]
    },
    {
        'id': '55_cancri',
        'name': '55 Cancri A System',
        'host': '55 Cancri A',
        'type': 'K0IV Star',
        'bodies': ['55 Cnc e', '55 Cnc b', '55 Cnc c', '55 Cnc f', '55 Cnc d'],
        'n': [1, 3, 4, 6, 9],
        'r_obs': [0.01544, 0.1134, 0.2373, 0.7708, 5.76],
        'unit': 'AU',
        'empty_nodes': [2, 5, 7, 8],
        'predict_outer': [10, 11]
    },
    {
        'id': 'kepler_20',
        'name': 'Kepler-20 System',
        'host': 'Kepler-20',
        'type': 'G8V Star',
        'bodies': ['Kepler-20b', 'Kepler-20e', 'Kepler-20c', 'Kepler-20f', 'Kepler-20d', 'Kepler-20g'],
        'n': [1, 2, 3, 4, 6, 8],
        'r_obs': [0.04537, 0.0507, 0.0930, 0.1100, 0.3450, 0.4780],
        'unit': 'AU',
        'empty_nodes': [5, 7],
        'predict_outer': [9, 10]
    },
    {
        'id': 'toi_700',
        'name': 'TOI-700 System',
        'host': 'TOI-700',
        'type': 'M2V Dwarf',
        'bodies': ['TOI-700 b', 'TOI-700 c', 'TOI-700 e', 'TOI-700 d'],
        'n': [1, 2, 3, 4],
        'r_obs': [0.0677, 0.0929, 0.1340, 0.1633],
        'unit': 'AU',
        'empty_nodes': [],
        'predict_outer': [5, 6, 7]
    }
]

def solve_system(s):
    r_obs = np.array(s['r_obs'], dtype=float)
    n = np.array(s['n'], dtype=float)
    ln_r = np.log(r_obs)
    
    # cov=True gives the parameter covariance matrix -> standard errors on lambda, ln(r0)
    p, cov = np.polyfit(n, ln_r, 1, cov=True)
    lam, ln_r0 = p[0], p[1]
    lam_se = np.sqrt(cov[0, 0])
    ln_r0_se = np.sqrt(cov[1, 1])

    r0 = np.exp(ln_r0)
    k = np.exp(lam)
    # Propagate SE through exp() via d(e^x)/dx = e^x
    r0_se = r0 * ln_r0_se
    k_se = k * lam_se
    
    r_pred = r0 * (k ** n)
    err = (r_pred - r_obs) / r_obs * 100.0
    abs_err_pct = np.abs(err)
    mae = np.mean(abs_err_pct)
    max_err = np.max(abs_err_pct)
    
    ss_res = np.sum((ln_r - (lam * n + ln_r0)) ** 2)
    ss_tot = np.sum((ln_r - np.mean(ln_r)) ** 2)
    r2 = 1.0 - (ss_res / ss_tot)
    
    return {
        'r0': r0,
        'r0_se': r0_se,
        'lambda': lam,
        'lambda_se': lam_se,
        'k': k,
        'k_se': k_se,
        'r2': r2,
        'mae': mae,
        'max_err': max_err,
        'r_pred': r_pred,
        'err': err
    }

def print_summary():
    print("=" * 80)
    print("EIGENMODE ORBITAL DYNAMICS - REPRODUCIBILITY SUMMARY")
    print("=" * 80)
    
    for s in SYSTEMS:
        res = solve_system(s)
        print(f"\nSystem: {s['name']} ({s['type']})")
        print(f"Formula: r_n = {res['r0']:.5f} * ({res['k']:.4f})^n {s['unit']}")
        print(f"Parameters: r0 = {res['r0']:.5f} +/- {res['r0_se']:.5f} {s['unit']} | "
              f"lambda = {res['lambda']:.4f} +/- {res['lambda_se']:.4f} | "
              f"k = {res['k']:.4f} +/- {res['k_se']:.4f} | R^2 = {res['r2']:.4f}")
        print(f"Honest error metrics: Mean Absolute % Error = {res['mae']:.2f}% | Max % Error = {res['max_err']:.2f}%")
        print("-" * 75)
        print(f"{'Index (n)':<10} | {'Body':<15} | {'Observed (' + s['unit'] + ')':<15} | {'Model (' + s['unit'] + ')':<15} | {'Error (%)':<10}")
        print("-" * 75)
        for b, ni, obs, pred, er in zip(s['bodies'], s['n'], s['r_obs'], res['r_pred'], res['err']):
            print(f"{ni:<10d} | {b:<15} | {obs:<15.4f} | {pred:<15.4f} | {er:+9.2f}%")
        
        # Predict empty internal nodes
        if s['empty_nodes']:
            print("-" * 75)
            print("Predicted Unoccupied / Intermediate Resonant Shells (Belt/Debris Candidates):")
            for empty_n in s['empty_nodes']:
                pred_empty = res['r0'] * (res['k'] ** empty_n)
                print(f"  * Node n = {empty_n:2d}: r_{empty_n} = {pred_empty:.4f} {s['unit']}")
                
        # Predict outer nodes
        if s['predict_outer']:
            print("Predicted Undiscovered Outer Harmonic Orbits:")
            for outer_n in s['predict_outer']:
                pred_outer = res['r0'] * (res['k'] ** outer_n)
                print(f"  * Node n = {outer_n:2d}: r_{outer_n} = {pred_outer:.4f} {s['unit']}")

if __name__ == '__main__':
    print_summary()
