import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class Select_size(Gtk.VBox):
    def __init__(self,parent):
        Gtk.VBox.__init__(self)
        self.parent = parent
        self.vert = Gtk.VBox()
        self.entry_box = Gtk.HBox()
        self.pack_start(self.vert,0,0,5)
        self.vert.pack_start(self.entry_box,0,0,5)
        self.label = Gtk.Label("read url")
        self.vert.pack_start(self.label,1,1,5)
        self.url_entry = Gtk.Entry()
        self.entry_box.pack_start(self.url_entry,1,1,5)
        self.set_size = Gtk.Button(label="Read")
        self.vert.pack_start(self.set_size,0,0,5)
        self.set_size.connect("clicked",self.start)
        self.url_but_1 = Gtk.Button(label="URL 1")
        self.url_but_2 = Gtk.Button(label="URL 2")
        self.url_but_1.connect("clicked",self.url_but_1_c)
        self.url_but_2.connect("clicked",self.url_but_2_c)
        self.url_box = Gtk.HBox()
        self.vert.pack_start(self.url_box,1,1,5)
        self.url_box.pack_start(self.url_but_1,1,1,5)
        self.url_box.pack_start(self.url_but_2,1,1,5)

        self.turn_back_but = Gtk.Button(label="Turn Back")
        self.vert.pack_start(self.turn_back_but,0,0,5)
        self.turn_back_but.connect("clicked",self.turn_back)

    def url_but_1_c(self,widget):
        self.start(None,"http://bilgisayar.kocaeli.edu.tr/prolab2/url1.txt")

    def url_but_2_c(self,widget):
        self.start(None,"http://bilgisayar.kocaeli.edu.tr/prolab2/url2.txt")

    def start(self,widget,url=None):
        if url == None:
            url = self.url_entry.get_text()
        self.parent.stack.set_visible_child_name("game")
        self.parent.game.start(1,url)
        #self.parent.game.start(1,"./mz_lib/maps/url1.txt")

    def turn_back(self,widget):
        self.parent.stack.set_visible_child_name("problem_select")