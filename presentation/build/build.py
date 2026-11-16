"""Build the AAE4203 group deck inside the professor's template.

python presentation/build/build.py presentation/template/AAE4203_Group_Presentation_Student_Template_v2.pptx presentation/Gxx_Txx_AAE4203.pptx
"""
import copy
import sys

from lxml import etree
from pptx import Presentation
from pptx.chart.data import CategoryChartData, XyChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION, XL_LEGEND_POSITION, XL_TICK_LABEL_POSITION
from pptx.enum.dml import MSO_LINE
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt

import pathlib
A = str(pathlib.Path(__file__).resolve().parents[1] / "assets") + "/"
BLUE, BLUE_T, NAVY = "2A64AD", "E8EFF8", "1B3F70"
PURP, PURP_T = "7A3FA6", "F2EAF8"
GREY, GREY_T = "5F6B7A", "EEF0F3"
INK, MUTED, LIGHT, GOLD, RED, LINE = "1F2933", "5A6573", "F4F6F8", "C8860A", "B33327", "C3CCD6"
FONT = "Arial"


def rgb(h):
    return RGBColor.from_string(h)


# ------------------------------------------------------------------ text
def R(text, **o):
    return (text, o)


def P(*runs, **o):
    return {"runs": [r if isinstance(r, tuple) else (r, {}) for r in runs], **o}


def fill_tf(tf, paras, size=18, color=INK, bold=False, align=PP_ALIGN.LEFT, spacing=None):
    tf.word_wrap = True
    first = True
    for para in paras:
        if isinstance(para, str):
            para = P(para)
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.alignment = para.get("align", align)
        if para.get("after") is not None:
            p.space_after = Pt(para["after"])
        if para.get("before") is not None:
            p.space_before = Pt(para["before"])
        if spacing or para.get("spacing"):
            p.line_spacing = para.get("spacing", spacing)
        for text, o in para["runs"]:
            r = p.add_run()
            r.text = text
            f = r.font
            f.name = o.get("font", FONT)
            f.size = Pt(o.get("size", para.get("size", size)))
            f.bold = o.get("bold", para.get("bold", bold))
            f.italic = o.get("italic", False)
            f.color.rgb = rgb(o.get("color", para.get("color", color)))


def txt(slide, x, y, w, h, paras, size=18, color=INK, bold=False, align=PP_ALIGN.LEFT,
        anchor=MSO_ANCHOR.TOP, margin=0.0, name=None, spacing=None):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.auto_size = None
    for side in ("left", "right", "top", "bottom"):
        setattr(tf, f"margin_{side}", Inches(margin))
    tf.vertical_anchor = anchor
    fill_tf(tf, paras, size, color, bold, align, spacing)
    if name:
        set_name(tb, name)
    return tb


def set_name(shape, name):
    shape._element.xpath("./*[1]/p:cNvPr")[0].set("name", name)


def set_alpha(shape, opacity):
    sf = shape.fill._xPr.find(qn("a:solidFill"))
    a = etree.SubElement(sf[0], qn("a:alpha"))
    a.set("val", str(int(opacity * 1000)))


def box(slide, x, y, w, h, fill=None, line=None, lw=1.0, radius=None, dash=False, opacity=None,
        shape=None, name=None, paras=None, size=18, color=INK, bold=False, align=PP_ALIGN.LEFT,
        anchor=MSO_ANCHOR.MIDDLE, margin=0.12):
    kind = shape or (MSO_SHAPE.ROUNDED_RECTANGLE if radius is not None else MSO_SHAPE.RECTANGLE)
    s = slide.shapes.add_shape(kind, Inches(x), Inches(y), Inches(w), Inches(h))
    if radius is not None and kind == MSO_SHAPE.ROUNDED_RECTANGLE:
        s.adjustments[0] = radius
    if fill:
        s.fill.solid()
        s.fill.fore_color.rgb = rgb(fill)
        if opacity is not None:
            set_alpha(s, opacity)
    else:
        s.fill.background()
    if line:
        s.line.color.rgb = rgb(line)
        s.line.width = Pt(lw)
        if dash:
            s.line.dash_style = MSO_LINE.DASH
    else:
        s.line.fill.background()
    s.shadow.inherit = False
    tf = s.text_frame
    for side in ("left", "right", "top", "bottom"):
        setattr(tf, f"margin_{side}", Inches(margin))
    tf.vertical_anchor = anchor
    if paras:
        fill_tf(tf, paras, size, color, bold, align)
    if name:
        set_name(s, name)
    return s


def arrow_shape(slide, x, y, w, h, kind=MSO_SHAPE.RIGHT_ARROW, fill=GREY):
    return box(slide, x, y, w, h, fill=fill, shape=kind)


def line(slide, x1, y1, x2, y2, color=GREY, width=1.5, dash=False):
    c = slide.shapes.add_connector(1, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    c.line.color.rgb = rgb(color)
    c.line.width = Pt(width)
    if dash:
        c.line.dash_style = MSO_LINE.DASH
    return c


def pic(slide, path, x, y, w=None, h=None, name=None):
    p = slide.shapes.add_picture(path, Inches(x), Inches(y), Inches(w) if w else None, Inches(h) if h else None)
    if name:
        set_name(p, name)
    return p


def headline(slide, text):
    return txt(slide, 0.35, 0.9, 9.3, 0.5, [text], size=20, bold=True, name="headline")


def source(slide, text):
    return txt(slide, 0.35, 5.03, 6.55, 0.3, [text], size=9, color=MUTED)


def notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text


# ------------------------------------------------------------------ slide plumbing
def drop(shape):
    el = shape._element
    el.getparent().remove(el)


def is_tag(shape):
    return shape.has_text_frame and shape.text_frame.text.startswith("Presenter:")


def clear_content(slide):
    for sh in list(slide.shapes):
        if sh.is_placeholder and sh.placeholder_format.type == 1:  # title
            continue
        if is_tag(sh):
            continue
        drop(sh)


def set_title(slide, text):
    t = slide.shapes.title
    runs = t.text_frame.paragraphs[0].runs
    if runs:
        runs[0].text = text
        for r in runs[1:]:
            r.text = ""
    else:
        t.text_frame.text = text


def set_tag(slide, member, tag_xml):
    tags = [s for s in slide.shapes if is_tag(s)]
    if not tags:
        slide.shapes._spTree.append(copy.deepcopy(tag_xml))
        tags = [s for s in slide.shapes if is_tag(s)]
    tags[0].text_frame.paragraphs[0].runs[0].text = f"Presenter: Member {member}"


def set_runs(shape, texts):
    """Replace run text paragraph by paragraph, keeping the template's formatting."""
    for p, t in zip(shape.text_frame.paragraphs, texts):
        if t is None:
            continue
        p.runs[0].text = t
        for r in p.runs[1:]:
            r.text = ""


P_NS = "http://schemas.openxmlformats.org/presentationml/2006/main"
MORPH = (
    '<mc:AlternateContent xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006">'
    '<mc:Choice xmlns:p159="http://schemas.microsoft.com/office/powerpoint/2015/09/main" Requires="p159">'
    f'<p:transition xmlns:p="{P_NS}" xmlns:p14="http://schemas.microsoft.com/office/powerpoint/2010/main" '
    'spd="slow" p14:dur="1200"><p159:morph option="byObject"/></p:transition></mc:Choice>'
    f'<mc:Fallback><p:transition xmlns:p="{P_NS}" spd="slow"><p:fade/></p:transition></mc:Fallback>'
    "</mc:AlternateContent>")


def add_morph(slide):
    sld = slide._element
    sld.find(qn("p:clrMapOvr")).addnext(etree.fromstring(MORPH))


# ------------------------------------------------------------------ slides
def cover(s):
    sh = {x.name: x for x in s.shapes}
    set_runs(sh["Rectangle 2"], ["Staying inside the line:", "a GNSS + radar guardrail"])
    parts = ["Background and motivation", "Technical principle, link to AAE4203",
             "Case study, demo, results", "Limitations, trends, conclusion"]
    for n, part in zip((15, 17, 19, 21), parts):
        r = sh[f"Rectangle {n}"]
        p = r.text_frame.paragraphs[1]
        p.runs[0].text = p.runs[0].text.replace("Part presented", part)
    notes(s, "Cover. Fill in group number, topic number, slot, names and student numbers before submitting.\n"
             "Opening line (Member 1): 'Hong Kong now lets drones and eVTOLs fly trials over the city. "
             "The rule is simple: stay inside the box. Our project is about how an aircraft knows it is inside the box.'")


def team(s):
    tbl = [x for x in s.shapes if x.has_table][0].table
    rows = [("Background and motivation", "4–7", "3.5 min"),
            ("Technical principle and link to AAE4203", "8–16", "4 min"),
            ("Case study, demo and results", "17–19", "4 min"),
            ("Limitations, future trends, conclusion", "20–22", "3.5 min")]
    for i, (part, sl, t) in enumerate(rows, start=1):
        for j, val in ((2, part), (3, sl), (4, t)):
            tf = tbl.cell(i, j).text_frame
            tf.paragraphs[0].runs[0].text = val
    notes(s, "Talk times add up to 15 minutes; 3 minutes of Q&A after. Slides 10–14 are the flowchart zoom: they go fast.")


def outline(s):
    clear_content(s)
    headline(s, "Why it matters, how it works, whether it works, what comes next")
    steps = [("1", "Why", "Background and motivation", "Hong Kong's new drone law, a real eVTOL, Singapore", "Member 1 · 4–7"),
             ("2", "How", "Technical principle", "Two navigation flows, one decision, link to AAE4203", "Member 2 · 8–16"),
             ("3", "Proof", "Case study and results", "Three bad GNSS days, our demo, a baseline", "Member 3 · 17–19"),
             ("4", "Next", "Limits and trends", "Where it breaks, where the field is going", "Member 4 · 20–22")]
    x, w, gap = 0.35, 2.175, 0.2
    for i, (n, word, part, what, who) in enumerate(steps):
        cx = x + i * (w + gap)
        box(s, cx, 1.6, w, 3.25, fill=LIGHT, radius=0.06)
        txt(s, cx + 0.2, 1.75, w - 0.4, 0.75, [P(R(n, size=40, bold=True, color=BLUE))])
        txt(s, cx + 0.2, 2.5, w - 0.4, 0.45, [P(R(word, size=24, bold=True, color=INK))])
        txt(s, cx + 0.2, 2.98, w - 0.4, 0.6, [P(R(part, size=16, bold=True, color=INK))])
        txt(s, cx + 0.2, 3.55, w - 0.4, 0.85, [P(R(what, size=14, color=MUTED))])
        txt(s, cx + 0.2, 4.45, w - 0.4, 0.3, [P(R(who, size=12, bold=True, color=GOLD))])
        if i < 3:
            arrow_shape(s, cx + w + 0.03, 3.05, 0.14, 0.3, fill=LINE)
    notes(s, "Keep this under 20 seconds. Each part answers one question: why, how, does it work, what next.")


def background(s):
    clear_content(s)
    headline(s, "Since July 2025, Hong Kong's law has a slot for every size of drone")
    txt(s, 0.35, 1.45, 4, 0.3, [P(R("Aircraft weight  →", size=12, bold=True, color=MUTED))])
    segs = [(0.35, 2.55, "D6E2F2", INK, "≤ 25 kg", "Cat A/B · Cap. 448G", "in force since 1 Dec 2022"),
            (2.95, 3.0, BLUE, "FFFFFF", "25–150 kg", "Cat C · Cap. 448G", "CAD permission · from 18 Jul 2025"),
            (6.0, 3.65, NAVY, "FFFFFF", "> 150 kg", "Trials of unconventional aircraft", "Cap. 448C Part IXA · CE's power, used by DGCA")]
    for x, w, f, c, big, mid, small in segs:
        box(s, x, 1.75, w - 0.05, 1.15, fill=f, anchor=MSO_ANCHOR.MIDDLE, margin=0.15,
            paras=[P(R(big, size=22, bold=True, color=c)), P(R(mid, size=14, bold=True, color=c)),
                   P(R(small, size=12, color=c))])
    box(s, 7.85, 2.98, 1.75, 0.34, fill=GOLD, radius=0.3, anchor=MSO_ANCHOR.MIDDLE, margin=0.04,
        paras=[P(R("EH216-S lives here", size=12, bold=True, color="FFFFFF"), align=PP_ALIGN.CENTER)])
    # timeline
    ty = 3.78
    line(s, 0.6, ty, 9.4, ty, color=LINE, width=2)
    ms = [("Dec 2022", "SUA Order fully in force"),
          ("Mar 2025", "Sandbox: 38 projects picked from 72"),
          ("Jul 2025", "Both amendment orders in force"),
          ("Nov 2025", "Sandbox X: cross-boundary and passenger aircraft"),
          ("Aug 2026", "EH216-S flies in public at Cyberport")]
    xs = [0.35 + i * 1.88 for i in range(5)]
    for i, (x, (d, t)) in enumerate(zip(xs, ms)):
        last = i == 4
        dot = box(s, x + 0.82, ty - 0.09, 0.18, 0.18, fill=GOLD if last else BLUE, shape=MSO_SHAPE.OVAL)
        txt(s, x, ty - 0.42, 1.82, 0.3, [P(R(d, size=14, bold=True, color=GOLD if last else BLUE), align=PP_ALIGN.CENTER)])
        txt(s, x, ty + 0.17, 1.82, 0.9, [P(R(t, size=13, color=INK), align=PP_ALIGN.CENTER)])
    source(s, "Sources: HKSAR Gov press release, 17 Jul 2025; CAD AIC 20/25; CAD AC-013; TLB Regulatory Sandbox page; news.gov.hk, 24 Nov 2025; avi-go, 28 Aug 2026.")
    notes(s, "Say: Until 2025 Hong Kong's drone law stopped at 25 kg. Since 18 July 2025 there is a slot for every size. "
             "25 to 150 kg is Category C under Cap. 448G and needs CAD permission. Above 150 kg, like a passenger eVTOL, "
             "is a trial of an 'unconventional aircraft' under Cap. 448C. The power belongs to the Chief Executive and the DGCA uses it.\n"
             "Timeline: the first Sandbox picked 38 projects from 72 applications; Sandbox X in November 2025 opened cross-boundary "
             "and passenger aircraft; in August 2026 the EH216-S flew in public at Cyberport. (~50 s)")


def ehang(s):
    clear_content(s)
    headline(s, "A fully certified aircraft still needs a Hong Kong box to fly in")
    box(s, 0.35, 1.5, 4.55, 3.4, fill=GREY_T, line=LINE, lw=1.25, dash=True, radius=0.04, align=PP_ALIGN.CENTER,
        paras=[P(R("[ your EH216-S photo from Cyberport ]", size=16, bold=True, color=MUTED), align=PP_ALIGN.CENTER),
               P(R("drop it here and delete this box", size=12, color=MUTED), align=PP_ALIGN.CENTER)],
        name="photo-placeholder")
    txt(s, 5.15, 1.5, 4.5, 0.3, [P(R("Certificates from CAAC (mainland China)", size=13, bold=True, color=MUTED))])
    certs = [("TC", "Oct 2023", "type design approved"), ("AC", "Dec 2023", "standard airworthiness"),
             ("PC", "Apr 2024", "production approved"), ("AOC", "2025", "operators approved")]
    for i, (c, d, what) in enumerate(certs):
        cx, cy = 5.15 + (i % 2) * 2.3, 1.85 + (i // 2) * 1.12
        box(s, cx, cy, 2.15, 1.0, fill="FFFFFF", line=BLUE, lw=2, radius=0.12, margin=0.12,
            anchor=MSO_ANCHOR.MIDDLE,
            paras=[P(R(c, size=24, bold=True, color=BLUE), R("   " + d, size=13, bold=True, color=INK)),
                   P(R(what, size=13, color=MUTED))])
    txt(s, 5.15, 4.12, 4.5, 0.8,
        [P(R("In Hong Kong it still needs a permission, and an ", size=16),
           R("operating area it must never leave", size=16, bold=True, color=BLUE), R(" (AIC 20/25 ¶5.3).", size=16))])
    source(s, "Sources: AAM International (TC); Asian Aviation (AC); CompositesWorld (PC); Business Aviation (AOC); avi-go (Cyberport flight, 28 Aug 2026); CAD AIC 20/25.")
    notes(s, "Say: This is the EH216-S at Cyberport (our own photo, taken during the internship). It holds the full set of "
             "mainland certificates: type certificate, airworthiness certificate, production certificate, and its operators hold AOCs. "
             "None of that lets it fly in Hong Kong. Here it needs a trial permission, and the permission says: stay inside the area we accepted. "
             "That sentence is our whole project. (~45 s)")


def aic(s):
    clear_content(s)
    headline(s, "The permission rule is secretly a navigation spec")
    box(s, 0.35, 1.5, 9.3, 1.95, fill=LIGHT, radius=0.05, margin=0.25, anchor=MSO_ANCHOR.MIDDLE,
        paras=[P(R("AIC 20/25 ¶5.3–5.4, paraphrased", size=13, bold=True, color=MUTED), after=6),
               P(R("The aircraft must stay inside the accepted operating area ", size=21),
                 R("at all times", size=21, bold=True), R(". Route planning must account for ", size=21),
                 R("navigation accuracy", size=21, bold=True, color=BLUE), R(", ", size=21),
                 R("detect-and-avoid capability", size=21, bold=True, color=PURP), R(" and ", size=21),
                 R("communication latency", size=21, bold=True, color=GREY), R(".", size=21))])
    chips = [(BLUE, "Navigation accuracy", "Flow 1: GNSS + IMU, and how wrong it is (σ_h)"),
             (PURP, "Detect and avoid", "Flow 2: radar ranges to buildings"),
             (GREY, "Latency", "Δt = 1.6 s, flown before any decision acts")]
    for i, (c, a, b) in enumerate(chips):
        cx = 0.35 + i * 3.15
        box(s, cx, 3.62, 3.0, 1.0, fill=c, radius=0.1, margin=0.15, anchor=MSO_ANCHOR.MIDDLE,
            paras=[P(R(a, size=18, bold=True, color="FFFFFF")), P(R(b, size=14, color="FFFFFF"))])
    txt(s, 0.35, 4.67, 9.3, 0.32, [P(R("¶5.5 adds: GNSS signal integrity must be adequate across the area; avoid dense high-rise districts.",
                                      size=13, italic=True, color=MUTED))])
    source(s, "Source: Civil Aviation Department, AIC 20/25, Permission to conduct trial operations of unconventional aircraft in Hong Kong, ¶4.4, ¶5.3–5.5, ¶11.1.")
    notes(s, "Say: Read the rule closely. It asks for three things: navigation accuracy, detect and avoid, latency. "
             "Those are our three colours for the rest of the talk: blue, purple, grey. "
             "A geofence is only as good as the position you check it against. Hand over to Member 2 after the next slide. (~45 s)")


def singapore(s):
    clear_content(s)
    set_title(s, "State of the Art: Hong Kong vs Singapore")
    headline(s, "Singapore has the same problem, with even less room")
    rows = [("", "Hong Kong", "Singapore"),
            ("Rules", "Cap. 448G up to 150 kg; Cap. 448C trials above", "ANR-101: permits by mass, height and place"),
            ("Geofence written as", "No-fly zones on CAD's eSUA map", "5 km from any aerodrome or airbase; 200 ft AMSL"),
            ("Next step", "Sandbox X: cross-boundary routes, passenger eVTOL", "National UTM system (Thales picked, May 2026)"),
            ("A bad day", "Oct 2018: GPS jamming drops 46 show drones into the harbour", "Jun 2019: drones close a Changi runway on and off; ~37 flights delayed")]
    gf = s.shapes.add_table(len(rows), 3, Inches(0.35), Inches(1.5), Inches(9.3), Inches(3.35))
    tbl = gf.table
    tbl.columns[0].width = Inches(1.9)
    tbl.columns[1].width = Inches(3.7)
    tbl.columns[2].width = Inches(3.7)
    tbl.first_row = True
    tbl.horz_banding = False
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            c = tbl.cell(i, j)
            c.fill.solid()
            c.fill.fore_color.rgb = rgb(INK if i == 0 else ("FFFFFF" if j else LIGHT))
            if i == 4 and j:
                c.fill.fore_color.rgb = rgb("FBEDEB")
            c.margin_left = c.margin_right = Inches(0.1)
            c.vertical_anchor = MSO_ANCHOR.MIDDLE
            tf = c.text_frame
            tf.text = ""
            fill_tf(tf, [P(R(val, size=15 if i else 16, bold=(i == 0 or j == 0),
                             color="FFFFFF" if i == 0 else INK))])
    source(s, "Sources: CAAS, Operator and activity permits; CAAS media response, 19 Jun 2019; Asian Aviation, 27 May 2026; SCMP, Oct 2018; TLB Sandbox page.")
    notes(s, "Say: Why Singapore? Same density, a mega-hub airport next to the city, and its drone rules are literally geofences "
             "written as numbers: 5 km from any aerodrome, 200 ft. In June 2019 drones near Changi suspended a runway on and off overnight; "
             "about 37 flights were delayed. Both cities are now building traffic-management systems. "
             "If asked: Singapore's first air-taxi plan (Volocopter, 2024) stalled when the company went insolvent in Dec 2024. (~50 s)")


def principle1(s):
    clear_content(s)
    set_title(s, "Technical Principle (1): How It Works")
    headline(s, "A zone exists only on a map; a building can be measured")
    # left: zone
    box(s, 0.35, 1.5, 4.5, 2.92, fill=BLUE_T, radius=0.04)
    txt(s, 0.55, 1.6, 4.1, 0.35, [P(R("No-entry zone  ·  Flow 1", size=18, bold=True, color=BLUE))])
    box(s, 2.75, 2.02, 1.8, 1.18, fill="FFFFFF", line=BLUE, lw=2, shape=MSO_SHAPE.HEXAGON,
        paras=[P(R("eSUA zone", size=13, bold=True, color=BLUE), align=PP_ALIGN.CENTER)], align=PP_ALIGN.CENTER)
    box(s, 0.95, 2.0, 1.22, 1.22, fill=BLUE, opacity=18, line=BLUE, lw=1, dash=True, shape=MSO_SHAPE.OVAL)
    box(s, 1.49, 2.54, 0.14, 0.14, fill=INK, shape=MSO_SHAPE.OVAL)
    txt(s, 0.55, 3.24, 2.0, 0.25, [P(R("we're in here somewhere", size=11, italic=True, color=BLUE), align=PP_ALIGN.CENTER)])
    txt(s, 0.55, 3.52, 4.1, 0.85, [P(R("Distance = our GNSS position vs the map, so GNSS error matters.", size=14)),
                                    P(R("Margin R + k·σ_h ≈ 19–26 m", size=14, bold=True, color=BLUE))])
    # right: building
    box(s, 5.15, 1.5, 4.5, 2.92, fill=PURP_T, radius=0.04)
    txt(s, 5.35, 1.6, 4.1, 0.35, [P(R("Building  ·  Flow 2", size=18, bold=True, color=PURP))])
    box(s, 5.75, 2.15, 0.95, 0.95, fill=PURP, opacity=10, line=PURP, lw=1, dash=True, shape=MSO_SHAPE.OVAL)
    box(s, 6.155, 2.555, 0.14, 0.14, fill=INK, shape=MSO_SHAPE.OVAL)
    a = line(s, 6.31, 2.625, 7.78, 2.625, color=INK, width=2)
    a.line._get_or_add_ln().append(etree.fromstring('<a:tailEnd xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" type="triangle"/>'))
    txt(s, 6.7, 2.3, 0.8, 0.3, [P(R("d", size=16, bold=True, italic=True), align=PP_ALIGN.CENTER)])
    box(s, 7.85, 2.0, 1.15, 1.25, fill="FFFFFF", line=PURP, lw=2,
        paras=[P(R("tower", size=13, bold=True, color=PURP), align=PP_ALIGN.CENTER)], align=PP_ALIGN.CENTER)
    txt(s, 5.35, 3.52, 4.1, 0.85, [P(R("Distance = radar range, measured directly. GNSS error never enters.", size=14)),
                                    P(R("Margin R + k·σ_range ≈ 4.5 m", size=14, bold=True, color=PURP))])
    box(s, 0.35, 4.52, 9.3, 0.42, fill=GREY_T, radius=0.2, margin=0.15,
        paras=[P(R("Shared: ", size=14, bold=True, color=GREY),
                 R("velocity from Flow 1 serves both, because speed sets the braking and turning distance.", size=14))])
    source(s, "Own design. R = 3 m aircraft radius, k = 3.03, σ_h ≈ 5–8 m (HDOP × σ_UERE), σ_range = 0.5 m.")
    notes(s, "Say (Member 2): The one idea of our project. A no-entry zone exists only on a map. To know how far we are from it, "
             "we compare our GNSS position with the map, so our GNSS error matters: the margin grows with sigma_h, about 19 to 26 m. "
             "A building is different: the radar measures the distance itself, so GNSS error never enters, and the margin is about 4.5 m. "
             "Velocity comes from GNSS and IMU and is used for both. (~40 s)")


HUB = {
    "blue": (BLUE, "FLOW 1 · GNSS + IMU", "Where am I, and how sure?", "GNSS fix, Doppler and IMU give position, velocity and error σ_h, compared with the eSUA zone map."),
    "grey": (GREY, "DECISION", "What do I do now?", "Can I still brake in time? → CLEAR · BRAKE · TURN · RETURN"),
    "purple": (PURP, "FLOW 2 · RADAR", "What is right next to me?", "Radar range and bearing, rotated into NED. No GNSS needed."),
}


def hub(s, nxt=None, seen=()):
    clear_content(s)
    set_title(s, "Technical Principle (2): Key Algorithm")
    headline(s, "One second of the loop: blue and purple only meet at grey")
    xs = {"blue": 0.35, "grey": 3.575, "purple": 6.8}
    for key, x in xs.items():
        col, lab, q, body = HUB[key]
        pic(s, A + f"flow_{key}_blur.png", x, 1.5, 2.85, 3.4, name=f"!!{key}")
        dim = key in seen
        panel = box(s, x, 1.5, 2.85, 3.4, fill=col, opacity=55 if dim else 80, name=f"panel-{key}",
                    line="FFFFFF" if key == nxt else None, lw=4)
        txt(s, x + 0.2, 1.68, 2.45, 0.3, [P(R(lab + ("   ✓" if dim else ""), size=12, bold=True, color="FFFFFF"))],
            name=f"label-{key}")
        txt(s, x + 0.2, 2.02, 2.45, 0.9, [P(R(q, size=21, bold=True, color="FFFFFF"))], name=f"q-{key}")
        txt(s, x + 0.2, 3.0, 2.45, 1.4, [P(R(body, size=16, color="FFFFFF"))], name=f"body-{key}")
        if key == nxt:
            box(s, x + 0.2, 4.45, 1.45, 0.3, fill="FFFFFF", radius=0.4, margin=0.04, name="next-pill",
                paras=[P(R("click to zoom ▸", size=11, bold=True, color=col), align=PP_ALIGN.CENTER)])
    arrow_shape(s, 3.235, 3.05, 0.3, 0.32, kind=MSO_SHAPE.RIGHT_ARROW, fill=LINE).name
    arrow_shape(s, 6.46, 3.05, 0.3, 0.32, kind=MSO_SHAPE.LEFT_ARROW, fill=LINE)
    source(s, "Own design, from the repo's main.py, location.py and boundary.py.")


def zoom(s, key, head):
    clear_content(s)
    set_title(s, "Technical Principle (2): Key Algorithm")
    headline(s, head)
    pic(s, A + f"flow_{key}.png", 0.3, 1.45, 9.4, 3.5, name=f"!!{key}")
    source(s, "Own design. Dashed boxes are inputs; thick boxes are what each flow hands to the decision.")


def speed(s, chart_xy):
    clear_content(s)
    set_title(s, "Technical Principle (2): Key Equations")
    headline(s, "Speed sets the distance: brake below 15.8 m/s, turn above it")
    xy = XyChartData()
    b = xy.add_series("Brake to a stop")
    t = xy.add_series("Turn away (head-on)")
    for v in range(0, 26):
        b.add_data_point(v, 1.6 * v + v * v / 5.0)
        t.add_data_point(v, 1.6 * v + 50.0)
    c = xy.add_series("15.8 m/s")
    c.add_data_point(15.81, 0)
    c.add_data_point(15.81, 170)
    gf = s.shapes.add_chart(XL_CHART_TYPE.XY_SCATTER_LINES_NO_MARKERS, Inches(0.3), Inches(1.45), Inches(5.7), Inches(3.5), xy)
    ch = gf.chart
    ch.font.name = FONT
    ch.font.size = Pt(12)
    ch.has_legend = True
    ch.legend.position = XL_LEGEND_POSITION.TOP
    ch.legend.include_in_layout = False
    ch.legend.font.size = Pt(13)
    for ser, colr, w, dash in zip(ch.plots[0].series, (GREY, "0B7880", MUTED), (3, 3, 1.5), (False, False, True)):
        ser.format.line.color.rgb = rgb(colr)
        ser.format.line.width = Pt(w)
        if dash:
            ser.format.line.dash_style = MSO_LINE.DASH
        ser.smooth = False
    xa, ya = ch.category_axis, ch.value_axis
    xa.minimum_scale, xa.maximum_scale, xa.major_unit = 0, 25, 5
    ya.minimum_scale, ya.maximum_scale, ya.major_unit = 0, 170, 40
    for ax, title in ((xa, "Closing speed v_c (m/s)"), (ya, "Distance needed (m)")):
        ax.has_title = True
        ax.axis_title.text_frame.text = title
        ax.axis_title.text_frame.paragraphs[0].runs[0].font.size = Pt(12)
        ax.axis_title.text_frame.paragraphs[0].runs[0].font.bold = False
        ax.tick_labels.font.size = Pt(12)
        ax.format.line.color.rgb = rgb(LINE)
    ya.has_major_gridlines = True
    ya.major_gridlines.format.line.color.rgb = rgb("E3E7EC")
    xa.has_major_gridlines = False
    # equations card
    box(s, 6.2, 1.5, 3.45, 3.4, fill=LIGHT, radius=0.05, margin=0.2, anchor=MSO_ANCHOR.TOP,
        paras=[P(R("Brake", size=14, bold=True, color=GREY), after=0),
               P(R("d = v·Δt + v² / 2a", size=19, bold=True), after=8),
               P(R("Turn (head-on, α = 0)", size=14, bold=True, color="0B7880"), after=0),
               P(R("d = v·Δt + R", size=19, bold=True), after=8),
               P(R("Equal when v² / 2a = R:", size=14, color=MUTED), after=0),
               P(R("v = √(2aR) = 15.8 m/s", size=17, bold=True), after=8),
               P(R("At 10 m/s, 16 m of the 36 m is just reaction time (Δt = 1.6 s).", size=13, color=MUTED))])
    source(s, "Own calculation from params.py: Δt = 1.6 s (1 s epoch + 0.1 s compute + 0.5 s actuation), a = 2.5 m/s², R = 50 m.")
    notes(s, "Say: Why does speed decide between braking and turning? Braking distance grows with v squared; turning distance is "
             "fixed by the turn radius. They cross where v^2/2a = R, so v = sqrt(2aR) = 15.8 m/s. Below that, braking is shorter; above, "
             "turning is. Both start with the reaction distance v times delta-t: at 10 m/s that is 16 of the 36 metres. (~35 s)")


def link(s):
    clear_content(s)
    headline(s, "The lecture stops at DOP; we turn DOP into metres of keep-out")
    def chain(items, y, col, gap=0.15):
        x = 0.35
        for i, (wd, a, b) in enumerate(items):
            last = i == len(items) - 1
            box(s, x, y, wd, 0.95, fill=col if last else "FFFFFF", line=col, lw=1.5, radius=0.1, margin=0.06,
                align=PP_ALIGN.CENTER,
                paras=[P(R(a, size=12, bold=True, color="FFFFFF" if last else col), align=PP_ALIGN.CENTER),
                       P(R(b, size=13, bold=True, color="FFFFFF" if last else INK), align=PP_ALIGN.CENTER)])
            if i:
                arrow_shape(s, x - 0.13, y + 0.39, 0.11, 0.17, fill=LINE)
            x += wd + gap
    txt(s, 0.35, 1.45, 9.3, 0.3, [P(R("POSITION → KEEP-OUT DISTANCE", size=12, bold=True, color=BLUE),
                                     R("   SPP least squares and DOP, Weeks 4–6", size=12, color=MUTED))])
    chain([(2.25, "SPP least squares", "Δx = (HᵀH)⁻¹HᵀΔρ"), (1.45, "Geometry", "Q = (HᵀH)⁻¹"),
           (1.8, "HDOP", "√(Q_NN + Q_EE)"), (1.85, "Error", "σ_h = HDOP·σ_UERE"),
           (1.35, "Keep-out margin", "R + k·σ_h")], 1.78, BLUE)
    txt(s, 0.35, 2.9, 9.3, 0.3, [P(R("VELOCITY → STOPPING DISTANCE", size=12, bold=True, color=GREY),
                                    R("   Doppler, same H matrix", size=12, color=MUTED))])
    chain([(1.7, "Doppler", "ρ̇ᵢ − eᵢ·v_sat,ᵢ"), (2.6, "Same H, one linear solve", "= −eᵢ·v + c·δṫ"),
           (2.2, "Blend with IMU", "inverse-variance weights"), (2.35, "Braking distance", "v·Δt + v² / 2a")], 3.23, GREY)
    txt(s, 0.35, 4.3, 9.3, 0.32, [P(R("New vs the lecture: ", size=14, bold=True),
                                     R("DOP becomes a distance in metres; Doppler velocity becomes a deadline.", size=14))])
    txt(s, 0.35, 4.63, 9.3, 0.32, [P(R("Also in the code: Klobuchar ionosphere, ECEF ↔ NED and body ↔ NED rotations, k = √(−ln P) = 3.03 for P = 10⁻⁴.", size=12, color=MUTED))])
    source(s, "Own code: location.gnss_fix (wls from Stanford NAV Lab's gnss_lib_py), location.doppler_velocity, boundary.decide.")
    notes(s, "Say: This is where AAE4203 lives in the project. Top row: the SPP least-squares solution from weeks 4 to 6 gives us "
             "Q = (H^T H)^-1, HDOP, and sigma_h = HDOP times sigma_UERE. The lecture stops there, at an accuracy number. We turn it into "
             "a keep-out distance: R + k sigma_h, with k = 3.03 from accepting a 1-in-10,000 chance that the error is bigger. "
             "Bottom row: Doppler uses the same H to give velocity, blended with the IMU, and velocity sets the braking distance. "
             "Check the week numbers against your lecture notes. (~50 s)")


def cases(s):
    clear_content(s)
    headline(s, "Hong Kong's GNSS fails in three ways: jammed, scrambled, blocked")
    cards = [("JAMMED", "Oct 2018 · Wine & Dine Festival",
              "GPS jamming dropped 46 of 100 show drones into Victoria Harbour; about HK$1M damage.",
              "Our knob: GNSS lost → IMU only, σ_h grows, it backs away"),
             ("SCRAMBLED", "Sep 30–Oct 1, 2024 · harbour",
              "Ionospheric scintillation cancelled both drone shows. Show drones may only stray 5–10 cm.",
              "Our knob: σ_UERE up. Klobuchar models the average delay, not scintillation"),
             ("BLOCKED", "Every day · street canyons",
              "Towers hide satellites: fewer in view, worse geometry. PolyU's UrbanNav data: TST, Whampoa, Mong Kok.",
              "Our knob: sky mask 40° → HDOP 1.03 → 1.47, margin 18.6 → 25.6 m")]
    for i, (word, when, what, knob) in enumerate(cards):
        x = 0.35 + i * 3.15
        box(s, x, 1.5, 3.0, 3.42, fill=LIGHT, radius=0.05)
        txt(s, x + 0.2, 1.62, 2.6, 0.45, [P(R(word, size=24, bold=True, color=BLUE))])
        txt(s, x + 0.2, 2.1, 2.6, 0.3, [P(R(when, size=12, bold=True, color=MUTED))])
        txt(s, x + 0.2, 2.45, 2.6, 1.3, [P(R(what, size=15, color=INK))])
        box(s, x + 0.12, 3.82, 2.76, 0.98, fill="FFFFFF", radius=0.1, margin=0.1,
            paras=[P(R(knob, size=13, bold=True, color=GREY))])
    source(s, "Sources: SCMP, Oct 2018; RTHK, 1–2 Oct 2024; L.-T. Hsu et al., NAVIGATION 70(4), 2023; own simulation (repo, seed 1).")
    notes(s, "Say (Member 3): Three real ways GNSS goes wrong in Hong Kong. Jammed: 2018, someone jammed GPS at the Wine and Dine "
             "Festival and 46 of 100 drones fell into the harbour. Scrambled: on National Day 2024 two drone shows were cancelled because "
             "of ionospheric scintillation. Our code corrects the ionosphere with Klobuchar, but Klobuchar models the average delay, "
             "not this fast flickering. Blocked: every day, street canyons hide satellites; PolyU's own UrbanNav dataset records this. "
             "Each one is a knob in our demo. (~60 s)")


def demo(s):
    clear_content(s)
    set_title(s, "Case Study / Demo")
    headline(s, "In our simulator it brakes for the zone and turns for the tower")
    pic(s, A + "trajectories.png", 0.35, 1.45, 9.3)
    source(s, "Own simulation (repo main.py, seed 1). Live version: demo.html in the repo (loads Pyodide, needs internet).")
    notes(s, "LIVE DEMO (open demo.html before the talk; if the network fails, use these plots).\n"
             "1. Fly at the building at 10 m/s → BRAKE. 2. Again at 20 m/s → TURN: braking would need 113 m, turning 76 m, "
             "so it turns 98 m out. 3. Fly at the zone with 'Sky blocked below' 15°, then 40° → it stops further out, because HDOP "
             "and sigma_h grew. Say what changed in one sentence each time.\n"
             "Left plot: at 10 m/s it brakes when the gap falls below the braking distance, then holds at the margin, 15 m from "
             "the zone edge. Right plot: at 20 m/s turning is shorter, so it turns early and slides past the tower, 16 m clear. (~70 s)")


def results(s):
    clear_content(s)
    headline(s, "Remove the k·σ_h term and 76 of 80 flights breach the zone")
    cd = CategoryChartData()
    cd.categories = ["Open sky", "Street canyon", "σ_UERE 10 m", "GNSS lost"]
    cd.add_series("Margin R + k·σ_h (ours)", (14.5, 19.2, 26.0, 48.2))
    cd.add_series("Margin R only (baseline)", (-3.7, -5.6, -11.0, -23.1))
    gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(0.3), Inches(1.45), Inches(6.1), Inches(3.5), cd)
    ch = gf.chart
    ch.font.name = FONT
    ch.font.size = Pt(12)
    ch.has_legend = True
    ch.legend.position = XL_LEGEND_POSITION.TOP
    ch.legend.include_in_layout = False
    ch.legend.font.size = Pt(13)
    plot = ch.plots[0]
    plot.gap_width = 70
    plot.overlap = -5
    for ser, colr in zip(plot.series, (BLUE, RED)):
        ser.format.fill.solid()
        ser.format.fill.fore_color.rgb = rgb(colr)
        ser.invert_if_negative = False
    plot.has_data_labels = True
    dl = plot.data_labels
    dl.font.size = Pt(12)
    dl.font.bold = True
    dl.number_format = '0.0" m"'
    dl.number_format_is_linked = False
    dl.position = XL_LABEL_POSITION.OUTSIDE_END
    ca, va = ch.category_axis, ch.value_axis
    ca.tick_label_position = XL_TICK_LABEL_POSITION.LOW
    ca.tick_labels.font.size = Pt(12)
    ca.format.line.color.rgb = rgb(GREY)
    va.minimum_scale, va.maximum_scale, va.major_unit = -30, 60, 15
    va.has_major_gridlines = True
    va.major_gridlines.format.line.color.rgb = rgb("E3E7EC")
    va.tick_labels.font.size = Pt(11)
    va.has_title = True
    va.axis_title.text_frame.text = "Closest distance to zone edge (m)"
    va.axis_title.text_frame.paragraphs[0].runs[0].font.size = Pt(11)
    va.axis_title.text_frame.paragraphs[0].runs[0].font.bold = False
    va.format.line.fill.background()
    # stat callouts
    txt(s, 6.65, 1.5, 3.0, 0.7, [P(R("0 / 80", size=40, bold=True, color=BLUE))])
    txt(s, 6.65, 2.2, 3.0, 0.5, [P(R("flights breached with R + k·σ_h", size=15))])
    txt(s, 6.65, 2.75, 3.0, 0.7, [P(R("76 / 80", size=40, bold=True, color=RED))])
    txt(s, 6.65, 3.45, 3.0, 0.5, [P(R("breached with the radius only", size=15))])
    txt(s, 6.65, 4.0, 3.0, 0.95, [P(R("Why: without k·σ_h it aims at the line using a position that is wrong by metres.", size=13, color=MUTED))])
    source(s, "Own simulation, 20 seeds per condition, 60 s flights; bars = mean; breach = closest true distance < 3 m (aircraft radius). Below 0 = inside the zone.")
    notes(s, "Say: The baseline is the same guardrail without the k sigma_h term: margin is just the aircraft radius. "
             "20 flights per condition. With our margin, no flight comes within 3 m of the zone edge, 0 of 80. Without it, 76 of 80 do, "
             "and the average flight ends up inside the zone (negative bars). The price is distance: we stop 15 to 48 m short, and that "
             "gap grows exactly when GNSS gets worse. (~70 s)")


def limits(s):
    clear_content(s)
    headline(s, "Our margin trusts HDOP, and HDOP can't see a reflected signal")
    rows = [("Limitation", "Course error source", "Next step"),
            ("Reflected (NLOS) signals bias the fix; HDOP doesn't change", "Multipath, NLOS", "χ² residual test, drop the worst satellite"),
            ("Simulated white-noise errors, one sky-mask angle", "Error modelling", "Real Hong Kong data (UrbanNav)"),
            ("GPS only", "Geometry, DOP", "Add BeiDou and Galileo"),
            ("Jamming: IMU dead reckoning lasts seconds", "σ_h grows as ½σ_a·t²", "Kalman GNSS/IMU fusion"),
            ("One 360° 'magic' radar; level flight, no wind", "Sensor model", "Sensor network; speed cap from radar range")]
    gf = s.shapes.add_table(len(rows), 3, Inches(0.35), Inches(1.5), Inches(9.3), Inches(3.4))
    tbl = gf.table
    for j, w in enumerate((4.2, 2.2, 2.9)):
        tbl.columns[j].width = Inches(w)
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            c = tbl.cell(i, j)
            c.fill.solid()
            c.fill.fore_color.rgb = rgb(INK if i == 0 else ("FBEDEB" if i == 1 else ("FFFFFF" if i % 2 else LIGHT)))
            c.margin_left = c.margin_right = Inches(0.1)
            c.vertical_anchor = MSO_ANCHOR.MIDDLE
            c.text_frame.text = ""
            fill_tf(c.text_frame, [P(R(val, size=14 if i else 14, bold=(i == 0 or (i == 1 and j == 0)),
                                       color="FFFFFF" if i == 0 else INK))])
    source(s, "Own analysis; details and effort estimates in the repo's FUTURE_WORK.md (items 1–2, 5–6, 9–15, 19–20).")
    notes(s, "Say (Member 4): The biggest hole first. Our margin trusts HDOP. A reflected signal in a street canyon makes the fix "
             "wrong without changing HDOP, so sigma_h is too optimistic exactly where it matters. The fix is a residual test, RAIM-style. "
             "Then: our errors are simulated white noise, GPS only, dead reckoning only lasts seconds under jamming, and the radar sees "
             "everything. Each has a next step in FUTURE_WORK.md. (~60 s)")


def trends(s):
    clear_content(s)
    headline(s, "Zones are becoming live data, and urban GNSS is getting smarter")
    cards = [("Zones as live data", "The EU wants zone data in one digital format (EUROCAE ED-318, 2024). HK's Sandbox X tests UTM; Singapore is buying a UTM system (2026).",
              "For us: zones.geojson becomes a live feed"),
             ("Better urban GNSS", "Multi-constellation, residual (RAIM-style) checks, and 3D-mapping-aided GNSS from PolyU AAE, tested on UrbanNav.",
              "For us: run location.py on real HK data"),
             ("Fence or warning?", "DJI turned its US no-fly zones into warnings (Jan 2025). China made GB 42590-2023 mandatory (Jun 2024). GBA routes cross two authorities' maps.",
              "For us: who may override the pilot?")]
    for i, (t, body, us) in enumerate(cards):
        x = 0.35 + i * 3.15
        box(s, x, 1.5, 3.0, 3.42, fill=LIGHT, radius=0.05)
        txt(s, x + 0.2, 1.65, 2.6, 0.75, [P(R(t, size=20, bold=True, color=BLUE))])
        txt(s, x + 0.2, 2.35, 2.6, 1.6, [P(R(body, size=13))])
        box(s, x + 0.12, 4.05, 2.76, 0.75, fill="FFFFFF", radius=0.1, margin=0.1,
            paras=[P(R(us, size=13, bold=True, color=GREY))])
    source(s, "Sources: EUROCAE ED-318 (Feb 2024); TLB Sandbox X; Asian Aviation, May 2026; H.-F. Ng, PolyU thesis, 2025; DroneDJ, 14 Jan 2025; GB 42590-2023.")
    notes(s, "Say: Three trends, each with a 'for us'. One: no-fly zones are turning into live data. Europe standardised the format, "
             "Hong Kong and Singapore are both building traffic-management systems, so our zone file becomes a feed. Two: urban GNSS "
             "is getting smarter, including 3D-mapping-aided GNSS from PolyU AAE itself. Three, the open question: hard fence or warning? "
             "DJI dropped hard no-fly zones in the US in 2025, while China made its first mandatory drone standard in 2024. (~70 s)")


def conclusion(s):
    clear_content(s)
    headline(s, "Three things to remember")
    items = [(BLUE, BLUE_T, "1", "A geofence is only as good as the position you check it against: margin = R + k·σ_h."),
             (PURP, PURP_T, "2", "A building measured by radar doesn't care about GNSS error. A zone on a map does."),
             (GREY, GREY_T, "3", "Speed sets the distance: brake below 15.8 m/s, turn above it.")]
    for i, (c, tint, n, t) in enumerate(items):
        y = 1.55 + i * 1.12
        box(s, 0.35, y, 9.3, 0.95, fill=tint, radius=0.12)
        box(s, 0.55, y + 0.17, 0.62, 0.62, fill=c, shape=MSO_SHAPE.OVAL, align=PP_ALIGN.CENTER, margin=0,
            paras=[P(R(n, size=22, bold=True, color="FFFFFF"), align=PP_ALIGN.CENTER)])
        txt(s, 1.4, y + 0.08, 8.1, 0.8, [P(R(t, size=20, bold=True, color=INK))], anchor=MSO_ANCHOR.MIDDLE)
    notes(s, "Say the three lines slowly, one per colour. No new material. Then: 'Thank you, questions?' (~40 s)")


def references(s):
    clear_content(s)
    refs = [
        "[1] L.-T. Hsu, F. Huang, H.-F. Ng, G. Zhang, Y. Zhong, X. Bai and W. Wen, “Hong Kong UrbanNav: An open-source multisensory dataset for benchmarking urban navigation algorithms,” NAVIGATION, vol. 70, no. 4, navi.602, 2023.",
        "[2] J. A. Klobuchar, “Ionospheric time-delay algorithm for single-frequency GPS users,” IEEE Trans. Aerosp. Electron. Syst., vol. AES-23, no. 3, pp. 325–331, 1987.",
        "[3] H.-F. Ng, “Urban navigation using 3D mapping-aided (3DMA) GNSS,” Ph.D. thesis, Dept. of Aeronautical and Aviation Engineering, The Hong Kong Polytechnic University, 2025.",
        "[4] JARUS, “JARUS guidelines on Specific Operations Risk Assessment (SORA), Main Body,” JAR-doc-25, ed. 2.5, May 2024.",
        "[5] Civil Aviation Department, “Permission to conduct trial operations of unconventional aircraft in Hong Kong,” AIC 20/25, 2025.",
        "[6] HKSAR Government, press release on the Small Unmanned Aircraft (Amendment) Order 2025 and the Air Navigation (Hong Kong) Order 1995 (Amendment) Order 2025, 17 Jul. 2025.",
        "[7] Civil Aviation Authority of Singapore, “Operator and activity permits,” caas.gov.sg, accessed 17 Nov. 2026.",
        "[8] EUROCAE, “ED-318: Technical specification for geographical zones and U-space data provision and exchange,” Feb. 2024.",
        "[9] Stanford NAV Lab, “gnss_lib_py,” GitHub repository (MIT licence), accessed Nov. 2026.",
        "[10] News: SCMP (GPS jamming, Oct. 2018); RTHK (scintillation, Oct. 2024); CAAS (Changi drones, 19 Jun. 2019); avi-go (EH216-S, 28 Aug. 2026); Asian Aviation (Singapore UTM, May 2026).",
    ]
    txt(s, 0.35, 0.85, 9.3, 4.15, [P(R(r, size=11), after=4) for r in refs])
    notes(s, "IEEE style. [1] and [2] are the journal papers the template asks for. Check [2]'s volume and pages against the paper.")


def thanks(s):
    sh = {x.name: x for x in s.shapes}
    set_runs(sh["Rectangle 3"], ["Group Gxx  ·  Topic No. XX — Staying inside the line"])
    notes(s, "Q&A, 3 minutes, whole group. Likely questions and owners:\n"
             "Why not RTK? (M2) RTK shrinks sigma, it doesn't remove it; the 2024 shows needed 5–10 cm and were still cancelled.\n"
             "Why k = 3.03? (M2) P(error > k sigma) = exp(-k^2) for a circular 2-D Gaussian; we accepted 1e-4.\n"
             "HDOP fine but a signal is reflected? (M4) Then sigma_h is optimistic; fix = chi-square residual test.\n"
             "GNSS and radar both fail? (M4) Dead reckoning then RETURN; beyond that, the emergency procedure AIC 20/25 ¶11.1 requires.\n"
             "Isn't 1 Hz too slow? (M2) At 10 Hz delta-t is about 0.7 s, reaction distance at 10 m/s drops from 16 m to 7 m.\n"
             "Why hover instead of going around? (M3) It's a guardrail, not a planner.\n"
             "DJI dropped hard fences, why build one? (M1) Fences stop careless pilots; AIC 20/25 makes containment mandatory for trials.\n"
             "Isn't overriding the pilot 'autonomous operation'? (M1) It's a pre-programmed protection, which ¶6.10 allows.")


# ------------------------------------------------------------------ main
def main(src, out):
    prs = Presentation(src)
    t = list(prs.slides)  # template slides, 0-based
    tag_xml = copy.deepcopy([sh for sh in t[5].shapes if is_tag(sh)][0]._element)
    layout = [l for l in prs.slide_layouts if l.name == "Title and Content"][0]

    def new():
        s = prs.slides.add_slide(layout)
        for ph in list(s.placeholders):
            if ph.placeholder_format.type != 1:
                drop(ph)
        return s

    S = {}
    S["cover"], S["team"], S["outline"] = t[1], t[2], t[3]
    S["bg"], S["sota"] = t[5], t[6]
    S["p1"], S["p2"], S["link"] = t[8], t[9], t[10]
    S["case"], S["res"] = t[12], t[13]
    S["lim"], S["trend"], S["concl"], S["refs"], S["thanks"] = t[15], t[16], t[17], t[18], t[19]
    for k in ("ehang", "aic", "zb", "h2", "zp", "h3", "zg", "speed", "demo"):
        S[k] = new()
    titles = {"ehang": "Background and Motivation", "aic": "Background and Motivation",
              "speed": "Technical Principle (2): Key Equations", "demo": "Case Study / Demo"}
    for k, v in titles.items():
        set_title(S[k], v)
    member = {"outline": 1, "bg": 1, "ehang": 1, "aic": 1, "sota": 1, "p1": 2, "p2": 2, "zb": 2, "h2": 2, "zp": 2,
              "h3": 2, "zg": 2, "speed": 2, "link": 2, "case": 3, "demo": 3, "res": 3, "lim": 4, "trend": 4, "concl": 4}
    for k, m in member.items():
        set_tag(S[k], m, tag_xml)

    cover(S["cover"]); team(S["team"]); outline(S["outline"])
    background(S["bg"]); ehang(S["ehang"]); aic(S["aic"]); singapore(S["sota"])
    principle1(S["p1"])
    hub(S["p2"], nxt="blue")
    notes(S["p2"], "Say: Here is one second of the loop as three questions. Blue: where am I, and how sure. Purple: what is right next "
                   "to me. Grey: what do I do. Blue and purple never talk to each other, like most group projects; they only meet at the "
                   "decision. Click to zoom into each. (~25 s)")
    zoom(S["zb"], "blue", "Blue: where we are, and how wrong that might be")
    notes(S["zb"], "Say: Left to right. With at least 4 satellites: remove the ionosphere with Klobuchar, solve SPP least squares, "
                   "and from the same geometry get HDOP and sigma_h. Doppler with the same H gives velocity, blended with the IMU by "
                   "inverse variance. No fix: IMU dead reckoning, and sigma_h grows with t squared. Out comes p, v, sigma_h, and the "
                   "zone threat uses margin R + k sigma_h. (~45 s)")
    hub(S["h2"], nxt="purple", seen=("blue",))
    notes(S["h2"], "Click straight through: back to the overview, then into purple.")
    zoom(S["zp"], "purple", "Purple: the radar measures the building, so GNSS error never enters")
    notes(S["zp"], "Say: The radar gives range and bearing. Two rotations, mount angle then heading, put it in NED. No GNSS anywhere, "
                   "so the margin uses the radar's own error: about 4.5 m. (~20 s)")
    hub(S["h3"], nxt="grey", seen=("blue", "purple"))
    notes(S["h3"], "Click straight through into grey.")
    zoom(S["zg"], "grey", "Grey: one rule for both threats, driven by closing speed")
    notes(S["zg"], "Say: For every threat, every second: how fast are we closing, how much room is left, how far do we fly before a "
                   "decision acts, how far to brake, how far to turn. Inside the margin: RETURN. Slow enough to brake in time: CLEAR. "
                   "Otherwise, turn if there is room, else brake. The most urgent threat wins. (~50 s)")
    speed(S["speed"], None)
    link(S["link"])
    cases(S["case"]); demo(S["demo"]); results(S["res"])
    limits(S["lim"]); trends(S["trend"]); conclusion(S["concl"])
    references(S["refs"]); thanks(S["thanks"])
    for k in ("zb", "h2", "zp", "h3", "zg"):
        add_morph(S[k])

    # order + delete
    order = ["cover", "team", "outline", "bg", "ehang", "aic", "sota", "p1", "p2", "zb", "h2", "zp", "h3", "zg",
             "speed", "link", "case", "demo", "res", "lim", "trend", "concl", "refs", "thanks"]
    lst = prs.slides._sldIdLst
    by_slide = {}
    for sid in list(lst):
        by_slide[prs.part.related_part(sid.rId)] = sid
    keep = [by_slide[S[k].part] for k in order]
    for sid in list(lst):
        if sid not in keep:
            rid = sid.rId
            lst.remove(sid)
            prs.part.drop_rel(rid)
    for sid in list(lst):
        lst.remove(sid)
    for sid in keep:
        lst.append(sid)
    prs.save(out)
    print("saved", out, len(prs.slides), "slides")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
