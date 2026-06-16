# Blender MCP Real-World Status

## Three MCP Servers Installed

### 1. ahujasid_blender_mcp
- RPC server on 0.0.0.0:8765
- 53KB server.py (substantial)
- Starts with Blender, exits with Blender
- **Issue**: No persistence — server dies when Blender exits

### 2. official_blender_mcp  
- Has test suite (pytest)
- Chat client included
- **Not yet tested**

### 3. patrykiti_blender_ai_mcp
- Most documented (110KB+ docs)
- Vision harness, E2E tests, router system
- 48KB README
- Python 3.12 venv ready
- **Most promising for production use**

## Critical Test Needed
```bash
# Test: Can MCP server survive Blender restart?
blender --background --python-expr "import bpy; bpy.ops.wm.read_homefile()" 
# Does the MCP addon auto-start? Does the port stay open?
```
