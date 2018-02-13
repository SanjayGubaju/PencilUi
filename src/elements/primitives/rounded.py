from math import pi

import cairo

from src.elements.primitives.object import Object


class Rounded(Object):
    __name__ = "Rectangle"

    def __init__(self):
        Object.__init__(self)

    def draw(self, context):

        # Radius of oval
        radius = float(0)

        if radius > (self.height / 2) or radius > (self.width / 2):
            if (self.height / 2) < (self.width / 2):
                radius = self.height / 2
            else:
                radius = self.width / 2

        context.move_to(self.x, self.y + radius)
        context.arc(self.x + radius, self.y + radius, radius, pi, -pi / 2)
        context.line_to(self.x + self.width - radius, self.y)
        context.arc(self.x + self.width - radius, self.y + radius, radius, -pi / 2, 0)
        context.line_to(self.x + self.width, self.y + self.height - radius)
        context.arc(self.x + self.width - radius, self.y + self.height - radius, radius, 0, pi / 2)
        context.line_to(self.x + radius, self.y + self.height)
        context.arc(self.x + radius, self.y + self.height - radius, radius, pi / 2, pi)
        context.close_path()

        if self.is_selected:
            context.set_source_rgba(1.0, 0.0, 0.0, 0.5)
        else:
            context.set_source_rgba(self.fill_color.red, self.fill_color.green, self.fill_color.blue,
                                    self.fill_color.alpha)

        context.fill_preserve()

        # Stroke Color
        context.set_source_rgba(self.stroke_color.red, self.stroke_color.green,
                                self.stroke_color.blue, self.stroke_color.alpha)
        context.set_line_width(self.stroke_width)
        context.stroke()

        # Draw object
        Object.draw(self, context)
