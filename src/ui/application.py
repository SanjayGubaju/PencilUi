import gi

from src.elements.primitives.shape import Shape
from src.elements.tools.editor import Editor

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk


class Application(Gtk.Window):
    def __init__(self):
        super(Application, self).__init__(title="PencilUI")

        # Application
        # Center window at startup
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_default_size(320, 480)

        # Quit on destroy
        self.connect("destroy", Gtk.main_quit)

        # Menu
        self.menu_bar = Gtk.MenuBar()
        self.init_menu()

        # Editor
        self.editor = Editor()
        self.connect("key-press-event", self.key_pressed)
        self.editor.setup_pages()

        # Layout
        self.box = Gtk.VBox(False, 2)
        self.box.pack_start(self.menu_bar, False, False, 0)
        self.box.pack_start(self.editor, True, True, 1)
        self.add(self.box)

    def init_menu(self):
        # Add MenuBar

        # Global Menu
        file_menu = Gtk.Menu()

        # File Menu
        file_item = Gtk.MenuItem("File")
        file_item.set_submenu(file_menu)

        # Shortcuts
        accel_group = Gtk.AccelGroup()
        self.add_accel_group(accel_group)

        # Save Sub Menu
        save_menu = Gtk.MenuItem("Save", accel_group)
        key, mod = Gtk.accelerator_parse("<Control>S")
        save_menu.add_accelerator("activate", accel_group, key, mod, Gtk.AccelFlags.VISIBLE)
        save_menu.connect("activate", self.save_canvas)
        file_menu.append(save_menu)

        # Exit Sub Menu
        exit_menu = Gtk.MenuItem("Exit", accel_group)
        key, mod = Gtk.accelerator_parse("<Control>Q")
        exit_menu.add_accelerator("activate", accel_group, key, mod, Gtk.AccelFlags.VISIBLE)
        exit_menu.connect("activate", Gtk.main_quit)
        file_menu.append(exit_menu)

        self.menu_bar.append(file_item)

    def run(self):
        self.show_all()
        Gtk.main()

    def key_pressed(self, widget, event):

        # Add Rectangle
        if event.keyval == Gdk.KEY_r:
            self.create_object("Rectangle")

        # Add Oval
        if event.keyval == Gdk.KEY_l:
            self.create_object("Line")

        # Delete shape
        if event.keyval == Gdk.KEY_Delete or event.keyval == Gdk.KEY_KP_Delete:
            self.delete_object()

        # Save canvas
        if event.state & Gdk.ModifierType.CONTROL_MASK:
            if event.keyval == Gdk.KEY_s:
                self.editor.canvas.save_to_svg()
            elif event.keyval == Gdk.KEY_0 or event.keyval == Gdk.KEY_KP_0:
                self.editor.zoom_reset()
            elif event.keyval == Gdk.KEY_g:
                self.editor.toggle_grid()
            elif event.keyval == Gdk.KEY_plus or event.keyval == Gdk.KEY_KP_Add:
                self.editor.zoom_in()
            elif event.keyval == Gdk.KEY_minus or event.keyval == Gdk.KEY_KP_Subtract:
                self.editor.zoom_out()

    def create_object(self, shape_name):
        self.editor.canvas.create_child(Shape().get_shape(shape_name))

    def delete_object(self):
        self.editor.canvas.delete_children()

    @staticmethod
    def save_canvas(_):
        print("Saved")
