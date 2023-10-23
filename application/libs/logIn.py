import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from libs import sqlLib

class LogInWin(Gtk.VBox):
    def __init__(self,parent):
        Gtk.VBox.__init__(self)
        self.parent = parent
        self.label = Gtk.Label("LogIn Win")
        self.pack_start(self.label,0,0,5)

        self.idEntery = Gtk.Entry()
        self.idEntery.set_placeholder_text(" ID ")
        self.pack_start(self.idEntery,0,0,5)

        self.pwdEntery = Gtk.Entry()
        self.pwdEntery.set_placeholder_text(" Password ")
        self.pack_start(self.pwdEntery,0,0,5)
        
        self.logInB = Gtk.Button()
        self.logInB.set_label("LogIn")
        self.logInB.connect("clicked",self.logInC)
        self.pack_start(self.logInB,0,0,5)
        
    def logInC(self,widget):
        userId = self.idEntery.get_text()
        userPwd = self.pwdEntery.get_text()
        userRole = self.parent.way.split("_")[0]
        print(userRole)
        activeNo = sqlLib.LogIn(userId, userPwd, userRole)
        if activeNo != None and activeNo != False:
            print("loginnig")
            self.parent.ActiveNo = activeNo
            print("NO",activeNo)
            self.parent.stack.set_visible_child_name(self.parent.way)
        else:
            print("error wrong ıd or password")

        #next path
    
