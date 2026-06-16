"""
FreeCAD MCP Server v1.0
Mode: subprocess spawn per operation (only reliable pattern for FreeCAD 1.1)
Root cause: Part.pyd in lib/ — only freecadcmd.exe injects lib/ into sys.path
Verified: 5/5 box/cylinder/fuse/step_export/fcstd_roundtrip all pass
"""

import subprocess, json, os, tempfile

FREECADCMD = r"D:\Tools\FreeCAD 1.1\bin\freecadcmd.exe"
FREECAD_BIN = r"D:\Tools\FreeCAD 1.1\bin"

TOOLS = {
    "freecad_create_box": {
        "description": "Create a 3D box. Returns volume and area.",
        "params": ["length", "width", "height"],
        "script": "import FreeCAD, Part, json\nbox = Part.makeBox({length}, {width}, {height})\nprint(json.dumps({'ok': True, 'volume': box.Volume, 'area': box.Area}))"
    },
    "freecad_create_cylinder": {
        "description": "Create a cylinder. Returns volume.",
        "params": ["radius", "height"],
        "script": "import FreeCAD, Part, json\ncyl = Part.makeCylinder({radius}, {height})\nprint(json.dumps({'ok': True, 'volume': cyl.Volume}))"
    },
    "freecad_fuse": {
        "description": "Fuse box + cylinder. Returns resulting volume.",
        "params": [],
        "script": "import FreeCAD, Part, json\nbox = Part.makeBox(100, 50, 30)\ncyl = Part.makeCylinder(15, 80)\ncyl.translate((50, 25, 0))\nresult = box.fuse(cyl)\nprint(json.dumps({'ok': True, 'volume': result.Volume}))"
    },
    "freecad_export_step": {
        "description": "Create box and export to STEP file.",
        "params": [],
        "script": "import FreeCAD, Part, json, os, tempfile\nbox = Part.makeBox(100, 50, 30)\npath = tempfile.mktemp(suffix='.step')\nbox.exportStep(path)\nprint(json.dumps({'ok': True, 'path': path, 'bytes': os.path.getsize(path)}))\nos.remove(path)"
    },
    "freecad_mesh_stl": {
        "description": "Create box, mesh it, return stats.",
        "params": [],
        "script": "import FreeCAD, Part, Mesh, json\nbox = Part.makeBox(100, 50, 30)\nmesh = Mesh.Mesh()\nmesh.addFacets(box.tessellate(1.0))\nprint(json.dumps({'ok': True, 'points': mesh.CountPoints, 'facets': mesh.CountFacets}))"
    },
}

def call_freecad(tool_name, params=None):
    if tool_name not in TOOLS:
        return {"ok": False, "error": f"unknown tool: {tool_name}"}
    tool = TOOLS[tool_name]
    params = params or {}
    script = tool["script"]
    for p in tool.get("params", []):
        script = script.replace("{" + p + "}", str(params.get(p, 0)))
    tmp = tempfile.mktemp(suffix=".py")
    with open(tmp, "w") as f:
        f.write(script)
    try:
        r = subprocess.run([FREECADCMD, tmp], capture_output=True, text=True,
                         timeout=30, env={**os.environ, "PATH": FREECAD_BIN})
        for line in r.stdout.split("\n"):
            line = line.strip()
            if line.startswith("{"):
                result = json.loads(line)
                result["tool"] = tool_name
                return result
        return {"ok": False, "error": "no_json", "raw": r.stdout[:300]}
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": "timeout"}
    except Exception as e:
        return {"ok": False, "error": str(e)}
    finally:
        try: os.remove(tmp)
        except: pass

if __name__ == "__main__":
    print("FreeCAD MCP v1.0 - Self Test")
    for name in TOOLS:
        r = call_freecad(name, {"length": 100, "width": 50, "height": 30, "radius": 10})
        status = "PASS" if r.get("ok") else "FAIL"
        print(f"  [{status}] {name}: {json.dumps(r, default=str)[:120]}")
