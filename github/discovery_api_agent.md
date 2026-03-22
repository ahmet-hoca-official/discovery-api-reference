# Ansys Discovery / SpaceClaim API Reference for Bracket Design Agent

**Version:** Ansys Discovery 2024 R2 (v242)
**API:** SpaceClaim.Api.V24
**Language:** IronPython 2.7
**Date:** 2024-03-22

---

## 📚 Table of Contents

1. [API Overview](#api-overview)
2. [Core Namespaces](#core-namespaces)
3. [Geometry Creation](#geometry-creation)
4. [Selection System](#selection-system)
5. [Boolean Operations](#boolean-operations)
6. [Simulation Setup](#simulation-setup)
7. [Results Export](#results-export)
8. [Best Practices](#best-practices)
9. [Common Patterns](#common-patterns)
10. [Troubleshooting](#troubleshooting)

---

## API Overview

### Import Structure

```python
# Standard IronPython script header
import math
import System
from SpaceClaim.Api.V24 import *

# Namespace hierarchy:
# SpaceClaim.Api.V24
#   ├── Point
#   ├── Direction
#   ├── Frame
#   ├── Vector
#   ├── Plane
#   ├── BlockBody
#   ├── CylinderBody
#   ├── Selection
#   ├── Combine
#   ├── ConstantRoundEdges
#   ├── Study (Discovery simulation)
#   ├── FixedSupport
#   ├── ForceLoad
#   └── MaterialHelper
```

### Version Compatibility

| Ansys Version | API Version | SpaceClaim API | Notes |
|---------------|-------------|----------------|-------|
| 2025 R2 | v252 | V252 | Latest - BlockBody deprecated |
| 2025 R1 | v251 | V251 | - |
| 2024 R2 | v242 | V24 | **Our target version** |
| 2024 R1 | v241 | V24 | - |
| 2023 R2 | v232 | V23 | - |
| 2023 R1 | v231 | V23 | - |

**IMPORTANT NOTES:**
- API version (`V24`) is separate from product version (`v242`)
- **This documentation targets Discovery 2024 R2 (V24 API)**
- V252 (2025 R2) has API changes - `BlockBody` class deprecated
- Always check your Discovery installation version before using scripts
- For V252, use alternative geometry creation methods (see below)

---

## Core Namespaces

### 1. Geometry Primitives

#### Point

```python
# Create a 3D point
Point.Create(x, y, z) -> Point

# Parameters:
#   x, y, z: float (meters in SI units)

# Example:
origin = Point.Create(0.0, 0.0, 0.0)
point1 = Point.Create(0.1, 0.05, 0.02)  # 100mm, 50mm, 20mm
```

**Properties:**
- `X`, `Y`, `Z`: Coordinate values
- `Vector`: Position as Vector object

#### Direction

```python
# Create a direction vector
Direction.Create(x, y, z) -> Direction

# Standard directions:
Direction.DirX  # (1, 0, 0)
Direction.DirY  # (0, 1, 0)
Direction.DirZ  # (0, 0, 1)

# Custom direction:
dir_custom = Direction.Create(1, 1, 0)  # 45° in XY plane
```

**Methods:**
- `Reverse()`: Opposite direction
- `Normalize()`: Unit vector

#### Frame

```python
# Create a coordinate frame (local coordinate system)
Frame.Create(origin, dir_x, dir_y) -> Frame

# Parameters:
#   origin: Point - Frame origin
#   dir_x: Direction - X-axis direction
#   dir_y: Direction - Y-axis direction
#   (Z-axis computed automatically via cross product)

# Example:
origin = Point.Create(0, 0, 0)
frame_xy = Frame.Create(origin, Direction.DirX, Direction.DirY)

# Rotated frame (45° around Z)
dir_x_rot = Direction.Create(math.cos(math.radians(45)),
                              math.sin(math.radians(45)), 0)
dir_y_rot = Direction.Create(-math.sin(math.radians(45)),
                               math.cos(math.radians(45)), 0)
frame_rot = Frame.Create(origin, dir_x_rot, dir_y_rot)
```

#### Vector

```python
# Create a vector
Vector.Create(x, y, z) -> Vector

# Operations:
v1 = Vector.Create(1, 0, 0)
v2 = Vector.Create(0, 1, 0)

# Magnitude:
length = v1.Magnitude  # -> 1.0

# Dot product:
dot = Vector.Dot(v1, v2)  # -> 0.0

# Cross product:
cross = Vector.Cross(v1, v2)  # -> Vector(0, 0, 1)
```

---

## Geometry Creation

### BlockBody (Box/Rectangular Prism)

```python
BlockBody.Create(frame, width, length, height) -> DesignBody

# Parameters:
#   frame: Frame - Coordinate system (width along X, length along Y, height along Z)
#   width: float - Dimension along frame X-axis [m]
#   length: float - Dimension along frame Y-axis [m]
#   height: float - Dimension along frame Z-axis [m]

# Returns:
#   DesignBody - Created solid body

# Example: Create a 100x50x3mm plate
origin = Point.Create(0, 0, 0)
frame = Frame.Create(origin, Direction.DirX, Direction.DirY)
plate = BlockBody.Create(frame, 0.1, 0.05, 0.003)
```

**Important Notes:**
- Dimensions are in METERS (SI units)
- Frame defines orientation and position
- Body is centered at frame origin
- Always store result if you need to reference it later

### CylinderBody

```python
CylinderBody.Create(origin, direction, radius, height) -> DesignBody

# Parameters:
#   origin: Point - Center of base circle
#   direction: Direction - Cylinder axis direction
#   radius: float - Cylinder radius [m]
#   height: float - Cylinder height [m]

# Example: Vertical cylinder (bolt hole)
origin = Point.Create(0.05, 0.05, 0)
cylinder = CylinderBody.Create(
    origin,
    Direction.DirZ,  # Vertical
    0.004,           # 8mm diameter (4mm radius)
    0.010            # 10mm height
)
```

### SphereBody

```python
SphereBody.Create(origin, radius) -> DesignBody

# Parameters:
#   origin: Point - Sphere center
#   radius: float - Sphere radius [m]
```

### Advanced: Sketch + Extrude

```python
# Create a sketch plane
plane = Plane.Create(Frame.Create(origin, Direction.DirX, Direction.DirY))
ViewHelper.SetSketchPlane(plane)

# Create sketch geometry (lines, arcs, circles)
p1 = Point2D.Create(0, 0)
p2 = Point2D.Create(0.1, 0)
p3 = Point2D.Create(0.1, 0.05)
p4 = Point2D.Create(0, 0.05)

SketchLine.Create(p1, p2)
SketchLine.Create(p2, p3)
SketchLine.Create(p3, p4)
SketchLine.Create(p4, p1)

# Extrude the sketch
mode = InteractionMode.Solid
result = Pull.Execute(
    Selection.CreateByNames('Sketch'),
    0.003,  # Extrusion distance [m]
    PullOptions()
)
```

---

## Selection System

### Selection.Create()

```python
# Selection is fundamental to SpaceClaim API
# Used for: picking objects, applying operations, filtering

# Select a single body:
body = GetRootPart().GetBodies()[0]
sel = Selection.Create(body)

# Select multiple bodies:
bodies = GetRootPart().GetBodies()
sel = Selection.Create(bodies)

# Select faces:
face = body.Faces[0]
sel = Selection.Create(face)

# Select edges:
edges = [e for e in body.Edges if _is_sharp(e)]
sel = Selection.Create(edges)

# Select by name:
sel = Selection.CreateByNames('Body1')
```

### GetRootPart()

```python
# Access the root part (document container)
root = GetRootPart()

# Get all bodies in document:
all_bodies = root.GetBodies()

# Get all parts:
all_parts = root.GetDescendants[IPart]()

# Filter by type:
for body in all_bodies:
    if body.Shape:
        print(f"Body: {body.Name}, Volume: {body.Shape.Volume}")
```

### Body Properties

```python
body = GetRootPart().GetBodies()[0]

# Geometry properties:
volume = body.Shape.Volume          # [m³]
mass = body.Mass                    # [kg] (if material assigned)
bbox = body.Shape.GetBoundingBox()  # BoundingBox object

# Bounding box:
min_point = bbox.MinCorner  # Point
max_point = bbox.MaxCorner  # Point
center = bbox.Center        # Point
size = bbox.Size            # Vector (width, length, height)

# Faces, edges, vertices:
faces = body.Faces          # ICollection<Face>
edges = body.Edges          # ICollection<Edge>
vertices = body.Vertices    # ICollection<Vertex>

# Material:
if body.Material:
    mat_name = body.Material.Name
```

---

## Boolean Operations

### Combine.Execute() - Boolean Union, Subtract, Intersect

```python
Combine.Execute(target_selection, tool_selection, mode) -> CommandResult

# Parameters:
#   target_selection: Selection - Primary body
#   tool_selection: Selection - Secondary body
#   mode: CombineMode
#     - CombineMode.Unite (Union, A ∪ B)
#     - CombineMode.Subtract (Difference, A - B)
#     - CombineMode.Intersect (Intersection, A ∩ B)

# Example 1: Union (merge two bodies)
body1 = GetRootPart().GetBodies()[0]
body2 = GetRootPart().GetBodies()[1]

result = Combine.Execute(
    Selection.Create(body1),
    Selection.Create(body2),
    CombineMode.Unite
)

# Example 2: Subtract (cutout hole)
main_body = GetRootPart().GetBodies()[0]
hole_cylinder = GetRootPart().GetBodies()[1]  # Created earlier

result = Combine.Execute(
    Selection.Create(main_body),
    Selection.Create(hole_cylinder),
    CombineMode.Subtract
)

# Example 3: Multiple unions (loop)
all_bodies = GetRootPart().GetBodies()
if len(all_bodies) > 1:
    target = all_bodies[0]
    for tool_body in all_bodies[1:]:
        Combine.Execute(
            Selection.Create(target),
            Selection.Create(tool_body),
            CombineMode.Unite
        )
        # Update target (may have changed after union)
        all_bodies = GetRootPart().GetBodies()
        if len(all_bodies) > 0:
            target = all_bodies[0]
```

**Important Notes:**
- Target body is modified in-place
- Tool body is consumed (deleted after operation)
- Always update body references after Combine
- Check if operation succeeded: `result.Success`

---

## Edge Operations

### ConstantRoundEdges.Execute() - Fillet/Round

```python
ConstantRoundEdges.Execute(selection, radius, options, is_rolling_ball) -> CommandResult

# Parameters:
#   selection: Selection - Edges to fillet
#   radius: float - Fillet radius [m]
#   options: RoundEdgesOptions (or None)
#   is_rolling_ball: bool - Use rolling ball algorithm

# Example: Fillet all sharp edges
body = GetRootPart().GetBodies()[0]
sharp_edges = []

for edge in body.Edges:
    # Check if edge is sharp (angle > threshold)
    # Note: Proper implementation requires face normal analysis
    sharp_edges.append(edge)

if sharp_edges:
    result = ConstantRoundEdges.Execute(
        Selection.Create(sharp_edges),
        0.002,  # 2mm radius
        None,
        False
    )
```

### ConstantChamferEdges.Execute() - Chamfer

```python
ConstantChamferEdges.Execute(selection, distance, options) -> CommandResult

# Parameters:
#   selection: Selection - Edges to chamfer
#   distance: float - Chamfer distance [m]
#   options: ChamferEdgesOptions (or None)

# Example:
edge_sel = Selection.Create(body.Edges[0])
ConstantChamferEdges.Execute(edge_sel, 0.001, None)  # 1mm chamfer
```

---

## Simulation Setup (Discovery Live Physics)

### Study Management

```python
# Create or get simulation study
study = Study.GetActive()  # Get existing study
if study is None:
    study = Study.Create()  # Create new study

# Study properties:
study.Name = "Structural Analysis 1"
study.MeshDensity = 2  # 1=fine, 2=medium, 3=coarse
```

### Material Assignment

```python
# Assign material from Discovery library
MaterialHelper.AssignMaterial(selection, material_name)

# Parameters:
#   selection: Selection - Bodies to assign material
#   material_name: string - Name from Discovery material library

# Available materials (common):
# - "Structural Steel"
# - "Aluminum Alloy"
# - "Stainless Steel"
# - "Titanium Alloy"
# - "Concrete"
# - "Custom..." (user-defined)

# Example:
all_bodies = GetRootPart().GetBodies()
for body in all_bodies:
    body_sel = Selection.Create(body)
    MaterialHelper.AssignMaterial(body_sel, "Structural Steel")
```

**Material Database Notes:**
- Discovery uses its own material library
- Material names are version-dependent
- Custom materials can be defined in Discovery UI first
- Our config.py materials map to Discovery names:
  - S235JR, S355JR → "Structural Steel"
  - Al6061-T6, Al5083 → "Aluminum Alloy"

### Boundary Conditions

#### Fixed Support

```python
FixedSupport.Create(study, face_selection) -> FixedSupport

# Parameters:
#   study: Study - Active simulation study
#   face_selection: Selection - Faces to fix (all DOF constrained)

# Returns:
#   FixedSupport object

# Example: Fix the bottom face
study = Study.GetActive()
bottom_faces = []

for body in GetRootPart().GetBodies():
    for face in body.Faces:
        bbox = face.Shape.GetBoundingBox()
        if bbox.Center.Z < 0.001:  # Z ≈ 0 (bottom)
            bottom_faces.append(face)

if bottom_faces:
    fixed_sel = Selection.Create(bottom_faces)
    bc_fixed = FixedSupport.Create(study, fixed_sel)
    bc_fixed.Name = "Fixed_Base"
```

#### Force Load

```python
ForceLoad.Create(study, face_selection) -> ForceLoad

# Parameters:
#   study: Study
#   face_selection: Selection - Faces to apply force

# Force properties:
force_load = ForceLoad.Create(study, face_sel)
force_load.Magnitude = 2000.0  # [N]
force_load.Direction = Direction.DirY  # or -Direction.DirY for negative
force_load.Name = "Applied_Force_Y"

# Direction options:
# - Direction.DirX, DirY, DirZ
# - -Direction.DirX (negative)
# - Direction.Create(x, y, z) (custom)
# - Normal to face (automatic, default)
```

#### Pressure Load

```python
PressureLoad.Create(study, face_selection) -> PressureLoad

pressure = PressureLoad.Create(study, face_sel)
pressure.Magnitude = 100000.0  # [Pa] (100 kPa)
pressure.Name = "Hydrostatic_Pressure"
```

#### Displacement BC

```python
DisplacementBC.Create(study, face_selection) -> DisplacementBC

disp = DisplacementBC.Create(study, face_sel)
disp.X = 0.0    # [m] Constrain X
disp.Y = None   # Free in Y
disp.Z = 0.0    # Constrain Z
disp.Name = "Partial_Constraint"
```

### Mesh Control

```python
# Global mesh density
study.MeshDensity = 2  # 1=fine, 2=medium, 3=coarse

# Local mesh refinement (advanced)
# Note: Discovery Live Physics uses automatic meshing
# For detailed mesh control, use Discovery AIM or Mechanical
```

### Solve

```python
# Run simulation
study.Solve()

# Check solution status:
if study.IsSolved:
    print("Solution converged")
else:
    print("Solution failed or not converged")
```

---

## Results Export

### Result Types

```python
# Available result types:
ResultType.VonMisesStress      # Equivalent stress [Pa]
ResultType.TotalDisplacement   # Total deformation [m]
ResultType.StressX, StressY, StressZ  # Normal stresses
ResultType.StrainX, StrainY, StrainZ  # Normal strains
ResultType.SafetyFactor        # Safety factor
ResultType.Temperature         # Thermal results
```

### Get Results

```python
study = Study.GetActive()

# Get stress results
stress_result = study.GetResult(ResultType.VonMisesStress)

# Result properties:
max_stress = stress_result.Maximum     # [Pa]
min_stress = stress_result.Minimum     # [Pa]
average = stress_result.Average        # [Pa]

# Node-based results:
for node in stress_result.Nodes:
    node_id = node.Id
    position = node.Position  # Point(x, y, z)
    value = node.Value        # Result value at node

    # Access coordinates:
    x = position.X
    y = position.Y
    z = position.Z

    print(f"Node {node_id}: ({x}, {y}, {z}) = {value} Pa")

# Displacement results
disp_result = study.GetResult(ResultType.TotalDisplacement)

for node in disp_result.Nodes:
    total_disp = node.Value      # Total displacement [m]
    disp_vector = node.Vector    # Vector(ux, uy, uz)

    ux = disp_vector.X
    uy = disp_vector.Y
    uz = disp_vector.Z
```

### Export to CSV

```python
import System.IO as IO

results_dir = r"C:\BracketAgent\results"
IO.Directory.CreateDirectory(results_dir)

study = Study.GetActive()

# Export stress data
stress_result = study.GetResult(ResultType.VonMisesStress)
stress_path = IO.Path.Combine(results_dir, 'stress_vonmises.csv')

with open(stress_path, 'w') as f:
    f.write('node_id,x,y,z,vonmises_pa\n')
    for node in stress_result.Nodes:
        pos = node.Position
        val = node.Value
        f.write(f'{node.Id},{pos.X},{pos.Y},{pos.Z},{val}\n')

# Export displacement data
disp_result = study.GetResult(ResultType.TotalDisplacement)
disp_path = IO.Path.Combine(results_dir, 'displacement.csv')

with open(disp_path, 'w') as f:
    f.write('node_id,x,y,z,ux,uy,uz,total\n')
    for node in disp_result.Nodes:
        pos = node.Position
        vec = node.Vector
        tot = node.Value
        f.write(f'{node.Id},{pos.X},{pos.Y},{pos.Z},{vec.X},{vec.Y},{vec.Z},{tot}\n')

# Export summary
summary_path = IO.Path.Combine(results_dir, 'summary.csv')

with open(summary_path, 'w') as f:
    f.write('metric,value\n')
    f.write(f'max_vonmises_pa,{stress_result.Maximum}\n')
    f.write(f'min_vonmises_pa,{stress_result.Minimum}\n')
    f.write(f'max_displacement_m,{disp_result.Maximum}\n')

    # Total mass
    total_mass = 0
    for body in GetRootPart().GetBodies():
        total_mass += body.Mass
    f.write(f'total_mass_kg,{total_mass}\n')

print(f"Results exported to {results_dir}")
```

---

## Best Practices

### 1. Unit System

**CRITICAL:** Discovery/SpaceClaim uses **SI units internally**:

| Quantity | Unit | Conversion |
|----------|------|------------|
| Length | meter (m) | 1mm = 0.001m |
| Force | newton (N) | - |
| Pressure/Stress | pascal (Pa) | 1 MPa = 1e6 Pa |
| Mass | kilogram (kg) | - |
| Angle | radian (rad) | 1° = π/180 rad |

```python
# CORRECT:
width_m = 0.100  # 100mm
force_n = 2000   # 2000N
stress_pa = 355e6  # 355 MPa

# WRONG:
width = 100  # This would be 100 meters!
```

### 2. Error Handling

```python
try:
    # Potentially failing operation
    result = Combine.Execute(sel1, sel2, CombineMode.Unite)

    if not result.Success:
        print("Combine operation failed")
except Exception as e:
    print(f"Error: {e}")
    # Fallback or recovery
```

### 3. Body Reference Updates

```python
# WRONG: Body reference may become invalid after Combine
body1 = GetRootPart().GetBodies()[0]
body2 = GetRootPart().GetBodies()[1]
Combine.Execute(Selection.Create(body1), Selection.Create(body2), CombineMode.Unite)
# body1 and body2 references may now be stale!

# CORRECT: Re-fetch bodies after Combine
all_bodies = GetRootPart().GetBodies()
Combine.Execute(Selection.Create(all_bodies[0]), Selection.Create(all_bodies[1]), CombineMode.Unite)
all_bodies = GetRootPart().GetBodies()  # Refresh
if len(all_bodies) > 0:
    target = all_bodies[0]
```

### 4. Face/Edge Selection

```python
# Select faces by geometric criteria
def find_bottom_faces(tolerance=0.001):
    """Find faces at Z=0 (bottom of model)"""
    bottom_faces = []
    for body in GetRootPart().GetBodies():
        for face in body.Faces:
            bbox = face.Shape.GetBoundingBox()
            if abs(bbox.Center.Z) < tolerance:
                bottom_faces.append(face)
    return bottom_faces

# Select faces by normal direction
def find_faces_with_normal(direction, tolerance=0.1):
    """Find faces with given normal direction"""
    matching_faces = []
    for body in GetRootPart().GetBodies():
        for face in body.Faces:
            # Face normal (may not be well-defined for all face types)
            try:
                normal = face.Shape.Geometry.GetNormal(Point2D.Origin)
                dot_product = Vector.Dot(normal, direction)
                if dot_product > (1.0 - tolerance):
                    matching_faces.append(face)
            except:
                pass
    return matching_faces
```

### 5. Cleanup

```python
# Delete all existing bodies before creating new geometry
bodies = GetRootPart().GetBodies()
for b in bodies:
    Selection.Create(b).Delete()

# Delete temporary bodies after Boolean operations
# (automatically done by Combine for tool body)
```

---

## Common Patterns

### Pattern 1: Create L-Bracket

```python
# Base plate (horizontal, XY plane)
origin_base = Point.Create(0, 0, 0)
frame_base = Frame.Create(origin_base, Direction.DirX, Direction.DirY)
base = BlockBody.Create(frame_base, 0.1, 0.08, 0.003)  # 100x80x3mm

# Vertical plate (XZ plane)
origin_vert = Point.Create(0, 0, 0)
frame_vert = Frame.Create(origin_vert, Direction.DirX, Direction.DirZ)
vertical = BlockBody.Create(frame_vert, 0.1, 0.06, 0.003)  # 100x60x3mm

# Union
all_bodies = GetRootPart().GetBodies()
Combine.Execute(
    Selection.Create(all_bodies[0]),
    Selection.Create(all_bodies[1]),
    CombineMode.Unite
)

# Fillet internal edges
body = GetRootPart().GetBodies()[0]
inner_edges = [e for e in body.Edges]  # Filter sharp edges in practice
ConstantRoundEdges.Execute(
    Selection.Create(inner_edges),
    0.005,  # 5mm fillet
    None, False
)
```

### Pattern 2: Create Bolt Hole Pattern

```python
# Hole positions (in meters)
hole_positions = [
    (0.02, 0.02, 0),
    (0.08, 0.02, 0),
    (0.02, 0.06, 0),
    (0.08, 0.06, 0),
]

# Create holes
for (x, y, z) in hole_positions:
    origin = Point.Create(x, y, z)
    hole = CylinderBody.Create(
        origin,
        Direction.DirZ,
        0.0042,  # M8 clearance hole (8.4mm diameter)
        0.010    # Through thickness
    )

# Subtract holes from main body
main_body = GetRootPart().GetBodies()[0]
for hole in GetRootPart().GetBodies()[1:]:
    Combine.Execute(
        Selection.Create(main_body),
        Selection.Create(hole),
        CombineMode.Subtract
    )
    main_body = GetRootPart().GetBodies()[0]  # Update reference
```

### Pattern 3: Triangular Gusset (Sketch+Extrude)

```python
# Define sketch plane (YZ plane at x=0)
origin = Point.Create(0, 0, 0)
plane = Plane.Create(Frame.Create(origin, Direction.DirY, Direction.DirZ))
ViewHelper.SetSketchPlane(plane)

# Triangle vertices (2D in sketch plane)
p0 = Point2D.Create(0, 0)
p1 = Point2D.Create(0.08, 0)  # 80mm base
p2 = Point2D.Create(0, 0.06)  # 60mm height

# Create sketch lines
SketchLine.Create(p0, p1)
SketchLine.Create(p1, p2)
SketchLine.Create(p2, p0)

# Extrude (create solid)
mode = InteractionMode.Solid
result = Pull.Execute(
    Selection.CreateByNames('Sketch'),
    0.003,  # 3mm thickness
    PullOptions()
)

# Exit sketch mode
ViewHelper.SetViewMode(ViewMode.Solid)
```

### Pattern 4: Full Simulation Workflow

```python
# 1. Material assignment
all_bodies = GetRootPart().GetBodies()
for body in all_bodies:
    MaterialHelper.AssignMaterial(Selection.Create(body), "Structural Steel")

# 2. Create study
study = Study.Create()
study.Name = "Bracket Stress Analysis"
study.MeshDensity = 2

# 3. Fixed support (bottom faces)
fixed_faces = []
for body in all_bodies:
    for face in body.Faces:
        if face.Shape.GetBoundingBox().Center.Z < 0.001:
            fixed_faces.append(face)

if fixed_faces:
    bc_fixed = FixedSupport.Create(study, Selection.Create(fixed_faces))
    bc_fixed.Name = "Fixed_Base"

# 4. Force load (top face)
load_faces = []
for body in all_bodies:
    for face in body.Faces:
        if face.Shape.GetBoundingBox().Center.Z > 0.05:
            load_faces.append(face)

if load_faces:
    force = ForceLoad.Create(study, Selection.Create(load_faces[0]))
    force.Magnitude = 2000.0
    force.Direction = -Direction.DirZ  # Downward
    force.Name = "Applied_Load"

# 5. Solve
study.Solve()

# 6. Export results (see Results Export section)
```

---

## Troubleshooting

### Issue 1: "Name 'XXX' is not defined"

**Cause:** Missing import or incorrect API version

**Solution:**
```python
# Check import:
from SpaceClaim.Api.V24 import *

# Verify API version matches Discovery installation
# Discovery 2024 R2 → V24
# Discovery 2023 R2 → V23
```

### Issue 2: Combine operation creates unexpected geometry

**Cause:** Overlapping or non-manifold geometry

**Solution:**
- Ensure bodies actually intersect (for Unite)
- Check body validity: `body.Shape.IsValid`
- Use `CombineMode.Unite` for merge, not `Intersect`

### Issue 3: Material not found

**Cause:** Material name doesn't exist in Discovery library

**Solution:**
```python
# List available materials (manually in Discovery):
# Tools → Materials → Material Library

# Common safe names:
# - "Structural Steel"
# - "Aluminum Alloy"
# - "Concrete"

# Or create custom material in Discovery first
```

### Issue 4: Simulation doesn't solve

**Causes:**
- No boundary conditions defined
- Over-constrained model
- No material assigned
- Geometry errors

**Debug steps:**
```python
study = Study.GetActive()

# Check if BCs exist:
fixed_supports = study.GetBoundaryConditions(BCType.FixedSupport)
print(f"Fixed supports: {len(fixed_supports)}")

# Check material:
for body in GetRootPart().GetBodies():
    if body.Material is None:
        print(f"Body {body.Name} has no material!")

# Check geometry:
if not body.Shape.IsValid:
    print("Invalid geometry detected")
```

### Issue 5: Results export fails

**Cause:** Study not solved or results not available

**Solution:**
```python
study = Study.GetActive()

if not study.IsSolved:
    print("Study not solved yet. Running solve...")
    study.Solve()

# Check result availability:
try:
    stress_result = study.GetResult(ResultType.VonMisesStress)
    if stress_result is None:
        print("Stress results not available")
except:
    print("Failed to retrieve results")
```

---

## Advanced Topics

### Working with Assemblies

```python
# Get all parts in assembly:
root = GetRootPart()
parts = root.GetDescendants[IPart]()

for part in parts:
    print(f"Part: {part.Name}")
    bodies = part.GetBodies()
    print(f"  Bodies: {len(bodies)}")
```

### Programmatic Named Selections

```python
# Create named selection for later use
faces_to_name = []  # Fill with face objects
named_sel = NamedSelection.Create(Selection.Create(faces_to_name), root)
named_sel.Name = "LoadFaces"

# Use later:
sel = Selection.CreateByNames("LoadFaces")
```

### Custom Coordinate Systems

```python
# Create datum plane
datum_origin = Point.Create(0.05, 0.05, 0)
datum_frame = Frame.Create(datum_origin, Direction.DirX, Direction.DirZ)
datum = DatumPlane.Create(root, "ReferencePlane", datum_frame)

# Use for sketching:
ViewHelper.SetSketchPlane(datum.Plane)
```

---

## Version Migration Guide

### From V23 to V24

Most API calls remain unchanged. Key differences:

```python
# V23:
from SpaceClaim.Api.V23 import *

# V24:
from SpaceClaim.Api.V24 import *

# Material assignment (same):
MaterialHelper.AssignMaterial(sel, material_name)

# Geometry creation (same):
BlockBody.Create(frame, w, l, h)
```

### From V24 to V252 (2025 R2)

**BREAKING CHANGES:**

```python
# V24 (2024 R2):
from SpaceClaim.Api.V24 import *
box = BlockBody.Create(frame, width, length, height)  # DEPRECATED in V252!

# V252 (2025 R2):
from SpaceClaim.Api.V252 import *
# BlockBody class removed - use alternative methods:

# Method 1: Sketch + Extrude
plane = Plane.Create(frame)
ViewHelper.SetSketchPlane(plane)
# Draw rectangle...
result = Pull.Execute(sketch_sel, height, PullOptions())

# Method 2: Import geometry from libraries
# (Check V252 documentation for updated geometry creation API)

# Method 3: Use Design → Sketch → Pull workflow
# (More steps but compatible with V252)
```

**Workaround for Legacy Scripts:**
If you have V24 scripts and need to run on V252 Discovery, manually create geometry in UI first, then apply simulations.

**Recommendation:**
- **For Discovery 2024 R2:** Use V24 API (as documented here)
- **For Discovery 2025 R2:** Migrate to V252 API (requires script updates)
- Always test scripts on target Discovery version before production use

---

## Quick Reference Card

```python
# ════════════════════════════════════════════════════════════
#  DISCOVERY API QUICK REFERENCE
# ════════════════════════════════════════════════════════════

# Import
from SpaceClaim.Api.V24 import *

# Geometry
p = Point.Create(x, y, z)
d = Direction.Create(x, y, z) | Direction.DirX/DirY/DirZ
f = Frame.Create(origin, dir_x, dir_y)
box = BlockBody.Create(frame, w, l, h)
cyl = CylinderBody.Create(origin, direction, radius, height)

# Selection
sel = Selection.Create(object_or_list)
bodies = GetRootPart().GetBodies()

# Boolean
Combine.Execute(sel_target, sel_tool, CombineMode.Unite|Subtract|Intersect)

# Fillet/Chamfer
ConstantRoundEdges.Execute(edge_sel, radius, None, False)

# Simulation
study = Study.Create() | Study.GetActive()
MaterialHelper.AssignMaterial(body_sel, "Structural Steel")
bc = FixedSupport.Create(study, face_sel)
force = ForceLoad.Create(study, face_sel)
force.Magnitude = value_N
study.Solve()

# Results
result = study.GetResult(ResultType.VonMisesStress|TotalDisplacement)
max_val = result.Maximum
for node in result.Nodes:
    pos = node.Position  # Point(x,y,z)
    val = node.Value

# Units: ALWAYS METERS
# 1mm = 0.001m, 1MPa = 1e6 Pa
```

---

## References

1. **Official Documentation:**
   - Ansys Discovery User Guide (Chapter: Scripting)
   - SpaceClaim API Class Library (CHM file)
   - Discovery Scripting Examples (install directory)

2. **Online Resources:**
   - Ansys Learning Hub
   - SpaceClaim Scripting Forum
   - Discovery Community

3. **Example Scripts:**
   - `%INSTALLATION%\SpaceClaim\Examples\Scripts\`
   - Discovery Help → Scripting → Examples

---

**Document Version:** 1.0
**Last Updated:** 2024-03-22
**Maintained by:** Bracket Design Agent Project

---

## Appendix: Material Properties Reference

| Material Name (Discovery) | E [GPa] | ν | ρ [kg/m³] | σ_y [MPa] |
|---------------------------|---------|---|-----------|-----------|
| Structural Steel | 200 | 0.30 | 7850 | 250 |
| Stainless Steel | 193 | 0.31 | 7750 | 207 |
| Aluminum Alloy | 71 | 0.33 | 2770 | 280 |
| Titanium Alloy | 96 | 0.36 | 4620 | 880 |
| Concrete | 30 | 0.18 | 2300 | 30 (comp) |
| Copper Alloy | 110 | 0.34 | 8300 | 280 |

**Note:** These are default Discovery values. Custom materials can be defined with specific properties.

---

*End of Document*
