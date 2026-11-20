"""
brake_turn_svg.py - the velocity field, drawn two ways.

Left:  phase plane. x = gap (room left before the keep-out margin), y = closing
       speed v_c. The brake curve IS the velocity field v_allow(gap); the turn
       line is where a turn still fits. Their regions are the decision states.
Right: top-down view of the same example (20 m/s, 100 m from the margin):
       braking overshoots the margin, turning stays out.

    python brake_turn_svg.py      -> ../assets/brake_turn_field.svg
"""

import math
import pathlib

A, DT, R = 2.5, 1.6, 50.0          # params.py: A_BRAKE, DT, R_TURN
V0, G0 = 20.0, 100.0               # worked example: 20 m/s, 100 m from the margin

INK, MUTED, LINE, GRID = "#1F2933", "#5A6573", "#C3CCD6", "#E3E7EC"
GREY, TEAL, BLUE, RED = "#5F6B7A", "#0B7880", "#2A64AD", "#B33327"
T_CLEAR, T_TURN, T_LATE, T_RET = "#F2F4F6", "#E2F1F1", "#F8E7E5", "#F0D2CE"
FONT = "Arial, Helvetica, sans-serif"

W, H = 1600, 900
out = []


def add(s):
    out.append(s)


def text(x, y, s, size=18, fill=INK, anchor="start", weight="normal", italic=False):
    st = ' font-style="italic"' if italic else ""
    add(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" '
        f'font-weight="{weight}"{st}>{s}</text>')


def v_brake(g):                      # the velocity field: fastest v_c that still stops within g
    return A * (math.sqrt(DT ** 2 + 2 * g / A) - DT) if g > 0 else 0.0


def v_turn(g):                       # fastest v_c that still turns (head-on) within g
    return max((g - R) / DT, 0.0)


# ---------------------------------------------------------------- left panel
LX0, LX1, LY0, LY1 = 110, 960, 170, 760          # plot box in px
GMIN, GMAX, VMAX = -30.0, 150.0, 25.0


def px(g):
    return LX0 + (g - GMIN) / (GMAX - GMIN) * (LX1 - LX0)


def py(v):
    return LY1 - v / VMAX * (LY1 - LY0)


def path(pts):
    return "M" + " L".join(f"{px(g):.1f},{py(v):.1f}" for g, v in pts)


gs = [i * 0.5 for i in range(0, int(GMAX * 2) + 1)]
brake_pts = [(g, min(v_brake(g), VMAX)) for g in gs]
g_vt = R + DT * VMAX                                         # turn line leaves the top here
turn_pts = [(R, 0.0), (g_vt, VMAX)]
g_x = R + DT * math.sqrt(2 * A * R)                          # crossover, 75.3 m
v_x = math.sqrt(2 * A * R)                                   # 15.8 m/s

add(f'<rect x="0" y="0" width="{W}" height="{H}" fill="#FFFFFF"/>')
add(f'<g font-family="{FONT}">')

# regions
add(f'<rect x="{px(GMIN):.1f}" y="{LY0}" width="{px(0) - px(GMIN):.1f}" height="{LY1 - LY0}" fill="{T_RET}"/>')
add(f'<path d="{path([(0, VMAX), (0, 0)] + brake_pts + [(GMAX, VMAX)])} Z" fill="{T_LATE}"/>')
add(f'<path d="{path([(0, 0)] + brake_pts + [(GMAX, 0)])} Z" fill="{T_CLEAR}"/>')
upper = [(g, min(v_turn(g), VMAX)) for g in gs if g >= g_x]
lower = [(g, v_brake(g)) for g in gs if g >= g_x][::-1]
add(f'<path d="{path(upper + [(GMAX, VMAX)] + lower)} Z" fill="{T_TURN}"/>')

# grid + axes
for v in range(0, 26, 5):
    add(f'<line x1="{LX0}" x2="{LX1}" y1="{py(v):.1f}" y2="{py(v):.1f}" stroke="{GRID}" stroke-width="1"/>')
    text(LX0 - 12, py(v) + 6, str(v), 17, MUTED, "end")
for g in range(-20, 141, 20):
    text(px(g), LY1 + 28, str(g), 17, MUTED, "middle")
add(f'<line x1="{LX0}" x2="{LX1}" y1="{LY1}" y2="{LY1}" stroke="{LINE}" stroke-width="1.5"/>')
add(f'<line x1="{px(0):.1f}" x2="{px(0):.1f}" y1="{LY0}" y2="{LY1}" stroke="{BLUE}" stroke-width="2.5"/>')
text((LX0 + LX1) / 2, LY1 + 62, "gap = distance left before the keep-out margin  (m)", 19, MUTED, "middle")
text((LX0 + LX1) / 2, LY1 + 86, "← the aircraft flies this way as it closes in", 16, MUTED, "middle", italic=True)
add(f'<text transform="translate({LX0 - 62},{(LY0 + LY1) / 2}) rotate(-90)" font-size="19" fill="{MUTED}" '
    f'text-anchor="middle">closing speed v_c towards the zone (m/s)</text>')
text(px(0) + 8, LY0 + 22, "margin", 16, BLUE, weight="bold")
text(px(0) + 8, LY0 + 42, "R + k·σ_h", 16, BLUE)

# region labels
text(px(-15), py(13), "RETURN", 18, RED, "middle", "bold")
text(px(-15), py(12), "inside", 15, RED, "middle")
text(px(-15), py(11.1), "margin", 15, RED, "middle")
text(px(22), py(21.5), "TOO LATE FOR BOTH", 19, RED, weight="bold")
text(px(22), py(20.4), "brake anyway: crosses the margin", 16, INK)
text(px(114), py(23.6), "TURN", 19, TEAL, "middle", "bold")
text(px(114), py(22.6), "can't brake, can turn", 15, INK, "middle")
text(px(110), py(4.6), "CLEAR", 19, GREY, "middle", "bold")
text(px(110), py(3.4), "can still brake in time", 16, INK, "middle")

# the two boundary lines
add(f'<path d="{path(brake_pts)}" fill="none" stroke="{GREY}" stroke-width="4"/>')
add(f'<path d="{path(turn_pts)}" fill="none" stroke="{TEAL}" stroke-width="4"/>')
add(f'<line x1="{px(g_x):.1f}" x2="{px(g_x):.1f}" y1="{py(v_x):.1f}" y2="{LY1}" stroke="{MUTED}" '
    f'stroke-width="1.5" stroke-dasharray="5 5"/>')
add(f'<circle cx="{px(g_x):.1f}" cy="{py(v_x):.1f}" r="6" fill="#FFFFFF" stroke="{INK}" stroke-width="2"/>')
text(px(g_x) + 12, py(v_x) + 26, "15.8 m/s = √(2aR)", 16, INK)


# example 1: 10 m/s cruise at the zone (field caps the command)
g10 = 10 * DT + 100 / (2 * A)                                   # 36 m
ex1 = [(GMAX, 10.0), (g10, 10.0)] + [(g, v_brake(g)) for g in gs if g <= g10][::-1]
add(f'<path d="{path(ex1)}" fill="none" stroke="{INK}" stroke-width="2.5" stroke-dasharray="2 6" '
    f'stroke-linecap="round"/>')
add(f'<circle cx="{px(g10):.1f}" cy="{py(10):.1f}" r="7" fill="{INK}" stroke="#FFFFFF" stroke-width="2"/>')
text(px(80), py(12.3), "10 m/s cruise: meets the field at 36 m,", 16, INK)
text(px(80), py(11.3), "then BRAKE caps it down the curve", 16, INK)

# example 2: 20 m/s, 100 m out -> turn vs brake
s_r = V0 * DT
turn_path = [(G0, V0), (G0 - s_r, V0)] + [
    (G0 - s_r - s, V0 * math.sqrt(max(1 - (s / R) ** 2, 0))) for s in [i * 0.5 for i in range(0, 101)]]
brake_path = [(G0, V0), (G0 - s_r, V0)] + [
    (G0 - s_r - s, math.sqrt(max(V0 ** 2 - 2 * A * s, 0))) for s in [i * 0.5 for i in range(0, 161)]]
add(f'<path d="{path(brake_path)}" fill="none" stroke="{RED}" stroke-width="3" stroke-dasharray="9 6"/>')
add(f'<path d="{path(turn_path)}" fill="none" stroke="{TEAL}" stroke-width="3.5"/>')
add(f'<circle cx="{px(G0):.1f}" cy="{py(V0):.1f}" r="8" fill="{INK}" stroke="#FFFFFF" stroke-width="2"/>')
add(f'<line x1="{px(G0):.1f}" y1="{py(V0):.1f}" x2="{px(106):.1f}" y2="{py(17.3):.1f}" stroke="{INK}" stroke-width="1.2"/>')
text(px(106) + 4, py(16.8), "20 m/s, 100 m out", 17, INK, weight="bold")
add(f'<circle cx="{px(G0 - s_r - R):.1f}" cy="{py(0):.1f}" r="7" fill="{TEAL}" stroke="#FFFFFF" stroke-width="2"/>')
add(f'<circle cx="{px(G0 - s_r - V0 ** 2 / (2 * A)):.1f}" cy="{py(0):.1f}" r="7" fill="{RED}" '
    f'stroke="#FFFFFF" stroke-width="2"/>')
text(px(G0 - s_r - R) + 12, py(0) - 8, "18 m out", 15, TEAL, weight="bold")
text(px(G0 - s_r - V0 ** 2 / (2 * A)) - 12, py(0) - 8, "12 m in", 15, RED, "end", "bold")

text(LX0, 62, "The velocity field, with both ways out", 26, INK, weight="bold")
text(LX0, 94, "Below the grey curve the aircraft can still stop. The teal line adds the turn.", 18, MUTED)
lx, ly = LX0, 136
for item, label in (
        (f'<line x1="0" x2="34" y1="0" y2="0" stroke="{GREY}" stroke-width="4"/>', "brake curve = the velocity field v_allow(gap)"),
        (f'<line x1="0" x2="34" y1="0" y2="0" stroke="{TEAL}" stroke-width="4"/>', "turn line: gap = v·Δt + R"),
        (f'<line x1="0" x2="34" y1="0" y2="0" stroke="{RED}" stroke-width="3" stroke-dasharray="9 6"/>', "only brakes")):
    add(f'<g transform="translate({lx},{ly})">{item}</g>')
    text(lx + 42, ly + 6, label, 16, INK)
    lx += 42 + len(label) * 8.3 + 30

# ---------------------------------------------------------------- right panel
RX0, RX1 = 1060, 1540
add(f'<line x1="1010" x2="1010" y1="40" y2="860" stroke="{GRID}" stroke-width="1.5"/>')
text(RX0, 62, "Same case, seen from above", 26, INK, weight="bold")
text(RX0, 94, "20 m/s, 100 m from the margin", 18, MUTED)

S = 3.1                       # px per metre, top-down
ym = 240                      # y of the margin line (zone is above it)
MB = 18 * S                   # margin width, R + k·σ_h ≈ 3 + 3·5 m
x_mid = RX0 + 150             # straight-line track x


def ty(gap):
    return ym + gap * S


# zone + margin band
add(f'<rect x="{RX0 - 20}" y="118" width="{RX1 - RX0 + 40}" height="{ym - 118 - MB}" fill="{BLUE}" fill-opacity="0.16"/>')
add(f'<line x1="{RX0 - 20}" x2="{RX1 + 20}" y1="{ym - MB}" y2="{ym - MB}" stroke="{BLUE}" stroke-width="3"/>')
add(f'<rect x="{RX0 - 20}" y="{ym - MB}" width="{RX1 - RX0 + 40}" height="{MB}" fill="{BLUE}" fill-opacity="0.07"/>')
add(f'<line x1="{RX0 - 20}" x2="{RX1 + 20}" y1="{ym}" y2="{ym}" stroke="{BLUE}" stroke-width="2" stroke-dasharray="7 5"/>')
text(RX0, 146, "no-entry zone", 17, BLUE, weight="bold")
text(RX1 + 10, ym - 8, "margin R + k·σ_h ≈ 18 m", 15, BLUE, "end")

y_start, y_react = ty(G0), ty(G0 - s_r)
# shared reaction leg
add(f'<line x1="{x_mid}" x2="{x_mid}" y1="{y_start}" y2="{y_react}" stroke="{INK}" stroke-width="4" '
    f'stroke-dasharray="3 6" stroke-linecap="round"/>')
# brake leg (straight on, overshoots)
y_stop = ty(G0 - s_r - V0 ** 2 / (2 * A))
add(f'<line x1="{x_mid}" x2="{x_mid}" y1="{y_react}" y2="{y_stop}" stroke="{RED}" stroke-width="4" stroke-dasharray="10 6"/>')
add(f'<circle cx="{x_mid}" cy="{y_stop:.1f}" r="8" fill="{RED}" stroke="#FFFFFF" stroke-width="2"/>')
# turn leg: quarter circle of radius R, ends parallel to the edge
cx, cyy = x_mid + R * S, y_react
add(f'<path d="M{x_mid},{y_react:.1f} A{R * S:.1f},{R * S:.1f} 0 0 1 {cx:.1f},{cyy - R * S:.1f} L{RX1 + 10},{cyy - R * S:.1f}" '
    f'fill="none" stroke="{TEAL}" stroke-width="4"/>')
add(f'<polygon points="{RX1 + 18},{cyy - R * S:.1f} {RX1 + 4},{cyy - R * S - 8:.1f} {RX1 + 4},{cyy - R * S + 8:.1f}" fill="{TEAL}"/>')
add(f'<line x1="{x_mid}" x2="{cx:.1f}" y1="{y_react:.1f}" y2="{cyy:.1f}" stroke="{TEAL}" stroke-width="1.5" stroke-dasharray="4 4"/>')
text((x_mid + cx) / 2, y_react + 22, "R = 50 m", 16, TEAL, "middle", "bold")
# aircraft
add(f'<circle cx="{x_mid}" cy="{y_start:.1f}" r="11" fill="{INK}"/>')
add(f'<polygon points="{x_mid},{y_start - 30:.1f} {x_mid - 8},{y_start - 16:.1f} {x_mid + 8},{y_start - 16:.1f}" fill="{INK}"/>')
text(x_mid + 20, y_start + 6, "start: decision taken here", 16, INK)


# dimension marks on the left of the track
def dim(x, y0, y1, label, colour, sub=None):
    add(f'<line x1="{x}" x2="{x}" y1="{y0:.1f}" y2="{y1:.1f}" stroke="{colour}" stroke-width="1.5"/>')
    for y in (y0, y1):
        add(f'<line x1="{x - 6}" x2="{x + 6}" y1="{y:.1f}" y2="{y:.1f}" stroke="{colour}" stroke-width="1.5"/>')
    text(x - 12, (y0 + y1) / 2 + 2, label, 16, colour, "end", "bold")
    if sub:
        text(x - 12, (y0 + y1) / 2 + 22, sub, 15, MUTED, "end")


dim(x_mid - 22, y_react, y_start, "v·Δt", INK, "32 m")
dim(x_mid - 22, y_stop, y_react, "v²/2a", RED, "80 m")
text(x_mid + 16, y_stop + 6, "brake stops 12 m past the margin", 16, RED, weight="bold")
text(RX1 + 10, cyy - R * S + 30, "turn: parallel to the edge,", 16, TEAL, "end", "bold")
text(RX1 + 10, cyy - R * S + 50, "18 m short of the margin", 16, TEAL, "end", "bold")

# takeaway box
bx, by = RX0 - 10, 640
add(f'<rect x="{bx}" y="{by}" width="{RX1 - RX0 + 30}" height="200" rx="10" fill="#F4F6F8"/>')
text(bx + 20, by + 36, "Brake: speed falls, heading stays.", 18, GREY, weight="bold")
text(bx + 20, by + 62, "Needs v·Δt + v²/2a.", 17, INK)
text(bx + 20, by + 100, "Turn: speed stays, heading swings.", 18, TEAL, weight="bold")
text(bx + 20, by + 126, "Still drifts in v·Δt + R before it", 17, INK)
text(bx + 20, by + 150, "runs parallel. v_c → 0, not distance → 0.", 17, INK)
text(bx + 20, by + 182, "Pick whichever fits in the gap.", 17, MUTED, italic=True)

add("</g>")
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
       + "".join(out) + "</svg>")
dst = pathlib.Path(__file__).resolve().parents[1] / "assets" / "brake_turn_field.svg"
dst.write_text(svg)
print("wrote", dst)
