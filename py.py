"""
Waves & Oscillations Simulator
================================
Visualizes key wave and oscillation concepts:
  1. Simple Harmonic Motion (mass-spring)
  2. Damped oscillation
  3. Transverse wave propagation
  4. Wave superposition / interference
  5. Standing waves

Developed for educational purposes (2021-2023).
Requirements: matplotlib, numpy
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# ─── Wave functions ───────────────────────────────

def shm(t, A=1.0, omega=2*np.pi, phi=0):
    return A * np.cos(omega*t + phi)

def damped_osc(t, A=1.0, omega=2*np.pi, gamma=0.5):
    """x(t) = A·e^(-γt)·cos(ω·t)"""
    return A * np.exp(-gamma * t) * np.cos(omega * t)

def traveling_wave(x, t, A=1.0, f=1.0, lam=1.0, direction=1):
    """y(x,t) = A·sin(2π(x/λ - f·t))  direction: +1 right, -1 left"""
    k = 2*np.pi / lam
    omega = 2*np.pi * f
    return A * np.sin(k*x - direction*omega*t)

def standing_wave(x, t, A=1.0, f=1.0, lam=1.0, n=1):
    """y(x,t) = 2A·sin(kx)·cos(ωt)"""
    k = n * np.pi / lam   # for a string of length lam
    omega = 2*np.pi * f
    return 2*A * np.sin(k*x) * np.cos(omega*t)

# ─── Main ─────────────────────────────────────────

def main():
    print("=" * 55)
    print("  WAVES & OSCILLATIONS SIMULATOR")
    print("=" * 55)

    t = np.linspace(0, 4, 800)   # time array (seconds)
    x = np.linspace(0, 2, 400)   # space array (metres)

    fig = plt.figure(figsize=(14, 12))
    fig.suptitle("Waves & Oscillations — Physics Simulation", fontsize=15, fontweight="bold")
    gs = gridspec.GridSpec(3, 2, figure=fig, hspace=0.5, wspace=0.35)

    # ── 1. SHM ──────────────────────────────────
    ax1 = fig.add_subplot(gs[0, 0])
    for A, lw, label in [(1.0, 2.5, "A=1.0 m"), (0.6, 1.8, "A=0.6 m"), (0.3, 1.2, "A=0.3 m")]:
        ax1.plot(t, shm(t, A=A, omega=2*np.pi), linewidth=lw, label=label)
    ax1.axhline(0, color="black", linewidth=0.5)
    ax1.set_title("Simple Harmonic Motion\n(mass-spring, f = 1 Hz)")
    ax1.set_xlabel("Time (s)"); ax1.set_ylabel("Displacement (m)")
    ax1.legend(fontsize=8); ax1.grid(True, alpha=0.3)

    # ── 2. Damped oscillation ────────────────────
    ax2 = fig.add_subplot(gs[0, 1])
    t_long = np.linspace(0, 6, 800)
    for gamma, label, color in [
        (0.1, "Light damping γ=0.1",    "#4CAF50"),
        (0.5, "Medium damping γ=0.5",   "#FF9800"),
        (1.5, "Heavy damping γ=1.5",    "#F44336"),
    ]:
        y = damped_osc(t_long, gamma=gamma)
        ax2.plot(t_long, y, linewidth=2, label=label, color=color)
    ax2.plot(t_long,  np.exp(-0.5*t_long), "k--", linewidth=1, alpha=0.5, label="Envelope (γ=0.5)")
    ax2.plot(t_long, -np.exp(-0.5*t_long), "k--", linewidth=1, alpha=0.5)
    ax2.axhline(0, color="black", linewidth=0.5)
    ax2.set_title("Damped Oscillation")
    ax2.set_xlabel("Time (s)"); ax2.set_ylabel("Displacement (m)")
    ax2.legend(fontsize=8); ax2.grid(True, alpha=0.3)

    # ── 3. Traveling wave snapshots ──────────────
    ax3 = fig.add_subplot(gs[1, 0])
    snapshots = [0, 0.25, 0.5, 0.75]
    cmap = plt.cm.viridis
    for i, t_snap in enumerate(snapshots):
        y = traveling_wave(x, t_snap, A=0.8, f=1.5, lam=0.8)
        ax3.plot(x, y, linewidth=2, color=cmap(i/len(snapshots)), label=f"t={t_snap} s")
    ax3.axhline(0, color="black", linewidth=0.5)
    ax3.set_title("Traveling Wave Snapshots\n(right-moving, f=1.5 Hz, λ=0.8 m)")
    ax3.set_xlabel("Position (m)"); ax3.set_ylabel("Amplitude (m)")
    ax3.legend(fontsize=8); ax3.grid(True, alpha=0.3)

    # ── 4. Wave superposition / interference ─────
    ax4 = fig.add_subplot(gs[1, 1])
    y1 = traveling_wave(x, 0, A=0.8, f=1.5, lam=0.8, direction=+1)
    y2 = traveling_wave(x, 0, A=0.8, f=1.5, lam=0.8, direction=-1)
    ax4.plot(x, y1, "--", color="#2196F3",  linewidth=1.5, label="Wave →")
    ax4.plot(x, y2, "--", color="#F44336",  linewidth=1.5, label="Wave ←")
    ax4.plot(x, y1 + y2, "-",  color="#212121", linewidth=2.5, label="Superposition")
    ax4.axhline(0, color="black", linewidth=0.5)
    ax4.set_title("Wave Superposition\n(two equal waves, opposite directions)")
    ax4.set_xlabel("Position (m)"); ax4.set_ylabel("Amplitude (m)")
    ax4.legend(fontsize=8); ax4.grid(True, alpha=0.3)

    # ── 5. Standing waves (harmonics) ───────────
    ax5 = fig.add_subplot(gs[2, :])
    colors5 = ["#E91E63","#9C27B0","#2196F3","#4CAF50"]
    t0 = 0
    L = 2.0   # string length
    xx = np.linspace(0, L, 400)
    for n, color in zip([1, 2, 3, 4], colors5):
        k = n * np.pi / L
        omega = 2*np.pi * n
        y = 2 * np.sin(k*xx) * np.cos(omega*t0)
        ax5.plot(xx, y + (n-1)*2.5, linewidth=2, color=color, label=f"n={n} harmonic")
        # mark nodes
        node_xs = [i*L/n for i in range(n+1)]
        for nx in node_xs:
            ax5.plot(nx, (n-1)*2.5, "o", color=color, markersize=5)
        ax5.axhline((n-1)*2.5, color="gray", linewidth=0.4, linestyle=":")
    ax5.set_title("Standing Waves — First 4 Harmonics\n(circles = nodes)")
    ax5.set_xlabel("Position (m)"); ax5.set_ylabel("Harmonic (offset for clarity)")
    ax5.legend(fontsize=9, loc="upper right"); ax5.grid(True, alpha=0.3)
    ax5.set_yticks([]); ax5.set_xlim(0, L)

    plt.savefig("5_waves_oscillations.png", dpi=120, bbox_inches="tight")
    print("\nSaved → 5_waves_oscillations.png")
    plt.show()

    # Phase space portrait (SHM)
    fig2, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig2.suptitle("Phase Space Portraits", fontsize=13, fontweight="bold")

    omega = 2*np.pi
    t_fine = np.linspace(0, 4, 2000)

    ax_a, ax_b = axes
    for A, color in [(1.0,"#2196F3"),(0.6,"#4CAF50"),(0.3,"#F44336")]:
        x_pos = shm(t_fine, A=A, omega=omega)
        x_vel = -A * omega * np.sin(omega*t_fine)
        ax_a.plot(x_pos, x_vel, color=color, linewidth=1.5, label=f"A={A}")
    ax_a.set_title("SHM — Phase Portrait\n(ellipses = energy levels)")
    ax_a.set_xlabel("Position (m)"); ax_a.set_ylabel("Velocity (m/s)")
    ax_a.legend(); ax_a.grid(True, alpha=0.3); ax_a.set_aspect("equal", adjustable="datalim")

    for gamma, color, label in [(0.1,"#4CAF50","γ=0.1"),(0.5,"#FF9800","γ=0.5"),(1.5,"#F44336","γ=1.5")]:
        xd = damped_osc(t_fine, gamma=gamma)
        vd = np.gradient(xd, t_fine)
        ax_b.plot(xd, vd, color=color, linewidth=1.5, label=label)
    ax_b.set_title("Damped Oscillation — Phase Portrait\n(spiral inward)")
    ax_b.set_xlabel("Position (m)"); ax_b.set_ylabel("Velocity (m/s)")
    ax_b.legend(); ax_b.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("5b_phase_portraits.png", dpi=120, bbox_inches="tight")
    print("Saved → 5b_phase_portraits.png")
    plt.show()

if __name__ == "__main__":
    main()