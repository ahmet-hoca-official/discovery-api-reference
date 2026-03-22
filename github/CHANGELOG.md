# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2024-03-22

### Added
- **Initial Release** - Complete Discovery API V24 reference
- Core API documentation:
  - Geometry creation (Point, Direction, Frame, BlockBody, etc.)
  - Selection system (Bodies, faces, edges)
  - Boolean operations (Union, subtract, intersect)
  - Edge operations (Fillet, chamfer)
  - Simulation setup (Material, BC, solve)
  - Results export (CSV, stress, displacement)
- Best practices guide:
  - SI units (CRITICAL)
  - Error handling patterns
  - Body reference management
  - Face/edge selection techniques
- Working code examples:
  - L-bracket creation
  - Bolt hole pattern
  - Triangular gusset
  - Full simulation workflow
- Troubleshooting guide with common errors
- Version compatibility matrix (V23, V24, V252)
- Quick reference card
- Version migration guide (V24 → V252)

### Documentation
- 85 KB comprehensive API reference
- 15+ tested code examples
- 12 major sections
- 50+ API methods documented

---

## [Planned] - Future Releases

### [1.1.0] - Planned
- [ ] V252 (Discovery 2025 R2) migration examples
- [ ] Advanced geometry: Loft, Sweep, Revolve
- [ ] Thermal simulation examples
- [ ] Modal analysis examples
- [ ] Assembly handling
- [ ] Performance optimization tips

### [1.2.0] - Planned
- [ ] Extension Builder complete guide
- [ ] Custom tool examples
- [ ] Script publishing workflow
- [ ] Advanced selection techniques
- [ ] Parametric design patterns

### [2.0.0] - Planned
- [ ] Discovery 2025 R2 (V252) as primary target
- [ ] Geometry creation without BlockBody
- [ ] Sketch + Extrude workflows
- [ ] Updated all examples for V252

---

## Version Support

| Version | Discovery | API | Status |
|---------|-----------|-----|--------|
| 1.x.x | 2024 R2 | V24 | ✅ Active |
| 2.x.x | 2025 R2 | V252 | 🔄 Planned |

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to propose changes.

---

**Legend:**
- ✅ Complete
- 🔄 In Progress
- 📝 Planned
- ⚠️ Breaking Change
