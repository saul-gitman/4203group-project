# Presentation

`Gxx_Txx_AAE4203.pptx` is built inside the course template
(`template/AAE4203_Group_Presentation_Student_Template_v2.pptx`). The template's
frame (title bar, gold presenter tag, slide order, the required "Link to
AAE4203" slide) is kept; the content area uses one colour code throughout:

| colour | means | question |
|---|---|---|
| Blue | Flow 1: GNSS + IMU, map zones | Where am I, and how sure? |
| Purple | Flow 2: radar, buildings | What is right next to me? |
| Grey | The decision | What do I do now? |

## Slides (15 min talk + 3 min Q&A)

| # | part | presenter | headline |
|---|---|---|---|
| 1–3 | Cover, team, outline | | |
| 4 | Background | Member 1 | Since July 2025, Hong Kong's law has a slot for every size of drone |
| 5 | Background | Member 1 | A fully certified aircraft still needs a Hong Kong box to fly in (EH216-S) |
| 6 | Background | Member 1 | The permission rule (AIC 20/25 ¶5.3–5.5) is secretly a navigation spec |
| 7 | State of the art | Member 1 | Singapore has the same problem, with even less room |
| 8 | Technical principle (1) | Member 2 | A zone exists only on a map; a building can be measured |
| 9–14 | Technical principle (2) | Member 2 | Flowchart hub → zoom blue → hub → zoom purple → hub → zoom grey (Morph) |
| 15 | Key equations | Member 2 | Speed sets the distance: brake below 15.8 m/s, turn above it |
| 16 | Link to AAE4203 | Member 2 | The lecture stops at DOP; we turn DOP into metres of keep-out |
| 17 | Case study | Member 3 | Hong Kong's GNSS fails in three ways: jammed, scrambled, blocked |
| 18 | Demo | Member 3 | Our simulator brakes for the zone and turns for the tower (live: `code/demo.html`) |
| 19 | Results | Member 3 | Remove the k·σ_h term and 76 of 80 flights breach the zone |
| 20 | Limitations | Member 4 | Our margin trusts HDOP, and HDOP can't see a reflected signal |
| 21 | Future trends | Member 4 | Zones are becoming live data, and urban GNSS is getting smarter |
| 22 | Conclusion | Member 4 | Three things to remember |
| 23–24 | References, Q&A | | Q&A answers with owners are in slide 24's notes |

## Still to do by hand

- Names, student numbers, group, topic number, slot (slides 1 and 24).
- EH216-S Cyberport photo on slide 5 (replace the dashed box).
- Check "Weeks 4–6" on slide 16 and the Klobuchar reference details on slide 23.
- Morph needs PowerPoint 2019/2021/365; test on the classroom PC. Elsewhere the
  slides just appear in order.

## Rebuild

```
pip install python-pptx playwright matplotlib pillow
python presentation/build/flow_svgs.py        # flowchart panels (SVG)
python presentation/build/render_svg.py presentation/assets/flow_*.svg   # SVG -> PNG (needs Chrome)
python code/analysis/trajectories.py          # slide 18 plot
python presentation/build/build.py presentation/template/AAE4203_Group_Presentation_Student_Template_v2.pptx presentation/Gxx_Txx_AAE4203.pptx
```

Rebuilding overwrites hand edits in the .pptx (names, photo), so edit the
script, or rebuild before you fill those in.

The longer working plan with research notes lives in the Claude doc
"AAE4203 LAE Guardrail — Project Recap & Slide Plan".
