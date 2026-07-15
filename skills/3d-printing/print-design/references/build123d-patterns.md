# build123d cookbook for printable parts

Builder mode is the default style. Everything in mm. `build()` returns `p.part` or a dict for multi-part.

## Core skeleton

```python
from build123d import *

def build():
    with BuildPart() as p:
        Box(40, 30, 10)                              # centered at origin
        with Locations((10, 0, 0)):
            Cylinder(3, 20, mode=Mode.SUBTRACT)       # hole
        fillet(p.edges().filter_by(Axis.Z), 2)        # vertical edges only
    return p.part
```

## Selectors you'll actually use

```python
p.edges().filter_by(Axis.Z)                  # vertical edges
p.faces().sort_by(Axis.Z)[-1]                # top face
p.faces().sort_by(Axis.Z)[0]                 # bottom face
p.edges().group_by(Axis.Z)[-1]               # edges of the top
p.edges().filter_by(GeomType.CIRCLE)         # circular edges (hole rims)
```

Chamfer bottom edges for the build plate (see printability rules):

```python
chamfer(p.edges().group_by(Axis.Z)[0], 0.6)
```

## Sketch → extrude (profiles, brackets)

```python
with BuildPart() as p:
    with BuildSketch(Plane.XZ) as sk:        # profile in XZ, extrude along Y
        with BuildLine() as ln:
            Polyline((0,0), (40,0), (40,8), (8,8), (8,30), (0,30), close=True)
        make_face()
        fillet(sk.vertices(), 2)             # round profile corners in 2D — cheaper than 3D fillets
    extrude(amount=20)
```

2D fillets in the sketch are far more robust than 3D fillets on the solid. Prefer them.

## Common features

```python
# Counterbored screw hole (top face, M4)
with Locations(p.faces().sort_by(Axis.Z)[-1]):
    CounterBoreHole(radius=2.25, counter_bore_radius=4.0, counter_bore_depth=2.5)

# Countersunk
CounterSinkHole(radius=2.25, counter_sink_radius=4.5)

# Slot
SlotCenterToCenter(center_separation=20, height=4.5)  # in a BuildSketch, then extrude with Mode.SUBTRACT

# Shell (box → open container, 2 mm walls)
offset(amount=-2, openings=p.faces().sort_by(Axis.Z)[-1])

# Rib/gusset: triangle sketch on the side plane, extrude
with BuildSketch(Plane.YZ.offset(WIDTH/2)):
    Triangle(a=15, b=15, C=90, align=(Align.MIN, Align.MIN))
extrude(amount=-3)

# Text (embossed on top)
with BuildSketch(p.faces().sort_by(Axis.Z)[-1]):
    Text("M4", font_size=8)
extrude(amount=0.6)

# Threads when truly needed (M8+): TrapezoidalThread from bd_warehouse — otherwise design for inserts/nuts
```

## Multi-part with fit clearance

```python
CLEAR = 0.25  # PETG snug fit, per side

def build():
    with BuildPart() as box:
        Box(50+2*WALL, 30+2*WALL, 20+WALL)
        offset(amount=-WALL, openings=box.faces().sort_by(Axis.Z)[-1])
    with BuildPart() as lid:
        Box(50 - 2*CLEAR, 30 - 2*CLEAR, 3)   # subtract clearance from male part
    return {"box": box.part, "lid": lid.part}
```

Clearance goes on the male part; export both and tell the user which is which.

## Pitfalls

- `Mode.SUBTRACT` cylinders: make them LONGER than the material (`height*1.01` or `2*T`) — exact-length booleans leave coincident-face artifacts and non-watertight meshes.
- Fillet radius ≥ wall thickness explodes. Stay under wall/2, or fillet in the 2D sketch.
- `align=` defaults center everything; `(Align.CENTER, Align.MAX, Align.MIN)` etc. controls which face touches where. Check alignment in the views PNG before trusting it.
- Rotated `Cylinder(rotation=(0,90,0))` rotates around the part center — verify position visually.
- A dict return must have unique, filesystem-safe keys (they become filenames).
- Don't `import *` inside `build()` — keep it at module top, the export runner imports the module once.
