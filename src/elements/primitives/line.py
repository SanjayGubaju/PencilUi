import cairo

from src.elements.primitives.object import Object
from src.elements.properties.point import Point


class Line(Object):
    __name__ = "Line"

    def __init__(self):
        Object.__init__(self)

        self.start_point = Point()
        self.end_point = Point()
        self.line_width = 1

    def draw(self, context):

        # line
        context.move_to(self.start_point.x, self.start_point.y)
        context.line_to(self.end_point.x, self.end_point.y)

        # Stroke Color
        context.set_line_cap(cairo.LINE_CAP_ROUND)
        if self.is_selected:
            context.set_source_rgba(1.0, 0.0, 0.0, 0.5)
        else:
            context.set_source_rgba(self.fill_color.red, self.fill_color.green, self.fill_color.blue,
                                    self.fill_color.alpha)
        context.set_line_width(self.line_width)
        context.stroke()

        Object.draw(self, context)

    def resize(self, x, y):
        Object.resize(self, x, y)

        self.start_point.x = self.pivot.x
        self.start_point.y = self.pivot.y
        self.end_point.x = x
        self.end_point.y = y
