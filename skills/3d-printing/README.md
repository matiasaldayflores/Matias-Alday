# Impresión 3D

## `print-design/` (propia) ⭐
Skill principal. Idea/foto/medidas → CAD paramétrico en Python (build123d) → STEP (Fusion 360) + STL,
con validación de imprimibilidad y G-code opcional. Configurada para **Anet ET4 + PETG**.

## Alternativas open-source (para comparar enfoques / inspirarse)
- **`cad-skill/`** (flowful-ai) — paramétrico con **CadQuery**, exporta STL + preview. Buen contraste con build123d.
- **`openscad-agent/`** (iancanderson) — enfoque **OpenSCAD**, valida geometría no-manifold e imprimibilidad.

Revisadas por seguridad junto al resto (limpio). Se mantienen como referencia; `print-design` sigue siendo la principal.
