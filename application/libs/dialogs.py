import gi
from libs import ocrRead, sqlLib, teacher
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf

        
class textMessage(Gtk.Dialog):
    def __init__(self, parent,text):
        super().__init__(title=" Error ! ")
        self.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK
        )
        self.parent = parent
        box = self.get_content_area()
        self.label = Gtk.Label(text)
        box.pack_start(self.label,0,0,5)
        self.show_all()
