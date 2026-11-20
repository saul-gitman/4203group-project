"""
brake_turn_cases_svg.py - two simple top-down pictures: when to brake, when to turn.

The aircraft flies up (bottom -> top) towards the zone and turns right.
Same scale in both. Numbers from params.py (a = 2.5 m/s^2, dt = 1.6 s, R = 50 m)
and a keep-out margin of about 18 m (R_DRONE 3 m + k sigma_h ~ 15 m).

    BRAKE case: 10 m/s, 36 m from the margin. Braking fits (16 + 20 = 36 m);
                a turn would need 16 + 50 = 66 m and cut 30 m past the margin.
    TURN case:  20 m/s, 100 m from the margin. Braking needs 32 + 80 = 112 m
                (12 m past the margin); a turn needs 32 + 50 = 82 m (18 m short).

    python brake_turn_cases_svg.py   -> ../assets/case_brake.svg, ../assets/case_turn.svg
"""

import pathlib

A, DT, R, MARGIN = 2.5, 1.6, 50.0, 18.0
INK, MUTED = "#1F2933", "#5A6573"
GREY, TEAL, BLUE, RED = "#5F6B7A", "#0B7880", "#2A64AD", "#B33327"
FONT = "Arial, Helvetica, sans-serif"

W, H = 640, 780
S = 4.0                      # px per metre
Y_ZONE = 150                 # zone edge (px)
Y_M = Y_ZONE + MARGIN * S    # margin line (px)
X0 = 170                     # straight track


def build(kind, v, gap):
    o = []
    add = o.append

    def text(x, y, s, size=20, fill=INK, anchor="start", weight="normal"):
        add(f'<text x="{x:.0f}" y="{y:.0f}" font-size="{size}" fill="{fill}" '
            f'text-anchor="{anchor}" font-weight="{weight}">{s}</text>')

    react = v * DT
    brake = v * v / (2 * A)
    y0 = Y_M + gap * S                     # start
    yr = y0 - react * S                    # end of reaction leg
    y_stop = yr - brake * S                # where braking ends
    y_turn = yr - R * S                    # where the turn runs parallel
    brake_ok = react + brake <= gap
    turn_ok = react + R <= gap

    add(f'<rect width="{W}" height="{H}" fill="#FFFFFF"/>')
    # zone + margin
    add(f'<rect x="0" y="80" width="{W}" height="{Y_ZONE - 80}" fill="{BLUE}" fill-opacity="0.18"/>')
    add(f'<line x1="0" x2="{W}" y1="{Y_ZONE}" y2="{Y_ZONE}" stroke="{BLUE}" stroke-width="3"/>')
    add(f'<rect x="0" y="{Y_ZONE}" width="{W}" height="{Y_M - Y_ZONE}" fill="{BLUE}" fill-opacity="0.06"/>')
    add(f'<line x1="0" x2="{W}" y1="{Y_M}" y2="{Y_M}" stroke="{BLUE}" stroke-width="2" stroke-dasharray="8 6"/>')
    text(24, 112, "no-entry zone", 20, BLUE, weight="bold")
    text(W - 16, Y_M - 10, "margin", 18, BLUE, "end")

    # reaction leg (both)
    add(f'<line x1="{X0}" x2="{X0}" y1="{y0}" y2="{yr}" stroke="{INK}" stroke-width="4" '
        f'stroke-dasharray="2 8" stroke-linecap="round"/>')
    text(X0 - 16, (y0 + yr) / 2 + 7, f"reaction {react:.0f} m", 17, MUTED, "end")

    def style(ok, colour):
        return (f'stroke="{colour}" stroke-width="5"' if ok
                else f'stroke="{RED}" stroke-width="3" stroke-dasharray="10 7"')

    # brake path: straight on
    add(f'<line x1="{X0}" x2="{X0}" y1="{yr}" y2="{y_stop}" {style(brake_ok, GREY)}/>')
    add(f'<rect x="{X0 - 14}" y="{y_stop - 4}" width="28" height="8" rx="2" fill="{GREY if brake_ok else RED}"/>')
    # turn path: quarter circle to the right, then along the edge
    xe = X0 + R * S
    add(f'<path d="M{X0},{yr} A{R * S},{R * S} 0 0 1 {xe},{y_turn} L{W - 40},{y_turn}" fill="none" '
        f'{style(turn_ok, TEAL)}/>')
    tip = TEAL if turn_ok else RED
    add(f'<polygon points="{W - 26},{y_turn} {W - 42},{y_turn - 9} {W - 42},{y_turn + 9}" fill="{tip}"/>')

    # labels on the two endings
    past_b, past_t = react + brake - gap, react + R - gap
    lb = (f"brake: stops {-past_b:.0f} m short ✓" if brake_ok and past_b < -0.5 else
          "brake: stops at the margin ✓" if brake_ok else f"brake: {past_b:.0f} m past ✗")
    lt = (f"turn: {-past_t:.0f} m short ✓" if turn_ok else f"turn: {past_t:.0f} m past ✗")
    text(X0 + 22, y_stop + (32 if brake_ok else 7), lb, 19, GREY if brake_ok else RED, weight="bold")
    text(W - 40, y_turn + 34, lt, 19, TEAL if turn_ok else RED, "end", "bold")

    # aircraft
    add(f'<circle cx="{X0}" cy="{y0}" r="13" fill="{INK}"/>')
    add(f'<polygon points="{X0},{y0 - 34} {X0 - 9},{y0 - 18} {X0 + 9},{y0 - 18}" fill="{INK}"/>')
    text(X0 + 24, y0 + 7, f"{v:.0f} m/s, {gap:.0f} m from the margin", 19, INK)

    # title + one-line reason
    if kind == "brake":
        title, colour = "BRAKE", GREY
        why = f"Stopping needs {react + brake:.0f} m and fits; a turn needs {react + R:.0f} m."
    else:
        title, colour = "TURN", TEAL
        why = f"Stopping needs {react + brake:.0f} m, too much; a turn needs {react + R:.0f} m."
    text(24, 50, title, 34, colour, weight="bold")
    text(24 + len(title) * 25 + 14, 50, "slow enough to stop" if kind == "brake" else "too fast to stop, room to turn",
         21, MUTED)
    text(24, H - 28, why, 19, INK)

    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
           f'font-family="{FONT}">' + "".join(o) + "</svg>")
    dst = pathlib.Path(__file__).resolve().parents[1] / "assets" / f"case_{kind}.svg"
    dst.write_text(svg)
    print("wrote", dst)


build("brake", 10.0, 10.0 * DT + 100 / (2 * A))    # 36 m: exactly where braking starts
build("turn", 20.0, 100.0)
