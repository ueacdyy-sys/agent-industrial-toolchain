# FreeCAD 1.1 Python API Quick Reference

## Headless Operation
```bash
D:/Tools/FreeCAD 1.1/bin/freecadcmd.exe script.py
```

## Key Modules
```python
import FreeCAD
import Part        # 112 names — solid modeling
import Mesh        # 26 names — mesh operations
import Sketcher    # 14 names — 2D sketching
import Draft       # 230 names — 2D drafting tools
import Fem         # 51 names — finite element analysis
import CAM         # 7 names — CNC toolpath generation
import BIM         # 7 names — building information modeling

# Basic operations
box = Part.makeBox(10, 20, 30)  # width, length, height
print(box.Volume, box.Area)

# Save
box.exportStep("output.step")
```

## MCP Integration
- Use `freecadcmd.exe` for headless (no GUI dependency)
- Python API accessible via bundled python.exe
- Key DLLs in bin/: FreeCADApp.dll, FreeCADGui.dll, FreeCADBase.dll
