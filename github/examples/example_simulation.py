# -*- coding: utf-8 -*-
"""
Full Simulation Workflow Example
=================================
Complete example: Geometry → Material → BC → Solve → Export

Creates a cantilever beam and runs structural analysis.

Tested on: Ansys Discovery 2024 R2 (API V24)
"""

import System.IO as IO
from SpaceClaim.Api.V24 import *

# ══════════════════════════════════════════════════════════════════════
#  HELPER FUNCTIONS
# ══════════════════════════════════════════════════════════════════════

def MM(val):
    """Convert millimeters to meters"""
    return val / 1000.0


# ══════════════════════════════════════════════════════════════════════
#  PARAMETERS
# ══════════════════════════════════════════════════════════════════════

# Beam dimensions (mm)
BEAM_LENGTH = 200
BEAM_WIDTH = 40
BEAM_HEIGHT = 20

# Load (N)
APPLIED_FORCE = 1000  # 1000N downward at free end

# Material
MATERIAL_NAME = "Structural Steel"

# Results export path
RESULTS_DIR = r"C:\Temp\DiscoveryResults"


# ══════════════════════════════════════════════════════════════════════
#  1. CREATE GEOMETRY (Cantilever Beam)
# ══════════════════════════════════════════════════════════════════════

# Clean up
bodies = GetRootPart().GetBodies()
for b in bodies:
    Selection.Create(b).Delete()

# Create beam
origin = Point.Create(0, 0, 0)
frame = Frame.Create(origin, Direction.DirX, Direction.DirY)

beam = BlockBody.Create(
    frame,
    MM(BEAM_LENGTH),
    MM(BEAM_WIDTH),
    MM(BEAM_HEIGHT)
)

print(f"Beam created: {BEAM_LENGTH}x{BEAM_WIDTH}x{BEAM_HEIGHT}mm")


# ══════════════════════════════════════════════════════════════════════
#  2. ASSIGN MATERIAL
# ══════════════════════════════════════════════════════════════════════

all_bodies = GetRootPart().GetBodies()

for body in all_bodies:
    body_sel = Selection.Create(body)
    MaterialHelper.AssignMaterial(body_sel, MATERIAL_NAME)

print(f"Material assigned: {MATERIAL_NAME}")


# ══════════════════════════════════════════════════════════════════════
#  3. CREATE SIMULATION STUDY
# ══════════════════════════════════════════════════════════════════════

study = Study.GetActive()
if study is None:
    study = Study.Create()

study.Name = "Cantilever Beam Analysis"
study.MeshDensity = 2  # 1=fine, 2=medium, 3=coarse

print("Study created")


# ══════════════════════════════════════════════════════════════════════
#  4. APPLY FIXED SUPPORT (Left end)
# ══════════════════════════════════════════════════════════════════════

# Find left face (X ≈ -BEAM_LENGTH/2)
fixed_faces = []

for body in all_bodies:
    for face in body.Faces:
        bbox = face.Shape.GetBoundingBox()
        center_x = bbox.Center.X

        # Left face is at X ≈ -L/2
        if abs(center_x - (-MM(BEAM_LENGTH/2))) < MM(1):  # 1mm tolerance
            fixed_faces.append(face)

if fixed_faces:
    fixed_sel = Selection.Create(fixed_faces)
    bc_fixed = FixedSupport.Create(study, fixed_sel)
    bc_fixed.Name = "Fixed_Support"
    print(f"Fixed support applied to {len(fixed_faces)} faces")
else:
    print("WARNING: No fixed faces found!")


# ══════════════════════════════════════════════════════════════════════
#  5. APPLY FORCE LOAD (Right end, downward)
# ══════════════════════════════════════════════════════════════════════

# Find right face (X ≈ +BEAM_LENGTH/2)
load_faces = []

for body in all_bodies:
    for face in body.Faces:
        bbox = face.Shape.GetBoundingBox()
        center_x = bbox.Center.X

        # Right face is at X ≈ +L/2
        if abs(center_x - MM(BEAM_LENGTH/2)) < MM(1):
            load_faces.append(face)

if load_faces:
    load_sel = Selection.Create(load_faces[0])  # Use first matching face
    force = ForceLoad.Create(study, load_sel)
    force.Magnitude = APPLIED_FORCE
    force.Direction = -Direction.DirZ  # Downward
    force.Name = "Applied_Force"
    print(f"Force applied: {APPLIED_FORCE}N downward")
else:
    print("WARNING: No load faces found!")


# ══════════════════════════════════════════════════════════════════════
#  6. SOLVE
# ══════════════════════════════════════════════════════════════════════

print("\nSolving...")
study.Solve()

if study.IsSolved:
    print("Solution complete ✓")
else:
    print("Solution failed ✗")


# ══════════════════════════════════════════════════════════════════════
#  7. EXPORT RESULTS
# ══════════════════════════════════════════════════════════════════════

# Create results directory
IO.Directory.CreateDirectory(RESULTS_DIR)

# Get results
stress_result = study.GetResult(ResultType.VonMisesStress)
disp_result = study.GetResult(ResultType.TotalDisplacement)

# Export stress
stress_path = IO.Path.Combine(RESULTS_DIR, 'stress.csv')
with open(stress_path, 'w') as f:
    f.write('node_id,x,y,z,stress_pa\n')
    for node in stress_result.Nodes:
        pos = node.Position
        val = node.Value
        f.write(f'{node.Id},{pos.X},{pos.Y},{pos.Z},{val}\n')

# Export displacement
disp_path = IO.Path.Combine(RESULTS_DIR, 'displacement.csv')
with open(disp_path, 'w') as f:
    f.write('node_id,x,y,z,ux,uy,uz,total\n')
    for node in disp_result.Nodes:
        pos = node.Position
        vec = node.Vector
        tot = node.Value
        f.write(f'{node.Id},{pos.X},{pos.Y},{pos.Z},{vec.X},{vec.Y},{vec.Z},{tot}\n')

# Export summary
summary_path = IO.Path.Combine(RESULTS_DIR, 'summary.csv')
with open(summary_path, 'w') as f:
    f.write('metric,value\n')
    f.write(f'max_stress_pa,{stress_result.Maximum}\n')
    f.write(f'max_displacement_m,{disp_result.Maximum}\n')

    total_mass = sum(body.Mass for body in all_bodies)
    f.write(f'total_mass_kg,{total_mass}\n')


# ══════════════════════════════════════════════════════════════════════
#  SUMMARY
# ══════════════════════════════════════════════════════════════════════

print("\n" + "="*60)
print("SIMULATION COMPLETE")
print("="*60)
print(f"Beam: {BEAM_LENGTH}x{BEAM_WIDTH}x{BEAM_HEIGHT}mm")
print(f"Material: {MATERIAL_NAME}")
print(f"Load: {APPLIED_FORCE}N")
print(f"\nResults:")
print(f"  Max stress: {stress_result.Maximum/1e6:.1f} MPa")
print(f"  Max displacement: {disp_result.Maximum*1000:.3f} mm")
print(f"  Mass: {total_mass*1000:.1f} g")
print(f"\nExported to: {RESULTS_DIR}")
print("="*60)
