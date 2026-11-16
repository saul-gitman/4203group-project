# Session summary, 17 Nov 2026 (presentation build)

## What was done

1. **Recap and plan.** Read the repo and the course template, researched the
   background, and wrote a slide plan (Claude doc "AAE4203 LAE Guardrail —
   Project Recap & Slide Plan"). Facts and links are in `references/sources.md`.
2. **Baseline experiment.** New: `code/analysis/baseline.py`. Same flights with
   margin `R + k·σ_h` vs `R` only, 20 seeds × 4 conditions. Result: 0/80 vs
   76/80 breaches of the 3 m clearance. This fills the template's
   "compare with a baseline" requirement.
3. **Deck.** `presentation/Gxx_Txx_AAE4203.pptx`, 24 slides, built by script
   inside the template. Landscape flowchart panels redrawn for 16:9;
   Morph zoom hub → blue → hub → purple → hub → grey on slides 9–14.
   Native PowerPoint charts on slides 15 and 19. Speaker notes on every slide.
4. **Repo reorganised.**
   - `code/`: all Python, `demo.html`, `analysis/`.
   - `data/zones.geojson`: `boundary.py` and `make_demo.py` now read it from
     there (with a fallback so `demo.html` under Pyodide still works).
   - `docs/`: flowchart, chart, `FUTURE_WORK.md`.
   - `presentation/`: deck, template, assets, build scripts.
   - `references/` and `notes/`.

   `python code/main.py` gives the same results as before the move.

## Decisions

- One colour code for the whole deck: blue = GNSS/IMU + map zones, purple =
  radar + buildings, grey = decision. Taken from the repo's flowchart.
- The template stays as the frame; the content area is our own style. No
  bullet slides, a sentence headline on each slide, and the dividers and the
  README slide removed (the template says dividers are optional).
- The flowchart zoom is done in PowerPoint (Morph), not a separate HTML page.
- Case study = three real Hong Kong GNSS failures (2018 jamming, 2024
  scintillation, street canyons), each matched to a demo setting.

## Corrections made along the way

- "Cat C (>150 kg) allowed by the Chief Executive" mixed two regimes. Cat C is
  25–150 kg under Cap. 448G (CAD permission). Above 150 kg is a Cap. 448C trial
  of an unconventional aircraft (CE's power, used by the DGCA via AIC 20/25).
- The EH216-S "4 certs" are CAAC TC, AC, PC and the operators' AOCs.

## Still open

- Names, student numbers, group, topic number, slot (slides 1, 24); file name.
- EH216-S photo for slide 5 (on the NAS).
- Check "Weeks 4–6" (slide 16) and the Klobuchar reference (slide 23).
- Test Morph and `demo.html` on the classroom PC / network.
- GitHub repo rename to the group-project name (Settings → rename; old URLs
  redirect).
