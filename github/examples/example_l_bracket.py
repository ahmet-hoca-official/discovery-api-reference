# -*- coding: utf-8 -*-
"""
L-Bracket Creation Example
===========================
Creates a simple L-shaped bracket using Discovery/SpaceClaim API.

Tested on: Ansys Discovery 2024 R2 (API V24)
"""

import math
from SpaceClaim.Api.V24 import *

# ══════════════════════════════════════════════════════════════════════
#  HELPER FUNCTIONS
# ══════════════════════════════════════════════════════════════════════

def MM(val):
    """Convert millimeters to meters (Discovery uses SI units)"""
    return val / 1000.0


# ══════════════════════════════════════════════════════════════════════
#  PARAMETERS
# ══════════════════════════════════════════════════════════════════════

# Dimensions in millimeters
BASE_WIDTH = 100    # mm
BASE_LENGTH = 80    # mm
VERTICAL_WIDTH = 100  # mm
VERTICAL_HEIGHT = 60  # mm
THICKNESS = 3       # mm
FILLET_RADIUS = 5   # mm


# ══════════════════════════════════════════════════════════════════════
#  CLEAN UP EXISTING GEOMETRY
# ══════════════════════════════════════════════════════════════════════

bodies = GetRootPart().GetBodies()
for b in bodies:
    Selection.Create(b).Delete()


# ══════════════════════════════════════════════════════════════════════
#  CREATE BASE PLATE (HORIZONTAL)
# ══════════════════════════════════════════════════════════════════════

# Base plate lies in XY plane
origin_base = Point.Create(0, 0, 0)
frame_base = Frame.Create(origin_base, Direction.DirX, Direction.DirY)

base_plate = BlockBody.Create(
    frame_base,
    MM(BASE_WIDTH),
    MM(BASE_LENGTH),
    MM(THICKNESS)
)

print(f"Base plate created: {BASE_WIDTH}x{BASE_LENGTH}x{THICKNESS}mm")


# ══════════════════════════════════════════════════════════════════════
#  CREATE VERTICAL PLATE
# ══════════════════════════════════════════════════════════════════════

# Vertical plate in XZ plane
origin_vert = Point.Create(0, 0, 0)
frame_vert = Frame.Create(origin_vert, Direction.DirX, Direction.DirZ)

vertical_plate = BlockBody.Create(
    frame_vert,
    MM(VERTICAL_WIDTH),
    MM(VERTICAL_HEIGHT),
    MM(THICKNESS)
)

print(f"Vertical plate created: {VERTICAL_WIDTH}x{VERTICAL_HEIGHT}x{THICKNESS}mm")


# ══════════════════════════════════════════════════════════════════════
#  BOOLEAN UNION
# ══════════════════════════════════════════════════════════════════════

all_bodies = GetRootPart().GetBodies()

if len(all_bodies) >= 2:
    result = Combine.Execute(
        Selection.Create(all_bodies[0]),
        Selection.Create(all_bodies[1]),
        CombineMode.Unite
    )
    print("Plates merged successfully")
else:
    print("WARNING: Expected 2 bodies for union")


# ══════════════════════════════════════════════════════════════════════
#  ADD FILLET TO INTERNAL CORNER
# ══════════════════════════════════════════════════════════════════════

# Find internal edges (simplified - selects all edges)
body = GetRootPart().GetBodies()[0]
edges_to_fillet = []

for edge in body.Edges:
    # In production, filter for internal concave edges only
    # For this example, we'll fillet all edges
    edges_to_fillet.append(edge)

if edges_to_fillet:
    try:
        result = ConstantRoundEdges.Execute(
            Selection.Create(edges_to_fillet),
            MM(FILLET_RADIUS),
            None,
            False  # Not rolling ball
        )
        print(f"Fillet applied: {FILLET_RADIUS}mm radius")
    except Exception as e:
        print(f"Fillet failed: {e}")
else:
    print("No edges found for filleting")


# ══════════════════════════════════════════════════════════════════════
#  SUMMARY
# ══════════════════════════════════════════════════════════════════════

final_body = GetRootPart().GetBodies()[0]
volume = final_body.Shape.Volume  # m³
mass = final_body.Mass if final_body.Mass else 0  # kg

print("\n" + "="*60)
print("L-BRACKET CREATION COMPLETE")
print("="*60)
print(f"Base: {BASE_WIDTH}x{BASE_LENGTH}x{THICKNESS}mm")
print(f"Vertical: {VERTICAL_WIDTH}x{VERTICAL_HEIGHT}x{THICKNESS}mm")
print(f"Fillet: {FILLET_RADIUS}mm")
print(f"Volume: {volume*1e6:.2f} cm³")
if mass > 0:
    print(f"Mass: {mass*1000:.2f} g")
print("="*60)
