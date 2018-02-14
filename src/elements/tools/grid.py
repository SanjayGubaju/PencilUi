import cairo

from src.elements.primitives.rectangle import Rectangle


class Grid(Rectangle):
    def __init__(self):
        Rectangle.__init__(self)

        self.is_active = False
        self.has_snap = False
        self.grid_size = 16

    def draw(self, context):
        context.set_antialias(cairo.ANTIALIAS_GRAY)
        context.set_line_width(1.0 / context.get_matrix()[0])
        context.set_source_rgba(0.0, 0.0, 0.0, 0.2)
        dash = [2.0 / context.get_matrix()[0], 2.0 / context.get_matrix()[0]]
        context.set_dash(dash)

        x = self.x
        y = self.y

        # Draw vertical lines
        while x <= self.x + self.width:
            context.move_to(x, self.y)
            context.line_to(x, self.y + self.height)
            x += self.grid_size

        while y <= self.y + self.height:
            context.move_to(self.x, y)
            context.line_to(self.x + self.width, y)
            y += self.grid_size

        context.stroke()
        context.set_antialias(cairo.ANTIALIAS_DEFAULT)

    # calculates nearest point
    def get_nearest_axis(self, value):
        if self.has_snap:
            # Calculate average and return whichever is greater.
            lower = self.grid_size * int(value / self.grid_size)
            upper = self.grid_size * int(value / self.grid_size) + self.grid_size
            middle = (lower + upper) / 2.0
            if value > middle:
                return float(upper)
            else:
                return float(lower)
        else:
            return value
