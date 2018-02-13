import gi

from src.elements.tools.canvas import Canvas

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk


class Editor(Gtk.HPaned):
    def __init__(self):
        print("Editor Initialized")
        Gtk.HPaned.__init__(self)

        # Add Canvas to the application
        self.canvas = Canvas()
        self.init_canvas()

        # self.canvas.add_page()
        self.add(self.canvas)


    def init_canvas(self):
        self.canvas.connect("scroll-event", self.zoom_page)

    # Page properties
    def setup_pages(self):
        for page in self.canvas.document.pages:
            page.width = 320
            page.height = 480

    # Mouse scroll event handler
    def zoom_page(self, widget, event):
        if event.state & Gdk.ModifierType.CONTROL_MASK:
            if event.direction == Gdk.ScrollDirection.UP:
                self.zoom_in()
            else:
                self.zoom_out()

        return True

    # Reset canvas
    def zoom_reset(self):
        self.canvas.zoom_normal()

    # Canvas Zoom in
    def zoom_in(self):
        self.canvas.zoom_in()

    # Canvas Zoom out
    def zoom_out(self):
        self.canvas.zoom_out()

    # Scroll
    def scroll_page(self, widget, event):
        return True

    def toggle_grid(self):
        self.canvas.toggle_grid()
