from src.elements.primitives.rectangle import Rectangle


class Margins(Rectangle):
    def __init__(self):
        Rectangle.__init__(self)

        self.is_active = True

        # Margin properties
        self.top = 0
        self.left = 0
        self.bottom = 0
        self.right = 0

    def draw(self, context):
        context.set_source_rgba(0.0, 0.0, 0.0, 0.0)
        context.stroke()
        pass
