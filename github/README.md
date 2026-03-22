# Discovery API Reference

> **Complete API reference for Ansys Discovery / SpaceClaim scripting (Python)**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Discovery Version](https://img.shields.io/badge/Discovery-2024%20R2%20(V24)-blue.svg)](https://www.ansys.com/products/3d-design/ansys-discovery)
[![API Version](https://img.shields.io/badge/API-SpaceClaim%20V24-green.svg)](https://spaceclaim.com)

**The most comprehensive Discovery/SpaceClaim Python API documentation available.**

Covers geometry creation, simulation setup, results export, and best practices for automating Ansys Discovery workflows.

---

## 📚 What's Inside

This repository contains a complete API reference guide for **Ansys Discovery 2024 R2** (SpaceClaim API V24):

- ✅ **Complete API Reference** - All essential classes, methods, and properties
- ✅ **Working Code Examples** - 15+ tested examples ready to use
- ✅ **Best Practices** - SI units, error handling, body references
- ✅ **Simulation Workflow** - Material assignment, boundary conditions, solving
- ✅ **Results Export** - CSV export for stress, displacement, mass
- ✅ **Troubleshooting Guide** - Common errors and solutions
- ✅ **Version Compatibility** - V23 → V24 → V252 migration guide
- ✅ **Quick Reference Card** - One-page API cheat sheet

---

## 🚀 Quick Start

### 1. Read the Documentation

📖 **[View the Complete API Reference](discovery_api_agent.md)**

### 2. Try an Example

```python
# Example: Create a simple L-bracket in Discovery
from SpaceClaim.Api.V24 import *

# Create base plate (100x80x3mm)
origin = Point.Create(0, 0, 0)
frame_base = Frame.Create(origin, Direction.DirX, Direction.DirY)
base = BlockBody.Create(frame_base, 0.1, 0.08, 0.003)

# Create vertical plate (100x60x3mm)
frame_vert = Frame.Create(origin, Direction.DirX, Direction.DirZ)
vertical = BlockBody.Create(frame_vert, 0.1, 0.06, 0.003)

# Union the two plates
all_bodies = GetRootPart().GetBodies()
Combine.Execute(
    Selection.Create(all_bodies[0]),
    Selection.Create(all_bodies[1]),
    CombineMode.Unite
)

print("L-bracket created!")
```

### 3. Run in Discovery

1. Open **Ansys Discovery**
2. Go to **File → Script Editor**
3. Paste the code
4. Click **Run**

More examples in the [`examples/`](examples/) folder.

---

## 📖 Documentation Structure

| Section | Description |
|---------|-------------|
| **API Overview** | Import structure, version compatibility |
| **Core Namespaces** | Point, Direction, Frame, Vector |
| **Geometry Creation** | BlockBody, CylinderBody, Sketch+Extrude |
| **Selection System** | Bodies, faces, edges selection |
| **Boolean Operations** | Union, subtract, intersect |
| **Edge Operations** | Fillet, chamfer |
| **Simulation Setup** | Material, BC, mesh, solve |
| **Results Export** | Von Mises, displacement, CSV |
| **Best Practices** | Units, error handling, references |
| **Common Patterns** | L-bracket, bolt holes, full workflow |
| **Troubleshooting** | Error messages and fixes |
| **Version Migration** | V23 → V24 → V252 changes |

---

## 💡 Key Features

### SI Units (Critical!)

⚠️ **Discovery API uses METERS internally:**

```python
# ✅ CORRECT
width = 0.100      # 100mm
force = 2000       # 2000N
stress = 355e6     # 355 MPa

# ❌ WRONG
width = 100        # This is 100 METERS!
```

### BlockBody - Two Methods

**Frame-based (recommended for complex geometry):**
```python
frame = Frame.Create(origin, Direction.DirX, Direction.DirY)
box = BlockBody.Create(frame, width, length, height)
```

**Two-point (simpler for axis-aligned boxes):**
```python
box = BlockBody.Create(
    Point.Create(x1, y1, z1),
    Point.Create(x2, y2, z2),
    ExtrudeType.ForceAdd
)
```

### Full Simulation Example

```python
# 1. Material
MaterialHelper.AssignMaterial(body_sel, "Structural Steel")

# 2. Study
study = Study.Create()
study.MeshDensity = 2  # medium

# 3. Fixed support
bc_fixed = FixedSupport.Create(study, face_sel)

# 4. Force load
force = ForceLoad.Create(study, load_face_sel)
force.Magnitude = 2000.0
force.Direction = -Direction.DirY

# 5. Solve
study.Solve()

# 6. Export results
stress = study.GetResult(ResultType.VonMisesStress)
print(f"Max stress: {stress.Maximum/1e6:.1f} MPa")
```

---

## 📁 Repository Contents

```
discovery-api-reference/
├── README.md                    # This file
├── discovery_api_agent.md       # Complete API reference ⭐
├── examples/                    # Working code examples
│   ├── example_l_bracket.py
│   ├── example_bolt_holes.py
│   ├── example_simulation.py
│   └── example_gusset.py
├── LICENSE                      # MIT License
├── CONTRIBUTING.md              # How to contribute
└── CHANGELOG.md                 # Version history
```

---

## 🎯 Use Cases

This API reference is perfect for:

- ✅ **Design Automation** - Automate repetitive CAD tasks
- ✅ **Parametric Modeling** - Generate geometry from parameters
- ✅ **Batch Simulations** - Run multiple FEA analyses
- ✅ **Optimization Loops** - Iterative design improvement
- ✅ **Custom Tools** - Build Discovery extensions
- ✅ **Learning** - Understand Discovery scripting API

---

## 🔧 Compatibility

| Discovery Version | API Version | Status |
|-------------------|-------------|--------|
| 2024 R2 | V24 | ✅ **Fully supported** |
| 2024 R1 | V24 | ✅ Supported |
| 2023 R2 | V23 | ✅ Compatible (minor changes) |
| 2025 R2 | V252 | ⚠️ Breaking changes (see migration guide) |

**Target Version:** Discovery 2024 R2 (SpaceClaim API V24)

---

## 📚 Additional Resources

- 📖 [Official Ansys Discovery Documentation](https://ansyshelp.ansys.com/)
- 💬 [Ansys Learning Forum](https://forum.ansys.com/)
- 🎓 [Ansys Innovation Courses](https://courses.ansys.com/)
- 🔧 [SpaceClaim Scripting Guide](https://spaceclaim.com/en/support/scripting)

---

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Ways to contribute:**
- 🐛 Report bugs or API errors
- 📝 Suggest documentation improvements
- 💡 Share your code examples
- ✨ Add new API methods or features
- 🌍 Translate documentation

---

## 📄 License

This documentation is released under the **MIT License**. See [LICENSE](LICENSE) for details.

**Note:** This is community documentation. Ansys, Discovery, and SpaceClaim are trademarks of ANSYS, Inc.

---

## ⚠️ Disclaimer

This documentation is provided as-is, without warranty. Always test scripts in a non-production environment first.

The API reference is based on:
- Ansys Discovery 2024 R2 official documentation
- SpaceClaim API Class Library (V24)
- Extensive testing and validation

---

## 🌟 Star This Repo

If you find this documentation helpful, please ⭐ **star this repository** to help others discover it!

---

## 📞 Support

- **Issues:** Use [GitHub Issues](../../issues) for bugs or questions
- **Discussions:** Use [GitHub Discussions](../../discussions) for general questions
- **Email:** For private inquiries (see profile)

---

## 🙏 Acknowledgments

- Ansys Inc. for Discovery and SpaceClaim
- The Discovery user community
- Contributors and testers

---

**Made with ❤️ for the Discovery community**

*Last updated: 2024-03-22*

---

## Quick Links

- 📖 **[Main API Reference](discovery_api_agent.md)** ← Start here!
- 💻 **[Code Examples](examples/)**
- 🐛 **[Report Issues](../../issues)**
- 💬 **[Discussions](../../discussions)**
- 📝 **[Contributing](CONTRIBUTING.md)**

---

### Related Projects

Looking for complete design automation? Check out:
- [Bracket Design Agent](https://github.com/yourusername/bracket-agent) - Automated bracket design with FEA optimization
- [Discovery Automation Tools](https://github.com/yourusername/discovery-tools) - Collection of useful Discovery scripts

---

**Happy Scripting with Discovery! 🚀**
