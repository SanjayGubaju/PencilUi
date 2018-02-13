import gi

gi.require_version('Gtk', '3.0')
from gi.repository import GObject


class Signals(GObject.GObject):
    def __init__(self):
        GObject.GObject.__init__(self)

    def install_signal(self, signal):
        if not GObject.signal_lookup(signal, self.__class__):
            GObject.signal_new(signal, self.__class__, GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE,
                               (GObject.TYPE_PYOBJECT,))
