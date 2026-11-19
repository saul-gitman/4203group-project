"""Flight 1 (zone, 10 m/s) and flight 2 (tower, 20 m/s) plot for the deck.

    python code/analysis/trajectories.py [out.png]
"""
import sys, json
import pathlib
CODE = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CODE))
import numpy as np, main as M, params as P, sim
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle
from matplotlib.lines import Line2D

COL = {"CLEAR": "#1D7F47", "BRAKE": "#A35F00", "TURN": "#0B7880", "RETURN": "#B33327", "HOLD": "#55606E"}
BLUE, PURP, INK, MUTED = "#2A64AD", "#7A3FA6", "#1F2933", "#55606E"

def fly(target, over, secs):
    M.set_params(over)
    f = M.Flight(M.START, target, seed=1)
    segs, info = [], []
    for k in range(secs):
        prev = f.world.p.copy()
        r = f.step()
        tr = [prev] + list(f.world.track)
        segs.append((np.array(tr), r["dec"].state))
        info.append((k, r["dec"].state, r["clearance"], r["nav"].sigma_h))
    zones = f.zones
    M.set_params({})
    return segs, zones, info

plt.rcParams.update({"font.family": "Liberation Sans", "font.size": 15})
fig, axes = plt.subplots(1, 2, figsize=(12.4, 4.6), dpi=200)
out = {}
for ax, (title, target, over, secs) in zip(axes, [
        ("Flight 1 · 10 m/s at the zone", M.ZONE_TARGET, {}, 45),
        ("Flight 2 · 20 m/s at the tower", M.BUILDING_TARGET, {"V_MAX": 20.0}, 36)]):
    segs, zones, info = fly(target, over, secs)
    for z in zones:
        ne = z.ne
        ax.add_patch(Polygon(np.c_[ne[:, 1], ne[:, 0]], closed=True, fc="#E8EFF8", ec=BLUE, lw=2))
    for name, poly in sim.BUILDINGS.items():
        ax.add_patch(Polygon(np.c_[poly[:, 1], poly[:, 0]], closed=True, fc="#F2EAF8", ec=PURP, lw=2))
    for tr, st in segs:
        ax.plot(tr[:, 1], tr[:, 0], color=COL.get(st, MUTED), lw=3.2, solid_capstyle="round")
    ax.plot(0, 0, "o", color=INK, ms=7)
    ax.plot(target[1], target[0], "x", color=INK, ms=10, mew=2.5)
    ax.set_title(title, loc="left", fontsize=17, fontweight="bold", color=INK)
    ax.set_aspect("equal"); ax.grid(color="#E3E7EC", lw=0.8)
    ax.set_xlabel("East (m)", color=MUTED); ax.set_ylabel("North (m)", color=MUTED)
    for s in ax.spines.values(): s.set_color("#C3CCD6")
    ax.tick_params(colors=MUTED)
    states = [i[1] for i in info]
    first = {s: next(k for k, x in enumerate(states) if x == s) for s in set(states)}
    out[title] = {"first": first, "min_zone": min(i[2][0] for i in info), "min_bldg": min(i[2][1] for i in info)}
axes[0].set_xlim(-30, 360); axes[0].set_ylim(-30, 350)
axes[1].set_xlim(-420, 60); axes[1].set_ylim(-40, 390)
axes[0].text(165, 180, "eSUA zone\n(example)", color=BLUE, fontsize=14, fontweight="bold")
axes[1].text(-118, 168, "tower", color=PURP, fontsize=14, fontweight="bold")
handles = [Line2D([0], [0], color=COL[s], lw=4, label=s) for s in ("CLEAR", "BRAKE", "TURN", "RETURN")]
handles += [Line2D([0], [0], marker="o", color=INK, lw=0, label="start"), Line2D([0], [0], marker="x", color=INK, lw=0, mew=2.5, ms=9, label="pilot's target")]
fig.legend(handles=handles, loc="lower center", ncol=6, frameon=False, fontsize=14)
fig.tight_layout(rect=(0, 0.08, 1, 1))
fig.savefig(sys.argv[1] if len(sys.argv) > 1 else str(CODE.parent / "presentation" / "assets" / "trajectories.png"), dpi=200, facecolor="white")
print(json.dumps(out, indent=1, default=str))
