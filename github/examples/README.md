# Discovery API Examples

Working code examples for Ansys Discovery / SpaceClaim scripting.

---

## 📁 Examples

| Example | Description | Difficulty |
|---------|-------------|------------|
| [example_l_bracket.py](example_l_bracket.py) | Create L-shaped bracket with fillet | ⭐ Beginner |
| [example_bolt_holes.py](example_bolt_holes.py) | Bolt hole pattern with subtraction | ⭐⭐ Intermediate |
| [example_simulation.py](example_simulation.py) | Full workflow: geometry → FEA → results | ⭐⭐⭐ Advanced |

---

## 🚀 How to Run

### Method 1: Script Editor (Recommended)

1. Open **Ansys Discovery**
2. Go to **File → Script Editor**
3. Click **Open** and select example file
4. Click **Run** button
5. Check console output

### Method 2: Copy-Paste

1. Open example file in text editor
2. Copy all code
3. Paste in Discovery Script Editor
4. Click **Run**

---

## 📋 Prerequisites

- **Ansys Discovery 2024 R2** (or compatible version)
- **SpaceClaim API V24**
- Windows 10/11

---

## 💡 Tips

### Modifying Examples

All examples use parameters at the top:

```python
# PARAMETERS
BEAM_LENGTH = 200    # mm - Change this!
BEAM_WIDTH = 40      # mm
APPLIED_FORCE = 1000 # N
```

Modify these values to experiment.

### Units

⚠️ **CRITICAL:** Discovery uses SI units (meters, Pa, N)

All examples include `MM()` helper:
```python
def MM(val):
    """Convert millimeters to meters"""
    return val / 1000.0

# Usage:
width = MM(100)  # 100mm = 0.1m
```

### Debugging

Enable Debug mode in Script Editor:
- Set breakpoints (click line number)
- Step through code
- Inspect variables

---

## 📚 Learning Path

1. **Start with:** `example_l_bracket.py`
   - Learn basic geometry creation
   - Understand BlockBody and frames
   - Practice boolean operations

2. **Next:** `example_bolt_holes.py`
   - Work with arrays/patterns
   - Use CylinderBody
   - Multiple boolean subtractions

3. **Advanced:** `example_simulation.py`
   - Complete FEA workflow
   - Boundary conditions
   - Results export

---

## 🔧 Troubleshooting

### "Module not found"
→ Check Discovery version (needs 2024 R2 or compatible)

### "Wrong units" / Huge geometry
→ Remember: API uses METERS! Use MM() helper

### Script runs but no geometry
→ Check if existing bodies were deleted (script includes cleanup)

### Simulation fails
→ Ensure material assigned and BC applied correctly

---

## 📖 Full API Reference

For complete documentation, see [discovery_api_agent.md](../discovery_api_agent.md)

---

## 🤝 Contributing

Have a useful example? Please contribute!

See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

---

**Happy Scripting! 🚀**
