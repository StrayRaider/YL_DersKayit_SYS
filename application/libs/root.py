import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk




class RootWin(Gtk.VBox):
    def __init__(self,parent):
        Gtk.VBox.__init__(self)
        self.parent = parent
        self.label = Gtk.Label("Student Win")
        self.pack_start(self.label,0,0,5)
        
        self.studentB = Gtk.Button()
        self.studentB.set_label("Student LogIn")
        self.studentB.connect("clicked",self.studentLogInC)
        
        self.teacherB = Gtk.Button()
        self.teacherB.set_label("Teacher LogIn")
        self.teacherB.connect("clicked",self.teacherLogInC)


        self.rootB = Gtk.Button()
        self.rootB.set_label("Root LogIn")
        self.rootB.connect("clicked",self.rootLogInC)

        self.pack_start(self.studentB,0,0,5)
        self.pack_start(self.teacherB,0,0,5)
        self.pack_start(self.rootB,0,0,5)


    def studentLogInC(self,widget):
        self.parent.stack.set_visible_child_name("read_url")
    
    def teacherLogInC(self,widget):
        self.parent.stack.set_visible_child_name("select_size")

    def rootLogInC(self,widget):
        self.parent.stack.set_visible_child_name("select_size")



