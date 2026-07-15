# Impresión 3D

## `print-design/` (propia) ⭐
Skill principal. Idea/foto/medidas → CAD paramétrico en Python (build123d) → STEP (Fusion 360) + STL,
con validación de imprimibilidad y G-code opcional. Configurada para **Anet ET4 + PETG**.

## Alternativas open-source (otros enfoques)
- **`cad-skill/`** (`parametric-3d-printing`) — paramétrico con **CadQuery**, exporta STL + preview.
- **`openscad-agent/`** — enfoque **OpenSCAD** (`openscad`, `export-stl`, `preview-scad`), valida
  geometría no-manifold e imprimibilidad.

Revisadas por seguridad. `print-design` sigue siendo la principal.
