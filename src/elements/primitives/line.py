import cairo

from src.elements.primitives.object import Object
from src.elements.properties.point import Point


class Line(Object):
    __name__ = "Line"

    def __init__(self):
        Object.__init__(self)

        self.is_line = True

        self.start_point = Point()
        self.end_point = Point()

        self.line_width = 1

    def initialize_controls(self):
        self.handler.set_controls(
            north_west=Point(self.start_point.x, self.start_point.y),
            south_east=Point(self.end_point.x, self.end_point.y)
        )

    def draw(self, context):
        # line
        context.move_to(self.start_point.x, self.start_point.y)
        context.line_to(self.end_point.x, self.end_point.y)

        # Stroke Color
        context.set_line_cap(cairo.LINE_CAP_ROUND)

        if self.is_selected:
            context.set_source_rgba(0.18, 0.76, 1.0, 1.0)
        else:
            context.set_source_rgba(self.fill_color.red, self.fill_color.green, self.fill_color.blue,
                                    self.fill_color.alpha)
        context.set_line_width(self.line_width)
        context.stroke()

        Object.draw(self, context)

    def resize(self, new_x, new_y):
        Object.resize(self, new_x, new_y)

        # Set start point
        self.start_point.x = self.handler.pivot_control.x
        self.start_point.y = self.handler.pivot_control.y

        # Set end point
        self.end_point.x = new_x
        self.end_point.y = new_y
