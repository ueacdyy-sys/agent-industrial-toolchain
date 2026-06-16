# KiCad Reverse Engineering Findings

## Installation
- Path: `D:\Tools\KiCad\`
- Version: 10.0
- Bundled Python: 3.11 (in `bin/python.exe`)

## Architecture

### Executables
| Tool | Path | Headless? |
|------|------|-----------|
| kicad.exe | bin/kicad.exe | No (GUI) |
| kicad-cli.exe | bin/kicad-cli.exe | **YES** |
| pcbnew.exe | bin/pcbnew.exe | No (GUI) |
| eeschema.exe | bin/eeschema.exe | No (GUI) |
| gerbview.exe | bin/gerbview.exe | No (GUI) |

### Python API Modules
| Module | DLL | Python wrapper? | Safe for automation? |
|--------|-----|-----------------|---------------------|
| pcbnew | _pcbnew.dll (31MB) | ✅ pcbnew.py | ✅ via import OR kicad-cli |
| eeschema | _eeschema.dll (19MB) | ❌ | ❌ Only via kicad-cli |
| cvpcb | _cvpcb.dll (11MB) | ❌ | ❌ Only via kicad-cli |
| gerbview | _gerbview.dll (3.6MB) | ❌ | ❌ Only via kicad-cli |
| pl_editor | _pl_editor.dll (3.3MB) | ❌ | ❌ Only via kicad-cli |
| pcb_calculator | _pcb_calculator.dll (2.9MB) | ❌ | ❌ Only via kicad-cli |
| kiapi | kiapi.dll (2.3MB) | ❌ (C DLL only) | ❌ ctypes only |

### Key DLL Dependencies
- kicommon.dll (10MB) - shared KiCad logic
- ngspice.dll (7.5MB) - SPICE circuit simulation
- OpenCascade TK*.dll - 3D modeling kernel (STEP export)
- wxWidgets - GUI framework (not needed for headless)

## kicad-cli: The Safe Automation Interface

### Available Subcommands
```
kicad-cli pcb {drc, export, import, render, upgrade}
kicad-cli sch {erc, export, upgrade}
kicad-cli fp {export, upgrade}
kicad-cli sym {export, upgrade}
kicad-cli jobset {run}
```

### PCB Export Formats
3dpdf, brep, drill, dxf, gencad, gerbers, glb, hpgl, ipc2581, ipcd356, odb, pdf, ply, pos, ps, stats, step, svg, vrml

### Headless DRC (Design Rule Check)
```
kicad-cli pcb drc --format json --exit-code-violations --schematic-parity input.kicad_pcb
```
- Outputs JSON for machine parsing
- Non-zero exit code on violations (CI/CD ready)
- Schematic parity check ensures PCB matches schematic

### Headless ERC (Electrical Rules Check)
```
kicad-cli sch erc --format json --exit-code-violations input.kicad_sch
```

## Verified: Real Board Test
- Loaded CM5_MINIMA_3.kicad_pcb: 112 footprints, 221 nets, 2528 tracks, 14 zones
- Duplicate() works
- SaveBoard() works (3.4MB output)
- All via Python pcbnew module

## Strategy for kicad-mcp-revival
1. **Primary interface: kicad-cli** (subprocess calls) - safest, handles all modules
2. **Secondary interface: pcbnew Python API** - for board manipulation (add footprints, route)
3. **Avoid: direct DLL calls** - no Python wrappers, unstable across versions
4. **Windows-specific considerations**: PATH must include bin/, PYTHONPATH must include bin/

## Blender Findings
- Path: D:\\IndustrialDesignTools\\Apps\\Blender\\5.1\\
- Has --background mode for headless operation
- Bundled Python with full bpy API
- Python scripts in 5.1/scripts/

## FreeCAD Status
- Only configuration files found (no executable installed)
- Not usable for automation without installation
