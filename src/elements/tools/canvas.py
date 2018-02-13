import cairo
import gi

from src.elements.primitives import ANONYMOUS
from src.elements.primitives.selection import Selection
from src.elements.properties.origin import Origin
from src.elements.tools.document import Document
from src.elements.tools.grid import Grid
from src.elements.tools.page import Page
from src.events.signals import Signals

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk


class BaseCanvas(Gtk.DrawingArea, Signals):
    def __init__(self):
        Gtk.DrawingArea.__init__(self)
        Signals.__init__(self)

        # Initialize events
        self.add_events(
            Gdk.EventMask.EXPOSURE_MASK |
            Gdk.EventMask.BUTTON_RELEASE_MASK |
            Gdk.EventMask.BUTTON_PRESS_MASK |
            Gdk.EventMask.POINTER_MOTION_MASK |
            Gdk.EventMask.SCROLL_MASK
        )
        self.expose_id = self.connect("draw", self.draw)
        self.motion_id = self.connect("motion-notify-event", self.motion)
        self.connect("button-press-event", self.press)
        self.connect("button-release-event", self.release)

        # Initialize signals
        self.install_signal("select")
        self.install_signal("finish-select")

    def motion(self, widget, context):
        raise NotImplementedError

    def press(self, widget, context):
        raise NotImplementedError

    def release(self, widget, context):
        raise NotImplementedError

    def draw(self, widget, context):
        raise NotImplementedError


class CanvasImplementation(BaseCanvas):
    def __init__(self):
        BaseCanvas.__init__(self)
        self.origin = Origin()
        self.selection = Selection()
        self.grid = Grid()
        self.document = Document()

        # Add Page
        page = Page()
        self.document.pages.append(page)

        # Page properties
        self.zoom = 1.0
        self.border = 0

        # Set true when shapes and items are selected/added
        self.has_child = False
        self.should_update = False
        self.new_child = None

    # Handles button release
    def release(self, widget, event):

        if self.selection.is_active:
            # Deselect all child
            self.deselect_all()

            # Select all child inside selection window
            for child in self.document.get_current_page().get_children():
                if child.inside_selection(self.selection):
                    child.is_selected = True
                    self.emit("select", child)

            self.selection.is_active = False
        else:
            for child in self.document.get_current_page().get_children():
                if child.is_selected:
                    self.emit("finish-select", child)

                if child.is_resizing:
                    child.is_resizing ^= 1
                    self.emit("finish-select", child)

        self.has_child = False
        self.should_update = False
        self.update_canvas()
        return True

    # Handles mouse motion
    def motion(self, widget, event):

        self.disconnect(self.motion_id)

        x = event.x / self.zoom
        y = event.y / self.zoom

        # Selection rectangle properties based on mouse motion
        if self.selection.is_active:
            self.selection.width = x - self.selection.x
            self.selection.height = y - self.selection.y
            self.should_update = False
            self.update_canvas()
        elif event.state & Gdk.ModifierType.BUTTON1_MASK:
            for selected_children in self.document.get_current_page().get_children():
                if selected_children.is_selected:
                    if selected_children.is_resizing:
                        selected_children.resize(self.grid.get_nearest_axis(x), self.grid.get_nearest_axis(y))
                    pass
                else:
                    pass

                # Update on every resize
                self.update_canvas()

        self.motion_id = self.connect("motion-notify-event", self.motion)

        return True

    # Handles button press
    def press(self, widget, event):

        x = event.x / self.zoom
        y = event.y / self.zoom

        def resize_child(selected_child):
            # Deselect all children
            self.deselect_all()

            # Select current selected child
            selected_child.is_selected = True
            selected_child.is_resizing = True
            if selected_child.direction < ANONYMOUS:
                selected_child.pivot.x = self.grid.get_nearest_axis(x)
                selected_child.pivot.y = self.grid.get_nearest_axis(y)

        # Add child when pressed
        if self.has_child:
            # Deselect all children
            self.deselect_all()

            current_child = self.new_child
            self.add_child(current_child)

            current_child.is_selected = True

            # Change child properties
            current_child.x = self.grid.get_nearest_axis(x)
            current_child.y = self.grid.get_nearest_axis(y)

            current_child.height = 0
            current_child.width = 0

            resize_child(current_child)
            self.emit("select", current_child)
            return True

        selection = True

        # Select a child
        def select_child(child_to_select):
            if not event.state & Gdk.ModifierType.CONTROL_MASK:
                self.deselect_all()

            child_to_select.is_selected = True

        # Select group of children
        for page_child in sorted(self.document.get_current_page().get_children(),
                                 key=lambda page_child: page_child.z_index):
            if page_child.is_selected:
                pass
            elif page_child.inside_position(x, y):
                selection = False
                select_child(page_child)
            else:
                continue

        # Show selection rectangle
        if selection:
            self.selection.x = x
            self.selection.y = y
            self.selection.width = 0
            self.selection.height = 0
            self.selection.is_active = True

        self.update_canvas()
        return True

    # Draws canvas
    def draw(self, widget, context):

        self.disconnect(self.expose_id)

        # Draw canvas background and scale based on zoom value
        context.scale(self.zoom, self.zoom)
        context.set_source_rgb(0.51, 0.51, 0.51)
        context.paint()

        page = self.document.get_current_page()

        # Draw document
        self.document.draw(context, self.border, self.zoom)

        # Get page position every time, as position of page can change during zoom or move.
        self.origin.x = page.x + page.left
        self.origin.y = page.y + page.top

        # Draw grid if active
        if self.grid.is_active:
            self.grid.x = self.origin.x
            self.grid.y = self.origin.y
            self.grid.width = page.width - page.left - page.right
            self.grid.height = page.height - page.top - page.bottom
            self.grid.draw(context)

        # Draw selection rectangle
        self.selection.draw(context)

        self.should_update = True
        self.expose_id = self.connect("draw", self.draw)
        return True

    # Update canvas
    def update_canvas(self):
        if not self.should_update:
            pass
        self.queue_draw()

    # Add shapes to page
    def add_child(self, child):
        self.document.get_current_page().add_child(child)

    # Create a child
    def create_child(self, new_child):
        self.has_child = True
        self.new_child = new_child
        new_child.z_index = len(self.document.get_current_page().get_children())

    # Delete selected child
    def delete_children(self):
        for child in self.document.get_current_page().get_children():
            self.document.get_current_page().delete_object(child)
        self.update_canvas()

    # Select all children
    def select_all(self, **args):
        for child in self.document.get_current_page().get_children():
            child.is_selected = True
        self.queue_draw()

    # Deselect all selected children
    def deselect_all(self):
        for child in self.document.get_current_page().get_children():
            child.is_selected = False
        self.queue_draw()


class ExtendedCanvas(CanvasImplementation):
    def __init__(self):
        CanvasImplementation.__init__(self)

    # Add document page
    def add_page(self):
        page = self.document.get_current_page()
        self.document.pages.append(page)
        self.queue_draw()

    # Scale canvas by factor
    def scale_factor(self, factor):
        self.zoom += factor
        if self.zoom < 0.05:
            self.zoom = 0.05
        self.queue_draw()

    # Reset canvas scale
    def scale_normal(self, factor):
        self.zoom = factor
        self.queue_draw()

    # Zoom in canavs
    def zoom_in(self, factor=0.05):
        return self.scale_factor(factor)

    # Zoom out canvas
    def zoom_out(self, factor=-0.05):
        return self.scale_factor(factor)

    # Reset canvas zoom
    def zoom_normal(self):
        return self.scale_normal(1.0)

    # Draw children
    def draw_children(self, page, context):
        for child in page.children:
            child.draw(context)

    # Save canvas to pdf
    def save_to_pdf(self):
        for i, page in enumerate(self.document.pages):
            surface = cairo.PDFSurface("untitled.pdf", page.width, page.height)
            context = cairo.Context(surface)
            self.draw_children(page, context)

            # context.show_page()
            surface.flush()

    # Toggle canvas grid
    def toggle_grid(self):
        self.grid.is_active ^= 1
        self.grid.has_snap ^= 1
        self.queue_draw()


class Canvas(ExtendedCanvas):
    def __init__(self):
        ExtendedCanvas.__init__(self)
