#!/usr/bin/env python3
"""
K-Ratio "Nice Number" Significance Test — Eigenmode Orbital Dynamics
Rick Drayson | Statistical Rigor Validation (Phase F1)

PURPOSE
-------
Section 4.2 of the paper labels each system's fitted geometric ratio k with the
nearest "nice" harmonic/musical/irrational ratio (4/3, sqrt(2), 3/2, sqrt(3), phi,
2.0, etc.). This is exactly the same kind of post-hoc pattern-matching already
flagged for index-gap assignment (Section 5.5) unless it can be shown that:
  (a) the claimed ratio is a statistically significant match (within ~2 sigma of
      the fitted k, given its own parameter uncertainty), AND
  (b) it is the ONLY candidate in a reasonable "nice ratio" pool that matches --
      if several nearby candidates all match equally well, the specific label
      chosen carries no more information than picking any of the others
      (a look-elsewhere-effect / multiple-comparisons problem).

This script tests both conditions for every system in the paper.
"""

import numpy as np

# System: (k_fit, k_se, claimed_ratio_label, claimed_ratio_value)
SYSTEMS = {
    'Solar System':        (1.7114, 0.0265, 'sqrt(3)', np.sqrt(3)),
    'Jovian Galilean':      (1.6413, 0.0283, 'phi (golden ratio)', (1 + np.sqrt(5)) / 2),
    'Saturnian Moons':      (1.3104, 0.0054, '4/3', 4/3),
    'Uranian Moons':        (1.4668, 0.0227, '3/2', 1.5),
    'TRAPPIST-1':           (1.3193, 0.0124, '4/3', 4/3),
    'Kepler-90':            (1.3999, 0.0206, 'sqrt(2)', np.sqrt(2)),
    'Kepler-11':            (1.3168, 0.0139, '4/3', 4/3),
    'HD 10180':             (2.0799, 0.0677, '2.0', 2.0),
    '55 Cancri A':          (2.0498, 0.0962, '2.0', 2.0),
    'Kepler-20':            (1.4459, 0.0484, '3/2', 1.5),
    'TOI-700':              (1.3509, 0.0328, '4/3', 4/3),
}

# Candidate pool of "nice" ratios a reader could plausibly propose (musical intervals,
# simple rationals, geometric/algebraic irrationals) spanning the observed k range.
CANDIDATE_POOL = {
    '6/5':        6/5,
    '5/4':        5/4,
    '4/3':        4/3,
    '7/5':        7/5,
    'sqrt(2)':    np.sqrt(2),
    '3/2':        3/2,
    '8/5':        8/5,
    'phi':        (1 + np.sqrt(5)) / 2,
    '5/3':        5/3,
    '7/4':        7/4,
    'sqrt(3)':    np.sqrt(3),
    '9/5':        9/5,
    '2.0':        2.0,
    '9/4':        9/4,
    'sqrt(5)':    np.sqrt(5),
    '5/2':        5/2,
}

def main():
    print("=" * 100)
    print("K-RATIO 'NICE NUMBER' SIGNIFICANCE TEST")
    print("=" * 100)
    print(f"{'System':<18}{'k_fit':<10}{'Claimed':<20}{'z(claimed)':<12}{'Sig?':<8}{'# Candidates <2sigma':<22}{'Unique?'}")
    print("-" * 100)

    flagged_systems = []
    for name, (k_fit, k_se, label, value) in SYSTEMS.items():
        z_claimed = abs(k_fit - value) / k_se
        sig_claimed = "YES" if z_claimed < 2.0 else "NO"

        matching_candidates = []
        for cand_label, cand_value in CANDIDATE_POOL.items():
            z = abs(k_fit - cand_value) / k_se
            if z < 2.0:
                matching_candidates.append((cand_label, cand_value, z))

        n_matches = len(matching_candidates)
        unique = "YES" if n_matches == 1 else ("NO" if n_matches > 1 else "N/A (none match)")

        print(f"{name:<18}{k_fit:<10.4f}{label + f' ({value:.4f})':<20}{z_claimed:<12.2f}{sig_claimed:<8}{n_matches:<22}{unique}")

        if n_matches > 1 or sig_claimed == "NO":
            flagged_systems.append((name, label, z_claimed, [c[0] for c in matching_candidates]))

    print("\n" + "=" * 100)
    print("DETAIL ON FLAGGED SYSTEMS (claimed ratio not significant, or multiple candidates match)")
    print("=" * 100)
    for name, label, z, matches in flagged_systems:
        print(f"\n{name}: claimed '{label}' at z={z:.2f} sigma")
        if len(matches) > 1:
            print(f"  Multiple candidates within 2-sigma: {matches}")
            print(f"  -> The specific label '{label}' is NOT uniquely preferred by the data;")
            print(f"     any of {matches} would fit equally well. This is a look-elsewhere-effect")
            print(f"     problem identical in kind to the index-gap assignment issue (Section 5.5).")
        elif z >= 2.0:
            print(f"  The claimed ratio is >2-sigma from the fitted value -- NOT a statistically")
            print(f"  supported match. This label should be removed or heavily caveated.")

    print("\n" + "=" * 100)
    print(f"SUMMARY: {len(flagged_systems)} of {len(SYSTEMS)} systems have an unsupported or")
    print(f"non-unique 'nice ratio' label out of {len(SYSTEMS)} total systems checked.")
    print("=" * 100)

if __name__ == '__main__':
    main()
