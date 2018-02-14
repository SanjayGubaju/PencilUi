from math import pi

import cairo


class Control:
    def __init__(self, stroke_width):
        self.is_active = True

        self.x = 0
        self.y = 0

        self.has_pivot = False

        self.stroke_width = stroke_width
        self.size = stroke_width * 2

    def draw(self, context):
        context.set_antialias(cairo.ANTIALIAS_GRAY)
        context.arc(self.x, self.y, self.size / context.get_matrix()[0], 0, 2.0 * pi)
        context.set_source_rgba(1.0, 1.0, 1.0, 1.0)
        context.fill_preserve()

        # Draw selection border
        context.set_source_rgba(0.18, 0.76, 1.0, 1.0)
        context.set_line_width(self.stroke_width / context.get_matrix()[0])
        context.stroke()
        context.set_antialias(cairo.ANTIALIAS_DEFAULT)

    def at_position(self, x, y):
        return (self.x - self.stroke_width) <= x <= (self.x + self.size) and (self.y - self.stroke_width) <= y <= (
            self.y + self.size)
