# FDM printability rules (PETG-first)

Design rules for parts that print reliably on a Bowden-extruder machine (Anet ET4) with PETG. PETG is stronger and more temperature-resistant than PLA but strings more, bridges worse, and needs more clearance.

## Clearances (PETG)

| Fit | Clearance per side |
|---|---|
| Press fit (permanent) | 0.10–0.15 mm |
| Snug fit (assembles by hand, holds) | 0.20–0.25 mm |
| Free fit (slides, rotates) | 0.30–0.40 mm |
| Captive nut pocket (M3/M4) | +0.20 mm on flats |

- Vertical holes (axis = Z) print undersized: add **+0.3 mm to diameter**.
- Horizontal holes (axis in XY plane) sag at the top: use a **teardrop** shape (circle + 45° point at top) or add +0.4 mm and accept some cleanup.
- PETG self-welds when scraping: moving printed-in-place joints need ≥0.4 mm gaps.

## Overhangs, bridges, orientation

- Safe overhang without supports: **≤50° from vertical** (PETG sags earlier than PLA; 45° if surface quality matters).
- Bridges: keep under **25 mm** in PETG; chop longer spans with intermediate ribs or redesign.
- **Chamfer instead of fillet on bottom edges** — a fillet at the build plate creates a gradual overhang that ruins the first layers; a 45° chamfer prints cleanly.
- Pick print orientation AT DESIGN TIME. Layer lines are weak in tension/peel: orient so loads run along layers, not across them. A hook should print with the hook profile flat on the bed when possible.

## Walls, floors, features

- Minimum reliable wall: **1.6 mm** (4 perimeters @ 0.4 nozzle). 0.8–1.2 mm only for cosmetic skirts.
- Minimum floor/roof: 1.2 mm (6 layers @ 0.2).
- Smallest reliable pin: Ø3 mm (Ø5 mm if load-bearing — or design a hole + metal pin).
- Embossed/debossed text: ≥0.6 mm stroke width, ≥0.4 mm depth; top or side faces only.
- Threads: don't model threads under M8. Use captive nuts, heat-set inserts (design pocket Ø = insert OD − 0.1 mm), or thread-forming screws into a Ø(screw minor − 0.1) hole.

## Strength

- Screw holes near edges: keep ≥2×wall thickness of material around them.
- Cantilevered features: add a triangular gusset/rib (45°, prints support-free) instead of thickening.
- PETG flexes before breaking — for stiff parts add ribs rather than solid mass; for snap-fits PETG is excellent (1.5–2 mm thick tongue, 6–10 mm long).

## Bed and machine limits (Anet ET4)

- Usable bed: 220×220 mm, height 250 mm. Keep parts ≤210 mm in XY to leave room for skirt/brim.
- Single 0.4 mm nozzle; no multi-material. Design supports out, don't assume soluble supports.
- Bowden extruder: long retractions, stringing-prone — avoid designs with many isolated towers (lots of travel = lots of strings); prefer connected geometry.
