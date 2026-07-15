#!/usr/bin/env python3
"""Export a build123d model to STEP + STL, validate printability, render views.

Usage:
    python export.py <model.py> [--out-dir DIR] [--bed 220x220x250]
                     [--no-snapshot] [--name NAME]

Contract: <model.py> must define a function `build()` that returns a build123d
Part/Solid/Compound, OR a dict {name: part} for multi-part jobs.

Outputs (next to model.py or in --out-dir):
    <name>.step       — parametric, for Fusion 360 / CAD editing
    <name>.stl        — mesh, for the slicer
    <name>_views.png  — 4-view snapshot for visual review
Prints a markdown report with validation results to stdout.
"""
from __future__ import annotations

import argparse
import importlib.util
import math
import sys
from pathlib import Path

OVERHANG_DEG = 50.0  # faces steeper than this (from vertical) likely need supports


def fail(msg: str) -> "NoReturn":  # noqa: F821
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def load_build(model_path: Path):
    spec = importlib.util.spec_from_file_location("pd_model", model_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore[union-attr]
    if not hasattr(mod, "build"):
        fail(f"{model_path.name} must define build() returning a build123d part or dict of parts")
    return mod.build()


def mesh_report(stl_path: Path, bed: tuple[float, float, float]) -> list[str]:
    import numpy as np
    import trimesh

    lines = []
    m = trimesh.load_mesh(stl_path)
    bb = m.bounds
    dims = bb[1] - bb[0]
    lines.append(f"- **Bounding box:** {dims[0]:.1f} x {dims[1]:.1f} x {dims[2]:.1f} mm")
    lines.append(f"- **Volume:** {m.volume / 1000:.1f} cm3 | **Watertight:** {'YES' if m.is_watertight else 'NO  <-- FIX BEFORE PRINTING'}")
    fits = all(d <= b + 1e-6 for d, b in zip(sorted(dims), sorted(bed))) and dims[2] <= bed[2]
    direct_fit = dims[0] <= bed[0] and dims[1] <= bed[1] and dims[2] <= bed[2]
    if direct_fit:
        lines.append(f"- **Bed fit ({bed[0]:.0f}x{bed[1]:.0f}x{bed[2]:.0f}):** OK")
    elif fits:
        lines.append(f"- **Bed fit:** only if reoriented/rotated — check orientation")
    else:
        lines.append(f"- **Bed fit:** DOES NOT FIT {bed[0]:.0f}x{bed[1]:.0f}x{bed[2]:.0f} — split or scale")

    # Overhang estimate: downward-facing faces steeper than OVERHANG_DEG from vertical,
    # excluding faces touching the build plate (bottom).
    n = m.face_normals
    down = n[:, 2] < -math.sin(math.radians(90 - OVERHANG_DEG))
    face_centers = m.triangles_center
    on_plate = face_centers[:, 2] < bb[0][2] + 0.5
    overhang_faces = down & ~on_plate
    if overhang_faces.any():
        area = float(m.area_faces[overhang_faces].sum())
        pct = 100.0 * area / float(m.area)
        if pct > 1.0:
            lines.append(f"- **Overhangs >{OVERHANG_DEG:.0f} deg:** ~{pct:.0f}% of surface — consider reorienting, chamfering undersides, or enabling supports")
        else:
            lines.append(f"- **Overhangs:** negligible ({pct:.1f}% of surface)")
    else:
        lines.append("- **Overhangs:** none detected")
    return lines


def snapshot(stl_path: Path, out_png: Path) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    import trimesh
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection

    m = trimesh.load_mesh(stl_path)
    views = [("isometric", (30, -60)), ("front (XZ)", (0, -90)), ("top (XY)", (90, -90)), ("right (YZ)", (0, 0))]
    fig = plt.figure(figsize=(12, 10))
    tri = m.vertices[m.faces]
    lim_lo, lim_hi = m.bounds[0].min(), m.bounds[1].max()
    for i, (title, (elev, azim)) in enumerate(views, 1):
        ax = fig.add_subplot(2, 2, i, projection="3d")
        pc = Poly3DCollection(tri, alpha=0.95, facecolor="#8fb4d9", edgecolor="#2a4a6b", linewidths=0.1)
        ax.add_collection3d(pc)
        ax.set_xlim(lim_lo, lim_hi); ax.set_ylim(lim_lo, lim_hi); ax.set_zlim(lim_lo, lim_hi)
        ax.view_init(elev=elev, azim=azim)
        ax.set_title(title, fontsize=11)
        ax.set_box_aspect((1, 1, 1))
    fig.tight_layout()
    fig.savefig(out_png, dpi=80)
    plt.close(fig)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("model", help="Python file defining build()")
    ap.add_argument("--out-dir", default=None)
    ap.add_argument("--bed", default="220x220x250", help="Bed WxDxH in mm (default: Anet ET4)")
    ap.add_argument("--name", default=None, help="Output basename (default: model filename)")
    ap.add_argument("--no-snapshot", action="store_true")
    args = ap.parse_args()

    from build123d import export_step, export_stl  # defer heavy import

    model_path = Path(args.model).resolve()
    if not model_path.is_file():
        fail(f"Model file not found: {model_path}")
    try:
        bed = tuple(float(v) for v in args.bed.lower().split("x"))
        assert len(bed) == 3
    except Exception:
        fail("--bed must look like 220x220x250")

    out_dir = Path(args.out_dir).resolve() if args.out_dir else model_path.parent
    out_dir.mkdir(parents=True, exist_ok=True)
    base = args.name or model_path.stem

    result = load_build(model_path)
    parts = result if isinstance(result, dict) else {base: result}

    print("# print-design export report\n")
    for name, part in parts.items():
        step_path = out_dir / f"{name}.step"
        stl_path = out_dir / f"{name}.stl"
        export_step(part, str(step_path))
        export_stl(part, str(stl_path), tolerance=0.05, angular_tolerance=0.2)
        print(f"## {name}\n")
        print(f"- **STEP (edit in Fusion 360):** `{step_path}`")
        print(f"- **STL (slice):** `{stl_path}`")
        for line in mesh_report(stl_path, bed):  # type: ignore[arg-type]
            print(line)
        if not args.no_snapshot:
            png = out_dir / f"{name}_views.png"
            snapshot(stl_path, png)
            print(f"- **Views (Read this to inspect):** `{png}`")
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
