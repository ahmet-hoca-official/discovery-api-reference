# -*- coding: utf-8 -*-
"""
Bolt Hole Pattern Example
==========================
Creates a plate with a bolt hole pattern.

Tested on: Ansys Discovery 2024 R2 (API V24)
"""

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

# Plate dimensions (mm)
PLATE_WIDTH = 120
PLATE_LENGTH = 100
PLATE_THICKNESS = 5

# Bolt hole parameters
HOLE_DIAMETER = 8.5  # M8 clearance hole (8.4mm nominal, 8.5mm for clearance)
HOLE_PATTERN = [
    # (x, y) positions in mm from plate center
    (40, 35),
    (40, -35),
    (-40, 35),
    (-40, -35),
]


# ══════════════════════════════════════════════════════════════════════
#  CLEAN UP
# ══════════════════════════════════════════════════════════════════════

bodies = GetRootPart().GetBodies()
for b in bodies:
    Selection.Create(b).Delete()


# ══════════════════════════════════════════════════════════════════════
#  CREATE BASE PLATE
# ══════════════════════════════════════════════════════════════════════

origin = Point.Create(0, 0, 0)
frame = Frame.Create(origin, Direction.DirX, Direction.DirY)

plate = BlockBody.Create(
    frame,
    MM(PLATE_WIDTH),
    MM(PLATE_LENGTH),
    MM(PLATE_THICKNESS)
)

print(f"Base plate created: {PLATE_WIDTH}x{PLATE_LENGTH}x{PLATE_THICKNESS}mm")


# ══════════════════════════════════════════════════════════════════════
#  CREATE BOLT HOLES
# ══════════════════════════════════════════════════════════════════════

hole_radius = MM(HOLE_DIAMETER / 2.0)
hole_height = MM(PLATE_THICKNESS * 1.5)  # Slightly taller than plate

hole_count = 0

for (x_mm, y_mm) in HOLE_PATTERN:
    # Convert to meters
    x = MM(x_mm)
    y = MM(y_mm)
    z = 0  # Holes start at plate center Z

    # Create hole center point
    hole_center = Point.Create(x, y, z)

    # Create cylinder (vertical, along Z-axis)
    cylinder = CylinderBody.Create(
        hole_center,
        Direction.DirZ,
        hole_radius,
        hole_height
    )

    hole_count += 1
    print(f"Hole {hole_count} created at ({x_mm}, {y_mm})mm")


# ══════════════════════════════════════════════════════════════════════
#  SUBTRACT HOLES FROM PLATE
# ══════════════════════════════════════════════════════════════════════

all_bodies = GetRootPart().GetBodies()

if len(all_bodies) > 1:
    main_body = all_bodies[0]  # The plate

    # Subtract each hole
    for i in range(1, len(all_bodies)):
        hole_body = GetRootPart().GetBodies()[1]  # Always get index 1 (next body after main)

        result = Combine.Execute(
            Selection.Create(main_body),
            Selection.Create(hole_body),
            CombineMode.Subtract
        )

        # Update main body reference
        main_body = GetRootPart().GetBodies()[0]

    print(f"\n{hole_count} holes subtracted from plate")
else:
    print("ERROR: No holes to subtract")


# ══════════════════════════════════════════════════════════════════════
#  SUMMARY
# ══════════════════════════════════════════════════════════════════════

final_body = GetRootPart().GetBodies()[0]
volume = final_body.Shape.Volume * 1e6  # m³ to cm³

print("\n" + "="*60)
print("BOLT HOLE PATTERN COMPLETE")
print("="*60)
print(f"Plate: {PLATE_WIDTH}x{PLATE_LENGTH}x{PLATE_THICKNESS}mm")
print(f"Holes: {hole_count} x Ø{HOLE_DIAMETER}mm")
print(f"Final volume: {volume:.2f} cm³")
print("="*60)
