# Objects
# Move, Scale
# Rectangle, Line, Arrow, Eclipse, Polygon, Star
# Pen Tool, Pencil Tool
# Text
# Ruler

# -----------------------------------------------------
# Color (Red, Green, Blue, Alpha)

# ------------------------------------------------------
# Position (x-axis, y-axis)
# Size (width, height)
# Rotation in degrees
# Corner Radius(top-left, top-right, bottom-left, bottom-right)

# ------------------------------------------------------
# Fill (Color)
# Stroke (Color, weight, Align(Center, Inside, Outside))
from math import pi

__all__ = ['NONE', 'NORTHWEST', 'NORTH', 'NORTHEAST', 'WEST', 'EAST', 'SOUTHWEST', 'SOUTH', 'SOUTHEAST', 'ANONYMOUS',
           'HORIZONTAL', 'VERTICAL', 'BOTH',
           'get_direction', 'degree_to_radian', 'radian_to_degree']

NONE = -1

# Direction of movement
NORTHWEST = 0
NORTH = 1
NORTHEAST = 2
WEST = 3
EAST = 4
SOUTHWEST = 5
SOUTH = 6
SOUTHEAST = 7
ANONYMOUS = 8

# Orientation types
VERTICAL = 0
HORIZONTAL = 1
BOTH = 2


# Returns direction of movement
def get_direction(direction):
    if direction in [EAST, WEST]:
        return HORIZONTAL
    elif direction in [NORTH, SOUTH]:
        return VERTICAL
    else:
        return NONE


# Returns opposite direction for a direction
def opposite(direction):
    if direction == NORTHEAST:
        return SOUTHWEST
    elif direction == NORTH:
        return SOUTH
    elif direction == NORTHWEST:
        return SOUTHEAST
    elif direction == SOUTHEAST:
        return NORTHWEST
    elif direction == SOUTH:
        return NORTH
    elif direction == SOUTHWEST:
        return NORTHEAST
    elif direction == WEST:
        return EAST
    elif direction == EAST:
        return WEST
    return NONE


def degree_to_radian(degree):
    return float(degree) * pi / 180.0


def radian_to_degree(rad):
    return float(rad) * 180 / pi
