# G-code generation (vendored gcode_tool.py)

`scripts/gcode_tool.py` (from earthtojake/text-to-cad, MIT) orchestrates real slicer CLIs. It never uploads or starts prints.

## Backend order

1. `orcaslicer` 2. `prusa-slicer` 3. `curaengine`. Discover with `python scripts/gcode_tool.py discover`. In sandboxes none is usually installed — in that case skip G-code, deliver the STL + `assets/anet_et4_petg.ini`, and tell the user to slice in OrcaSlicer (File > Import > Import Configs reads the .ini).

## Wrapper profile JSON

The tool requires a wrapper JSON with ABSOLUTE paths. Generate it at runtime (don't ship absolute paths):

```json
{
  "backend": "prusa-slicer",
  "native_config": "/abs/path/to/assets/anet_et4_petg.ini",
  "machine": {
    "name": "Anet ET4 (custom board)",
    "bed_size_mm": [220, 220],
    "z_height_mm": 250
  },
  "filament": {
    "type": "PETG",
    "nozzle_temp_c": 235,
    "bed_temp_c": 75
  }
}
```

For `orcaslicer` backend, `native_config`/`native_settings` must point at OrcaSlicer JSON configs instead of the .ini.

## Sequence

```bash
python scripts/gcode_tool.py inspect --input part.stl --json
python scripts/gcode_tool.py slice --input part.stl --output part.gcode --profile wrapper.json --backend auto --dry-run
# review the printed command, then re-run with --execute
python scripts/gcode_tool.py validate --gcode part.gcode --profile wrapper.json --json
```

Validation is static: movement bounds vs bed, temps present, extrusion present. `ok: true` ≠ safe to print — the user reviews orientation/adhesion in their slicer preview anyway. The user's ET4 runs a custom board: ALWAYS hand over the G-code file, never assume network access to the printer.
