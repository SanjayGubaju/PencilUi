import gi

from src.elements.primitives import VERTICAL, HORIZONTAL

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Ruler(Gtk.DrawingArea):
    def __init__(self, orientation=VERTICAL):
        Gtk.DrawingArea.__init__(self)

        # Ruler properties
        self.orientation = orientation
        self.zoom = 1.0

        self.connect("draw", self.draw)

    def draw(self, widget, context):
        context.scale(self.zoom, self.zoom)
        context.set_source_rgb(0.0, 1.0, 0.0)
        context.paint()


class VerticalRuler(Ruler):
    def __init__(self):
        Ruler.__init__(self, VERTICAL)


class HorizontalRuler(Ruler):
    def __init__(self):
        Ruler.__init__(self, HORIZONTAL)
