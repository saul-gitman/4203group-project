"""Baseline: same flights with margin R + k*sigma_h vs R only (20 seeds each).

    python code/analysis/baseline.py
"""
import sys
import pathlib
CODE = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CODE))
import numpy as np, main as M, params as P

def fly(target, over, seed, seconds=60, change=None):
    M.set_params(over)
    f = M.Flight(M.START, target, seed=seed)
    zmin = 1e9
    for k in range(seconds):
        if change and k == change[0]:
            for n, v in change[1].items(): setattr(P, n, v)
        zmin = min(zmin, f.step()["clearance"][0])
    return zmin

cases = [("open sky", {}, None), ("canyon 40deg", {"SKY_MASK_DEG": 40.0}, None),
         ("sigma_UERE 10 m", {"SIGMA_UERE": 10.0}, None),
         ("outage t=10 s", {}, (10, {"SKY_MASK_DEG": 50.0}))]
for name, over, ch in cases:
    for lab, extra in (("R + k*sigma_h", {}), ("R only", {"K_SIGMA": 0.0})):
        z = np.array([fly(M.ZONE_TARGET, {**over, **extra}, s, change=ch) for s in range(1, 21)])
        print(f"{name:16s} {lab:14s} mean {z.mean():6.1f}  worst {z.min():6.1f}  breaches {(z < P.R_DRONE).sum()}/20")
M.set_params({})
