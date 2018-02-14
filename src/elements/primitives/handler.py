import cairo

from src.elements.primitives import ANONYMOUS, NONE
from src.elements.primitives.control import Control
from src.elements.primitives.object import NORTHWEST, NORTHEAST, SOUTHWEST, SOUTHEAST, NORTH, SOUTH, WEST, EAST


class Handler:
    def __init__(self):
        self.controls = list()

        self.x = 0
        self.y = 0

        self.height = 0
        self.width = 0

        self.stroke_width = 2

        self.pivot_control = Control(self.stroke_width)
        self.pivot_control.has_pivot = True

        # Total of 8 controls. Draw all of them.
        # ANONYMOUS is 9th control which is outside the scope
        index = 0
        while index < ANONYMOUS:
            self.controls.append(Control(self.stroke_width))
            index += 1

        pass

    # Draw handler box
    def draw_handler(self, context):
        context.set_antialias(cairo.ANTIALIAS_GRAY)

        # Draw selection rectangle
        dash = list()
        context.set_dash(dash)
        context.rectangle(self.x, self.y, self.width, self.height)
        context.set_source_rgba(0.0, 0.0, 0.5, 0.0)
        context.fill_preserve()

        # Draw selection border
        context.set_source_rgba(0.18, 0.76, 1.0, 1.0)
        context.set_line_width(self.stroke_width / context.get_matrix()[0])
        context.stroke()

        context.set_antialias(cairo.ANTIALIAS_DEFAULT)

    # Draw all control points
    def draw_control(self, context):
        for control in self.controls:
            control.draw(context)

    def draw(self, context):
        self.draw_handler(context)
        self.draw_control(context)
        if self.pivot_control.has_pivot:
            self.pivot_control.draw(context)

    # Set current handler position and size
    def set_dimensions(self, x, y, width, height):
        self.x = x
        self.y = y
        self.height = height
        self.width = width

    # Sets control points for an object based on availability
    def set_controls(self, north_west=None, north_east=None, south_west=None, south_east=None, north=None, south=None,
                     west=None, east=None):

        if north_west is not None:
            self.controls[NORTHWEST].x = north_west.x
            self.controls[NORTHWEST].y = north_west.y

        if north is not None:
            self.controls[NORTH].x = north.x
            self.controls[NORTH].y = north.y

        if north_east is not None:
            self.controls[NORTHEAST].x = north_east.x
            self.controls[NORTHEAST].y = north_east.y

        if west is not None:
            self.controls[WEST].x = west.x
            self.controls[WEST].y = west.y

        if east is not None:
            self.controls[EAST].x = east.x
            self.controls[EAST].y = east.y

        if south_west is not None:
            self.controls[SOUTHWEST].x = south_west.x
            self.controls[SOUTHWEST].y = south_west.y

        if south is not None:
            self.controls[SOUTH].x = south.x
            self.controls[SOUTH].y = south.y

        if south_east is not None:
            self.controls[SOUTHEAST].x = south_east.x
            self.controls[SOUTHEAST].y = south_east.y

    def inside_position(self, x, y):
        return self.get_direction(x, y) is not NONE

    def get_direction(self, x, y):
        for direction, control in enumerate(self.controls):
            if control.at_position(x, y):
                return direction
        return NONE
