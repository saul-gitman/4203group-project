# AAE4203 group project: LAE guardrail

Keeping an eVTOL out of no-entry zones and away from buildings, for low-altitude
flights in Hong Kong and Singapore. A GNSS + IMU flow measures our position and
how wrong it might be; a radar flow measures buildings directly; one decision
turns both into CLEAR / BRAKE / TURN / RETURN.

**The one idea:** a geofence is only as good as the position you check it
against, so the keep-out margin is `R + k·σ_h`, with `σ_h = HDOP·σ_UERE` from the
course's SPP least squares.

## Layout

| folder | what is in it |
|---|---|
| [`code/`](code/) | The Python guardrail, the browser demo (`demo.html`) and `analysis/` scripts. Technical README inside. |
| [`data/`](data/) | `zones.geojson`: the example no-entry zone (made up, eSUA-style). |
| [`docs/`](docs/) | Flowchart (HTML + PNG), braking-vs-turning chart, `FUTURE_WORK.md`. |
| [`presentation/`](presentation/) | The deck in the course template, its figures, and the scripts that build it. |
| [`references/`](references/) | Sources and facts used in the deck (regulations, incidents, papers). |
| [`notes/`](notes/) | Session summaries: what was decided and what is still open. |

## Quick start

```
pip install numpy
cd code
python main.py                     # four scripted flights
python analysis/baseline.py        # with vs without k·σ_h, 20 seeds each
```

Open `code/demo.html` in a browser for the live demo (loads Pyodide from a CDN,
so it needs internet).

## Presentation

`presentation/Gxx_Txx_AAE4203.pptx`: 24 slides in the professor's template,
speaker notes on every slide, Morph zoom on the flowchart (slides 9–14).
Before submitting: fill names, student numbers, group and topic numbers, slot,
add the EH216-S photo on slide 5, and rename the file to `Gxx_Txx_AAE4203.pptx`
with the real numbers. See [`presentation/README.md`](presentation/README.md).
