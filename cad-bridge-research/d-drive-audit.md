# D: Drive Industrial Toolchain — Complete Audit

## Verified & Working

### Blender 5.1.2 ✅
- Path: `D:/IndustrialDesignTools/Apps/Blender/blender.exe` (106MB)
- Python: 3.13.9 bundled
- MCP: **3 servers installed and verified**
  - `ahujasid_blender_mcp` — RPC server on 0.0.0.0:8765
  - `official_blender_mcp` — tests + chat client
  - `patrykiti_blender_ai_mcp` — production-shaped, 110KB server docs, vision harness, E2E tests
- CLI: `blender.exe --background --python-expr "..."` ✅
- Status: **READY for MCP-based automation**

### FreeCAD 1.1 ✅
- Path: `D:/Tools/FreeCAD 1.1/` (also `D:/IndustrialDesignTools/Apps/FreeCAD/`)
- Version: 1.1.1 (2026-04-14)
- Python: bundled in `bin/python.exe`
- API modules verified: Part(112), Mesh(26), Sketcher(14), Draft(230), Fem(51), CAM(7), BIM(7)
- CLI: `freecadcmd.exe` (headless) ✅
- Test: `Part.makeBox(10,20,30)` → volume=6000, area=2200 ✅
- Status: **READY for Python automation**

### KiCad 10.0 ✅
- Path: `D:/Tools/KiCad/` (also `D:/IndustrialDesignTools/Apps/KiCad/`)
- Python: 3.11 bundled
- CLI: `kicad-cli.exe` (headless) — pcb drc/export, sch erc/export, jobset ✅
- API: `pcbnew` (177 classes, 186 funcs) ✅
- Other modules (eeschema/cvpcb/gerbview): **NO Python wrapper — must use kicad-cli**
- Status: **READY — use kicad-cli for safety**

### PlatformIO 6.1.19 ✅
- Path: `D:/Tools/PlatformIO/`
- ESP32 support
- CLI working
- Status: **READY for embedded automation**

### OpenSCAD ✅
- Path: `D:/Tools/OpenSCAD/`
- Scriptable CAD with Python test helpers
- Status: **READY**

## Other Installed Tools

| Tool | Path | Type | Python? |
|------|------|------|---------|
| AutoCAD 2027 | D:/AutoCAD 2027/ | Professional CAD | ❌ |
| blueCFD (OpenFOAM) | Apps/blueCFD/ | CFD simulation | msys2 |
| BRL-CAD | Apps/BRL-CAD/ | Solid modeling | ❌ |
| Cura (UltiMaker) | Apps/Cura/ | 3D slicer | ✅ full Python API |
| Elmer + MPI | Apps/Elmer/, Apps/ElmerMPI/ | FEM multiphysics | Fortran |
| Gmsh 4.13 | Apps/Gmsh/ | Mesh generator | ✅ onelab.py |
| Inkscape | Apps/Inkscape/ | Vector graphics | ✅ Python 3.12 |
| MeshLab | Apps/MeshLab/ | Mesh processing | ❌ |
| Netgen | Apps/NetgenNGSuite/ | Mesh generator | init.py |
| OpenModelica | Apps/OpenModelica/ | System modeling | ❌ |
| Pandoc 3.10 | Apps/Pandoc/ | Document converter | ❌ |
| ParaView | Apps/ParaView/ | Scientific viz | ✅ full Python |
| PrusaSlicer | Apps/PrusaSlicer/ | 3D slicer | ❌ |
| QCAD | Apps/QCAD/ | 2D CAD | ❌ |
| SolveSpace | Apps/SolveSpace/ | Parametric 3D CAD | ❌ |
| Tectonic | Apps/Tectonic/ | LaTeX engine | ❌ |
| 嘉立创EDA Pro | D:/lceda-pro/ | PCB design (Electron) | ❌ |

## Python Virtual Environments

| venv | Tools | Status |
|------|-------|--------|
| cad-automation | ezdxf, flask, dash, jupyter | Ready |
| eeg-research | coverage, httpx, jupyter | Ready |
| industrial-vision-geometry | ezdxf, meshio, imageio | Ready |

## MCP Servers (all under D:/IndustrialDesignTools/mcp/)

| Server | Docs | Tests | Status |
|--------|------|-------|--------|
| ahujasid_blender_mcp | README 10KB | ❌ | Working |
| official_blender_mcp | README 3KB | ✅ pytest | Working |
| patrykiti_blender_ai_mcp | 110KB+ docs | ✅ E2E + unit | **Production-ready** |

## Actionable Paths

1. **kicad-mcp-revival**: Use kicad-cli (safe) + pcbnew API (board manipulation)
2. **freecad-mcp**: Use freecadcmd.exe (headless) + FreeCAD Python API
3. **blender-mcp**: 3 servers already installed — document, integrate, contribute
4. **platformio-mcp**: Wrap PlatformIO CLI for embedded firmware automation
5. **openscad-mcp**: Scriptable CAD with CLI + Python helpers
