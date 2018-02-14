import cairo

from src.elements.tools.margins import Margins


class Paper(Margins):
    def __init__(self):
        Margins.__init__(self)

        self.background = None

    def draw(self, context):
        # Background for paper
        context.save()

        context.set_antialias(cairo.ANTIALIAS_GRAY)
        context.set_line_width(1.0 / context.get_matrix()[0])
        context.rectangle(self.x, self.y, self.width, self.height)

        context.set_source_rgba(1.0, 1.0, 1.0, 1.0)
        context.fill_preserve()

        # Draw margins
        Margins.draw(self, context)
        context.set_antialias(cairo.ANTIALIAS_DEFAULT)

        context.restore()

        pass
