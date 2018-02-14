import cairo

from src.elements.primitives.rectangle import Rectangle


# Selection rectangle
class Selection(Rectangle):
    def __init__(self):
        Rectangle.__init__(self)
        self.is_active = False

    def draw(self, context):
        if self.is_active:
            context.set_antialias(cairo.ANTIALIAS_GRAY)

            # Draw selection rectangle
            dash = list()
            context.set_dash(dash)
            context.set_line_width(1.0 / context.get_matrix()[0])
            context.rectangle(self.x, self.y, self.width, self.height)
            context.set_source_rgba(0.0, 0.0, 0.5, 0.15)
            context.fill_preserve()

            # Draw selection border
            context.set_source_rgba(0.0, 0.0, 0.25, 0.5)
            context.stroke()

            context.set_antialias(cairo.ANTIALIAS_DEFAULT)
        else:
            pass
