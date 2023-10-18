import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class MyWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Youtube Installation")
        self.main_box = Gtk.HBox()
        self.add(self.main_box)
        left_box = Gtk.Box()
        right_box = Gtk.Box()
        mid_box = Gtk.VBox()
        self.main_box.pack_start(left_box,1,1,10)
        self.main_box.pack_start(mid_box,1,1,10)
        self.main_box.pack_start(right_box,1,1,10)

        #student button
        but_box = Gtk.HBox()
        mid_box.pack_start(but_box,0,0,10)
        new_box = Gtk.HBox()
        but_box.pack_start(new_box,0,0,0)
        self.button = Gtk.Button(label=" Student LogIn ")
        self.button.connect("clicked", self.studentLogIn)
        new_box.pack_start(self.button,0,0,10)

    def studentLogIn(widget,signal):
        print("student login")


def quit_app(arg):
    print("quiting..")
    Gtk.main_quit()
    print("All Done")

