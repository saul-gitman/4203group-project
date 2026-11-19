"""Landscape flowchart panels (blue / purple / grey) for the Morph zoom slides."""
W, H = 2350, 875
BLUE, BLUE_T = "#2A64AD", "#E8EFF8"
PURP, PURP_T = "#7A3FA6", "#F2EAF8"
GREY, GREY_T = "#5F6B7A", "#EEF0F3"
INK, MUTED, EDGE = "#1F2933", "#55606E", "#6B7785"
ST = {"CLEAR": ("#1D7F47", "#E3F3EA"), "BRAKE": ("#A35F00", "#FBF0DC"),
      "TURN": ("#0B7880", "#DEF2F3"), "RETURN": ("#B33327", "#F8E4E1")}

def head(bg):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
            f'font-family="Arial, Liberation Sans, sans-serif">'
            f'<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" '
            f'orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{EDGE}"/></marker></defs>'
            f'<rect width="{W}" height="{H}" fill="{bg}"/>')

def box(cx, cy, lines, w=290, h=150, stroke=EDGE, fill="#FFFFFF", sw=4, dash=False, name_size=42, sub_size=36, name_fill=INK):
    x, y = cx - w / 2, cy - h / 2
    d = ' stroke-dasharray="14 10"' if dash else ""
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>'
    n = len(lines)
    gap = 46
    top = cy - (n - 1) * gap / 2
    for i, t in enumerate(lines):
        size, weight, col = (name_size, 700, name_fill) if i == 0 else (sub_size, 400, MUTED)
        s += (f'<text x="{cx}" y="{top + i * gap + size * 0.35}" font-size="{size}" font-weight="{weight}" '
              f'fill="{col}" text-anchor="middle">{t}</text>')
    return s

def diamond(cx, cy, hw, hh, text, stroke=EDGE, size=40):
    return (f'<polygon points="{cx-hw},{cy} {cx},{cy-hh} {cx+hw},{cy} {cx},{cy+hh}" fill="#FFFFFF" '
            f'stroke="{stroke}" stroke-width="4"/>'
            f'<text x="{cx}" y="{cy + size*0.35}" font-size="{size}" font-weight="700" fill="{INK}" text-anchor="middle">{text}</text>')

def arrow(d, dash=False):
    dd = ' stroke-dasharray="12 9"' if dash else ""
    return f'<path d="{d}" fill="none" stroke="{EDGE}" stroke-width="4"{dd} marker-end="url(#a)"/>'

def label(x, y, t, size=34, anchor="start", fill=MUTED, weight=400, italic=False):
    st = ' font-style="italic"' if italic else ""
    return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"{st}>{t}</text>'

# ---------------------------------------------------------------- blue
def blue():
    c = [165, 500, 835, 1170, 1505, 1840, 2175]
    rA, rB, rC = 110, 437, 765
    s = head(BLUE_T)
    s += box(c[0], rA, ["GNSS", "ρ, Doppler"], dash=True)
    s += diamond(c[1], rA, 150, 80, "≥ 4 sats?")
    s += box(c[2], rA, ["Klobuchar", "ρ − I_iono"])
    s += box(c[3], rA, ["SPP LSQ", "(HᵀH)⁻¹HᵀΔρ"])
    s += box(c[4], rA, ["Error σ_h", "HDOP·σ_UERE"], stroke=BLUE, sw=5)
    s += box(c[6], rA, ["eSUA zones", "lat/lon → NED"], dash=True, w=300)
    s += box(535, rB, ["No fix:", "dead reckoning", "σ_h grows ½σ_a·t²"], w=380, h=170)
    s += box(c[3], rB, ["Doppler LSQ", "→ v_GNSS"], w=300)
    s += box(c[4], rB, ["Blend v", "σ²-weighted"])
    s += box(c[5], rB, ["Nav state", "p, v, σ_h"], stroke=BLUE, sw=6)
    s += box(c[6], rB, ["Zone threat", "R + k·σ_h"], w=300, stroke=BLUE, fill="#FFFFFF", sw=9, name_fill=BLUE)
    s += box(c[0], rC, ["IMU", "accel, heading"], dash=True)
    s += box(c[2], rC, ["IMU velocity", "v + a·dt"], w=300)
    # arrows
    s += arrow(f"M{c[0]+145} {rA} H{c[1]-150}")
    s += arrow(f"M{c[1]+150} {rA} H{c[2]-145}")
    s += arrow(f"M{c[2]+145} {rA} H{c[3]-145}")
    s += arrow(f"M{c[3]+145} {rA} H{c[4]-145}")
    s += arrow(f"M{c[4]+145} {rA} H{c[5]} V{rB-75}") + label(c[4] + 165, rA - 22, "p, σ_h")
    s += arrow(f"M{c[1]} {rA+80} V{rB-85}") + label(c[1] + 16, 290, "no: GNSS outage")
    s += arrow(f"M{c[3]} {rA+75} V{rB-75}") + label(c[3] + 16, 290, "same H")
    s += arrow(f"M{c[3]+150} {rB} H{c[4]-145}")
    s += arrow(f"M{c[4]+145} {rB} H{c[5]-145}") + label(c[4] + 165, rB - 22, "v")
    s += arrow(f"M{c[5]+145} {rB} H{c[6]-150}")
    s += arrow(f"M{c[6]} {rA+75} V{rB-75}")
    s += arrow(f"M535 {rB+85} V610 H{c[5]} V{rB+75}")
    s += label(1000, 596, "IMU-only p, v and a growing σ_h", size=32)
    s += arrow(f"M{c[0]+145} {rC} H{c[2]-150}")
    s += arrow(f"M{c[2]+150} {rC} H{c[4]} V{rB+75}") + label(c[2] + 170, rC - 22, "v_IMU")
    s += label(W - 30, H - 22, "FLOW 1 · GNSS + IMU → zones", size=34, anchor="end", fill=BLUE, weight=700)
    return s + "</svg>"

# ---------------------------------------------------------------- purple
def purple():
    xs, cy = [230, 690, 1150, 1610, 2060], 160
    s = head(PURP_T)
    s += box(xs[0], cy, ["Radar", "range, bearing"], w=380, h=170, dash=True)
    s += box(xs[1], cy, ["Unit vector", "sensor frame"], w=380, h=170)
    s += box(xs[2], cy, ["× R_bs", "mount → body"], w=380, h=170)
    s += box(xs[3], cy, ["× R_nb", "body → NED"], w=380, h=170)
    s += box(xs[4], cy, ["Building threat", "R + k·σ_range"], w=420, h=170, stroke=PURP, sw=9, name_fill=PURP)
    for a, b, wa, wb in ((0, 1, 190, 190), (1, 2, 190, 190), (2, 3, 190, 190), (3, 4, 190, 210)):
        s += arrow(f"M{xs[a]+wa} {cy} H{xs[b]-wb}")
    s += box(xs[3], 380, ["heading ψ", "from the IMU"], w=320, h=110, dash=True, name_size=36, sub_size=30)
    s += arrow(f"M{xs[3]} {325} V{cy+85}", dash=True)
    s += label(xs[4] - 200, 290, "range d, direction u", size=34)
    s += label(70, 520, "No GNSS anywhere in this chain.", size=64, fill=PURP, weight=700)
    s += label(70, 600, "The radar measures the distance itself, so the", size=40, fill=INK)
    s += label(70, 655, "margin uses the radar's own error, not σ_h:", size=40, fill=INK)
    s += label(70, 745, "R + k·σ_range = 3 + 3.03 × 0.5 ≈ 4.5 m", size=48, fill=INK, weight=700)
    ax, ay = 1350, 640
    s += f'<circle cx="{ax}" cy="{ay}" r="220" fill="none" stroke="{PURP}" stroke-width="4" stroke-dasharray="16 12"/>'
    s += label(1115, 820, "radar range 150 m", size=32, anchor="end", fill=PURP)
    s += f'<rect x="1540" y="540" width="180" height="220" fill="#FFFFFF" stroke="{PURP}" stroke-width="5"/>'
    s += f'<rect x="1522" y="522" width="216" height="256" fill="none" stroke="{PURP}" stroke-width="3" stroke-dasharray="10 8"/>'
    s += label(1630, 662, "tower", size=34, anchor="middle", fill=PURP, weight=700)
    s += label(1750, 540, "margin", size=30, anchor="start", fill=PURP)
    s += f'<circle cx="{ax}" cy="{ay}" r="20" fill="{INK}"/>'
    s += f'<path d="M{ax+22} {ay} H1518" stroke="{INK}" stroke-width="5" marker-end="url(#a)"/>'
    s += label((ax + 1520) / 2, ay - 18, "d", size=40, anchor="middle", fill=INK, weight=700, italic=True)
    s += label(W - 30, H - 22, "FLOW 2 · radar → buildings", size=34, anchor="end", fill=PURP, weight=700)
    return s + "</svg>"

# ---------------------------------------------------------------- grey
def grey():
    s = head(GREY_T)
    cells = [("closing speed", ["v_c = −v·n̂"]), ("room left", ["gap = d − margin"]),
             ("reaction", ["d_react = v_c·Δt"]), ("braking", ["d_react", "+ v_c² / 2a"]),
             ("turning", ["d_react", "+ R(1 − sin α)"]), ("allowed speed", ["v_allow so that", "d_brake = gap"])]
    x0, cw, gp, y0, ch = 30, 365, 22, 30, 200
    for i, (lab, fs) in enumerate(cells):
        x = x0 + i * (cw + gp)
        s += f'<rect x="{x}" y="{y0}" width="{cw}" height="{ch}" rx="14" fill="#FFFFFF" stroke="{GREY}" stroke-width="4"/>'
        s += label(x + cw / 2, y0 + 50, lab, size=34, anchor="middle")
        for j, f in enumerate(fs):
            s += label(x + cw / 2, y0 + 112 + j * 50, f, size=38, anchor="middle", fill=INK, weight=700)
    s += label(30, 290, "Per threat, every epoch. Δt = 1.6 s, a = 2.5 m/s², R = 50 m. The most urgent threat wins: max(v_c − v_allow).", size=34)
    ry, oy = 450, 735
    s += diamond(300, ry, 230, 95, "gap ≤ 0 ?")
    s += diamond(900, ry, 260, 95, "v_c ≤ v_allow ?", size=38)
    s += diamond(1500, ry, 250, 95, "gap ≥ d_turn ?", size=38)
    def st(cx, cy, name, sub, w=400):
        col, tint = ST[name]
        return box(cx, cy, [name, sub], w=w, h=150, stroke=col, fill=tint, sw=6, name_fill=col, name_size=46)
    s += st(2060, ry, "BRAKE", "slow to v_allow", w=420)
    s += st(300, oy, "RETURN", "back off at 2 m/s")
    s += st(900, oy, "CLEAR", "pilot command passes")
    s += st(1500, oy, "TURN", "fly along the edge")
    s += arrow(f"M530 {ry} H{900-260}") + label(585, ry - 20, "no", anchor="middle")
    s += arrow(f"M1160 {ry} H{1500-250}") + label(1205, ry - 20, "no", anchor="middle")
    s += arrow(f"M1750 {ry} H{2060-210}") + label(1800, ry - 20, "no", anchor="middle")
    for cx in (300, 900, 1500):
        s += arrow(f"M{cx} {ry+95} V{oy-75}") + label(cx + 16, ry + 135, "yes")
    s += label(1855, 690, "Below 15.8 m/s braking", size=36, fill=INK)
    s += label(1855, 738, "is shorter; above it,", size=36, fill=INK)
    s += label(1855, 786, "turning is.", size=36, fill=INK)
    s += label(W - 30, H - 22, "DECISION · boundary.py", size=34, anchor="end", fill=GREY, weight=700)
    return s + "</svg>"

if __name__ == "__main__":
    import pathlib
    out = pathlib.Path(__file__).resolve().parents[1] / "assets"
    for name, fn in (("blue", blue), ("purple", purple), ("grey", grey)):
        (out / f"flow_{name}.svg").write_text(fn(), encoding="utf-8")
    print("ok")
