---
name: print-design
description: Turn ideas, descriptions, photos, or measurements into 3D-printable designs - parametric CAD models exported as STEP (editable in Fusion 360) + STL (sliceable), with printability validation and optional G-code generation. Use this skill whenever the user wants to design, model, or print a physical part or object - brackets, hooks, mounts, enclosures, clips, adapters, organizers, replacement parts - or mentions 3D printing, su impresora 3D, STL, STEP, G-code, Fusion 360, or shares a photo/measurements of something to replicate or fix. Trigger even for casual phrasing like "diseñame un soporte para X", "quiero imprimir algo que...", "se me rompió esta pieza".
---

# Print Design: idea → printable part

Pipeline: capture the spec → write parametric build123d Python → export STEP + STL with validation → visually inspect renders → iterate → (optional) slice to G-code.

The design source is a Python file the user keeps: every dimension is a named parameter, so iteration means changing a number and re-running. STEP goes to Fusion 360 for manual edits; STL goes to the slicer.

## User's default setup

Unless told otherwise, assume: **Anet ET4** (bed 220×220×250 mm, 0.4 mm nozzle, Bowden extruder, custom Marlin-flavor firmware) printing **PETG**. Bake PETG behavior into the design itself — see `references/printability-fdm.md` for clearances, overhang and orientation rules. These defaults live in `assets/anet_et4_petg.ini`.

## Dependencies

`pip install build123d trimesh --break-system-packages` (matplotlib usually present). The build123d/OCP wheel is ~150 MB — on a fresh sandbox, install before doing anything else, and if the call times out just run it again (pip resumes from cache).

## Workflow

### 1. Capture the spec — design brief first

Write a short brief before any code: what the part does, critical dimensions, what it mates with, expected loads, print orientation. Sources:

- **Description**: extract dimensions; apply sensible defaults for the rest and state them.
- **Photo**: estimate proportions from reference objects in frame; ask ONLY for the fit-critical measurement (e.g. "¿cuánto mide el diámetro del tubo donde va montado?"). Never guess a dimension that determines whether the part fits something.
- **Measurements/sketch**: use as given; flag anything inconsistent.

One focused question max when something is fit-critical; otherwise proceed with explicit assumptions the user can correct on iteration.

### 2. Write the parametric source

Create `<part>.py` in the user's project folder (they keep and iterate on it):

```python
"""<part> — <one-line purpose>. All dims in mm."""
from build123d import *

# ── Parameters (edit these) ─────────────────────
WIDTH = 30        # ancho de la placa base
HOLE_D = 4.5      # M4 clearance
FIT_CLEARANCE = 0.3  # holgura PETG para encajes
# ────────────────────────────────────────────────

def build():
    with BuildPart() as p:
        ...
    return p.part   # or {"base": ..., "lid": ...} for multi-part
```

Modeling patterns and common build123d pitfalls: `references/build123d-patterns.md`. Design for the print bed from the start: pick the orientation the part will print in, design the biggest flat face as the bottom, chamfer (not fillet) bottom edges.

### 3. Export + validate

```bash
python scripts/export.py <part>.py [--bed 220x220x250] [--out-dir DIR]
```

Produces `<part>.step`, `<part>.stl`, `<part>_views.png` and a report: bounding box, watertight check, bed fit, overhang estimate. 

**Read the `_views.png` ALWAYS** — the report catches topology errors but only your eyes catch "the hook opens the wrong way". In sandboxed environments (Cowork), pass `--out-dir` inside a Read-accessible folder (session outputs or the project folder), not `/tmp`.

If watertight = NO or the geometry looks wrong: fix the source, re-run. Don't hand the user a broken STL.

### 4. Iterate with the user

Show the views PNG and the key dimensions. Ask what to adjust. Changes go in the Parameters block; re-export. Keep `<part>.py`, `.step`, and `.stl` together in the project folder — same basename.

### 5. Deliver

Final files to the user's project folder: `<part>.py` (source of truth), `<part>.step` (Fusion 360), `<part>.stl` (slicer). Present them with a one-line print recommendation: orientation, supports yes/no, infill suggestion.

### 6. Optional: G-code

Only when the user asks for G-code directly. Uses the vendored `scripts/gcode_tool.py` (from earthtojake/text-to-cad, MIT):

```bash
python scripts/gcode_tool.py discover            # find slicer CLIs
# write wrapper JSON: absolute native_config path → assets/anet_et4_petg.ini
python scripts/gcode_tool.py slice --input part.stl --output part.gcode --profile wrapper.json --backend auto --dry-run
# review the dry-run command, then add --execute
python scripts/gcode_tool.py validate --gcode part.gcode --profile wrapper.json --json
```

Details and wrapper format: `references/slicing.md`. If no slicer CLI is installed (typical in sandbox), don't fight it: deliver the STL plus `assets/anet_et4_petg.ini` and tell the user to slice in OrcaSlicer (the .ini imports directly). Never invent printer profiles for machines you don't have specs for — ask.

## Iteration etiquette

- Parameters are the API: when the user says "más ancho" or "el hoyo más grande", change the named parameter, never hardcode.
- After 2+ iterations on the same part, summarize current parameter values so the user sees the state.
- If the user will edit in Fusion 360, remind them: edits there live in the STEP/F3D, not the Python — future parameter changes from this skill would overwrite. Pick one editing home per part.

## What NOT to do

- Don't deliver STL-only. STEP costs nothing extra and is the only sanely editable format in Fusion 360.
- Don't skip the visual check on `_views.png`, and don't claim validations that didn't run.
- Don't design in-air geometry: every part prints layer by layer — if a feature floats at 45°+ without material under it, redesign or note that supports are required.
- Don't guess fit-critical dimensions from photos.
- Don't generate G-code without a dry-run first, and never send G-code to a printer from this skill.

## References

- `references/printability-fdm.md` — FDM/PETG design rules: clearances, overhangs, orientation, walls, holes, threads. Read when designing any part that mates with something.
- `references/build123d-patterns.md` — modeling cookbook and pitfalls. Read before writing your first part in a session.
- `references/slicing.md` — gcode_tool wrapper format, backend order, validation. Read only for G-code requests.
