#!/usr/bin/env python3
"""
Eigenmode Orbital Dynamics — Python/Matplotlib + FFmpeg Simulation & Video Renderer
Rick Drayson | Research Visualisation Suite

Generates:
1. High-Resolution Multi-Panel PNG Snapshot ('eigenmode_orbital_snapshot.png')
2. Full 1080p MP4 Simulation Video ('eigenmode_orbital_simulation.mp4')
   visualizing rotating planetary bodies trapped in magnetohydrodynamic standing-wave potential wells.
"""

import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle

# Output Paths
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
SNAPSHOT_PATH = os.path.join(OUTPUT_DIR, 'eigenmode_orbital_snapshot.png')
VIDEO_PATH = os.path.join(OUTPUT_DIR, 'eigenmode_orbital_simulation.mp4')

# Solar System Data
BODIES = [
    {"name": "Mercury", "n": 1, "r": 0.3871, "color": "#a0a0a0", "size": 6},
    {"name": "Venus",   "n": 2, "r": 0.7233, "color": "#e3bb76", "size": 9},
    {"name": "Earth",   "n": 3, "r": 1.0000, "color": "#2277ff", "size": 10},
    {"name": "Mars",    "n": 4, "r": 1.5237, "color": "#cc4422", "size": 8},
    {"name": "Ceres",   "n": 5, "r": 2.7675, "color": "#d4a373", "size": 5, "is_belt": True},
    {"name": "Jupiter", "n": 6, "r": 5.2044, "color": "#d4a373", "size": 18},
    {"name": "Saturn",  "n": 7, "r": 9.5826, "color": "#f4e2bb", "size": 15},
    {"name": "Uranus",  "n": 8, "r": 19.2184, "color": "#70d6ff", "size": 12},
    {"name": "Neptune", "n": 9, "r": 30.1104, "color": "#3a86ff", "size": 12},
    {"name": "Pluto",   "n": 10, "r": 39.4820, "color": "#c8b6ff", "size": 6}
]

R0 = 0.21355
LAMBDA = 0.5373
K = np.exp(LAMBDA)
KAPPA = np.pi / LAMBDA

def setup_figure():
    fig = plt.figure(figsize=(16, 9), facecolor='#030611')
    gs = fig.add_gridspec(2, 2, width_ratios=[1.25, 1.0], height_ratios=[1.0, 1.0],
                           left=0.05, right=0.95, top=0.90, bottom=0.08, wspace=0.18, hspace=0.25)
    
    # Title
    fig.suptitle("EIGENMODE ORBITAL DYNAMICS — MACROSCOPIC STANDING WAVE RESONATOR",
                 fontsize=14, fontweight='bold', color='#48cae4', y=0.96)
    
    # 1. Main Orbital Plane (Left)
    ax_orbit = fig.add_subplot(gs[:, 0], facecolor='#02040a')
    ax_orbit.set_title("Circumstellar Standing-Wave Potential Sheaths & Quantized Nodes (r_n = r₀ · kⁿ)",
                       fontsize=10, color='#90e0ef', pad=10)
    ax_orbit.set_aspect('equal')
    
    # 2. 1D Radial Wave Potential (Top Right)
    ax_wave = fig.add_subplot(gs[0, 1], facecolor='#040914')
    ax_wave.set_title("Radial Standing Wave: ψ(r) = A · sin(κ · ln(r/r₀))",
                      fontsize=10, color='#90e0ef')
    
    # 3. Log-Linear Regression (Bottom Right)
    ax_log = fig.add_subplot(gs[1, 1], facecolor='#040914')
    ax_log.set_title("Harmonic Index Quantization: ln(r_n) = 0.5373·n - 1.5439 (R² = 0.9934)",
                     fontsize=10, color='#90e0ef')
    
    return fig, ax_orbit, ax_wave, ax_log

def render_snapshot_and_video(fps=24, duration_sec=5):
    fig, ax_orbit, ax_wave, ax_log = setup_figure()
    
    # Normalize radii for visual clarity on 2D orbital plane
    max_r = 42.0
    r_disp = [np.power(b['r'] / max_r, 0.45) * 40.0 for b in BODIES]
    
    # Draw Background Standing Wave Bands on Orbital Plane
    theta = np.linspace(0, 2*np.pi, 200)
    for n in range(1, 11):
        r_node = R0 * (K ** n)
        r_d = np.power(r_node / max_r, 0.45) * 40.0
        ax_orbit.plot(r_d * np.cos(theta), r_d * np.sin(theta),
                      color='#00f0ff', alpha=0.25, linestyle='-', linewidth=1.0)
    
    # Draw Central Star
    ax_orbit.scatter([0], [0], color='#ffaa00', s=220, zorder=10, edgecolors='#ffffff', linewidth=1.5)
    ax_orbit.text(0, -3.0, "SOL (Central Core)", color='#ffd166', fontsize=8, ha='center', va='top')
    
    # Predicted Outer Band (n=11)
    r_pred = R0 * (K ** 11)
    r_pred_d = np.power(r_pred / max_r, 0.45) * 40.0
    ax_orbit.plot(r_pred_d * np.cos(theta), r_pred_d * np.sin(theta),
                  color='#ffd166', alpha=0.6, linestyle='--', linewidth=1.2, label='Predicted n=11 Shell')
    
    ax_orbit.set_xlim(-46, 46)
    ax_orbit.set_ylim(-46, 46)
    ax_orbit.axis('off')
    
    # Static setup for 1D Radial Wave Potential
    u_vals = np.linspace(0, 11 * LAMBDA, 500)
    r_vals = R0 * np.exp(u_vals)
    psi_vals = np.sin(KAPPA * u_vals)
    
    ax_wave.axhline(0, color='#778da9', linestyle=':', alpha=0.5)
    wave_line, = ax_wave.plot(u_vals / LAMBDA, psi_vals, color='#00f0ff', linewidth=2.0, label='ψ(r)')
    
    for b in BODIES:
        u_b = np.log(b['r'] / R0)
        n_pos = u_b / LAMBDA
        ax_wave.scatter([n_pos], [0], color=b['color'], s=50, zorder=5)
        ax_wave.text(n_pos, 0.15, b['name'], color='#e0e8f5', fontsize=7, rotation=45, ha='left')
        
    ax_wave.set_xlabel("Harmonic Mode Index n = ln(r/r₀) / λ", color='#a0aec0', fontsize=8)
    ax_wave.set_ylabel("Wave Amplitude ψ(r)", color='#a0aec0', fontsize=8)
    ax_wave.tick_params(colors='#a0aec0', labelsize=8)
    ax_wave.grid(True, color='#1b263b', alpha=0.5)
    ax_wave.set_ylim(-1.4, 1.4)
    ax_wave.set_xlim(0.5, 11.5)
    
    # Static setup for Log-Linear Regression
    n_arr = np.array([b['n'] for b in BODIES])
    ln_r_obs = np.array([np.log(b['r']) for b in BODIES])
    
    n_line = np.linspace(0.8, 11.2, 100)
    ln_r_model = LAMBDA * n_line + np.log(R0)
    
    ax_log.plot(n_line, ln_r_model, color='#00f0ff', linewidth=2.0, label='Model: ln(r) = λ·n + ln(r₀)')
    ax_log.scatter(n_arr, ln_r_obs, color='#ffd166', s=45, zorder=5, label='Observed (AU)')
    
    for b in BODIES:
        ax_log.text(b['n'] + 0.15, np.log(b['r']), b['name'], color='#e0e8f5', fontsize=7, va='center')
        
    ax_log.set_xlabel("Integer Harmonic Index (n)", color='#a0aec0', fontsize=8)
    ax_log.set_ylabel("ln(Semi-Major Axis in AU)", color='#a0aec0', fontsize=8)
    ax_log.tick_params(colors='#a0aec0', labelsize=8)
    ax_log.grid(True, color='#1b263b', alpha=0.5)
    ax_log.legend(loc='lower right', facecolor='#0d1b2a', edgecolor='#415a77', fontsize=7, labelcolor='#e0e8f5')
    
    # Save High-Resolution Snapshot
    fig.savefig(SNAPSHOT_PATH, dpi=200, facecolor=fig.get_facecolor(), edgecolor='none')
    print(f"✅ High-resolution snapshot saved to: {SNAPSHOT_PATH}")
    
    # Animation Objects
    total_frames = fps * duration_sec
    planet_scatters = []
    trail_lines = []
    trails_x = [[] for _ in BODIES]
    trails_y = [[] for _ in BODIES]
    
    for i, b in enumerate(BODIES):
        sc = ax_orbit.scatter([], [], color=b['color'], s=b['size']*3, zorder=6)
        tr, = ax_orbit.plot([], [], color=b['color'], alpha=0.4, linewidth=1.0)
        planet_scatters.append(sc)
        trail_lines.append(tr)
    
    def update(frame):
        t = (frame / total_frames) * 2 * np.pi
        
        # 1. Update Planet Positions
        for i, b in enumerate(BODIES):
            omega = 3.0 / np.power(b['n'], 1.2)
            angle = omega * t
            rd = r_disp[i]
            x = rd * np.cos(angle)
            y = rd * np.sin(angle)
            
            planet_scatters[i].set_offsets([[x, y]])
            
            trails_x[i].append(x)
            trails_y[i].append(y)
            if len(trails_x[i]) > 30:
                trails_x[i].pop(0)
                trails_y[i].pop(0)
            trail_lines[i].set_data(trails_x[i], trails_y[i])
            
        # 2. Oscillate Radial Standing Wave
        psi_t = np.sin(KAPPA * u_vals - t * 2.0)
        wave_line.set_ydata(psi_t)
        
        return planet_scatters + trail_lines + [wave_line]

    print(f"🎬 Rendering MP4 Simulation Video ({total_frames} frames @ {fps} fps)...")
    ani = animation.FuncAnimation(fig, update, frames=total_frames, interval=1000/fps, blit=True)
    
    try:
        ani.save(VIDEO_PATH, writer='ffmpeg', fps=fps, dpi=140,
                 extra_args=['-vcodec', 'libx264', '-pix_fmt', 'yuv420p'])
        print(f"✅ Simulation video successfully saved to: {VIDEO_PATH}")
    except Exception as e:
        print(f"⚠️ FFmpeg video rendering failed: {e}")
    finally:
        plt.close(fig)

if __name__ == '__main__':
    render_snapshot_and_video(fps=24, duration_sec=6)
