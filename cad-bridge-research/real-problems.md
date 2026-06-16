# Real-World Integration Problems Found

## FreeCAD 1.1

### Problem 1: Module Import Hell
- `Part.pyd` lives in `lib/`, NOT `bin/Lib/site-packages/`
- `import Part` works in `freecadcmd.exe` context ✅
- `import Part` from `python.exe` directly FAILS ❌
- **Root cause**: FreeCAD initialization C++ code in freecadcmd.exe sets up the module search paths that python.exe doesn't

### Problem 2: Double Execution
- `freecadcmd.exe script.py` runs the script TWICE
- Output appears duplicated
- **Impact**: Any side effects (file writes, API calls) happen twice

### Problem 3: Document Lifecycle Race Condition
- `FreeCAD.closeDocument("X")` followed by script exit causes `[Unknown document 'X']`
- FreeCAD C++ core tries to clean up documents after Python already closed them
- **Workaround**: Don't close documents explicitly in scripts — let freecadcmd exit handle cleanup

### Problem 4: Must Use subprocess, Not import
- For MCP server: spawn `freecadcmd.exe` per operation, not `import FreeCAD` once
- Each invocation = ~1-2 second startup overhead
- **Strategy**: Batch operations into single freecadcmd calls, or keep a persistent freecadcmd process

## KiCad 10.0

### Problem 1: DRC Performance
- Small board (86KB): DRC completes in <5 seconds
- Large board (vme-wren, ~500KB): DRC **times out (>30s)**
- **Root cause**: Complex boards with many nets/zones cause exponential DRC computation
- **Workaround**: Use `--format json` + `--severity-error` to reduce output overhead

### Problem 2: CLI Needs QT But Works Headless
- kicad-cli links against Qt but works with `QT_QPA_PLATFORM=offscreen`
- No display needed ✅

### Problem 3: Other Modules Have NO Python Wrapper
- eeschema, cvpcb, gerbview, etc. can ONLY be used via kicad-cli subprocess
- Direct DLL loading fails — no Python bindings exist

## Blender 5.1.2

### Problem 1: MCP Server Registration on Every Launch
- Blender MCP addon registers on startup, unregisters on exit
- `blender --background` starts the MCP RPC server but **immediately exits** in background mode
- **Root cause**: Blender exits after script completes, killing the RPC server
- **Workaround**: Use `blender` in non-background mode with a persistent script, or use the MCP server as a standalone process

### Problem 2: 3 MCP Servers, Which One Works?
- ahujasid: RPC on 0.0.0.0:8765 ✅ (but exits with blender)
- official: Tests exist, needs addon installation
- patrykiti: Most documented (110KB docs), production-ready
- **Need to test**: Which one stays running reliably?

## General Cross-Tool Issues

### Path/Dependency Hell
- Each tool bundles its own Python (KiCad 3.11, FreeCAD 3.11, Blender 3.13)
- Cross-tool Python imports FAIL
- Must use each tool's own interpreter

### Subprocess is the Only Safe Pattern
- For ALL tools: spawn subprocess per operation
- Do NOT try to import modules across tool boundaries
- Accept 1-2 second startup overhead as the cost of reliability
