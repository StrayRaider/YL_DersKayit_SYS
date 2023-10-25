import gi
from libs import sqlLib

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class TeacherWin(Gtk.VBox):
    def __init__(self,parent):
        Gtk.VBox.__init__(self)
        self.parent = parent
        self.label = Gtk.Label("Teacher Win")
        self.pack_start(self.label,0,0,5)

        self.lessonButton = Gtk.Button()
        self.lessonButton.set_label("Create New Lesson")
        self.lessonButton.connect("clicked",self.lessonButtonC)
        self.pack_start(self.lessonButton,0,0,5)

        self.intButton = Gtk.Button()
        self.intButton.set_label("New Interest")
        self.intButton.connect("clicked",self.intButtonC)
        self.pack_start(self.intButton,0,0,5)

        self.turnbackB = Gtk.Button()
        self.turnbackB.set_label("Back")
        self.turnbackB.connect("clicked",self.turnbackBC)
        self.pack_start(self.turnbackB,0,0,5)

    def turnbackBC(self,widget):
        self.parent.stack.set_visible_child_name("way_select")
        sqlLib.closeDB()
        sqlLib.connect()

    def lessonButtonC(self,widget):
        self.dialog = LessonDialog(self)
        response = self.dialog.run()
        if response == Gtk.ResponseType.OK:
            print("The OK button was clicked")
            self.dialog.destroy()
        elif response == Gtk.ResponseType.CANCEL:
            print("The Cancel button was clicked")
            self.dialog.destroy()

    def intButtonC(self,widget):
        self.dialog = InterestDialog(self)
        response = self.dialog.run()

class LessonDialog(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="New Lesson")
        self.parent = parent
        self.set_default_size(650, 600)
        box = self.get_content_area()

        self.nameEntery = Gtk.Entry()
        self.nameEntery.set_placeholder_text(" Lesson Name ")
        box.pack_start(self.nameEntery,0,0,5)

class InterestDialog(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Interest")
        self.parent = parent
        self.set_default_size(650, 600)
        box = self.get_content_area()


        interests = [
            "OS",
            "AI"
        ]
        self.intcombo = Gtk.ComboBoxText()
        self.intcombo.set_entry_text_column(0)
        self.intcombo.connect("changed", self.on_int_combo_changed)
        for interest in interests:
            self.intcombo.append_text(interest)

        self.intcombo.set_active(0)
        box.pack_start(self.intcombo, False, False, 5)

        interests = sqlLib.getInterest(self.parent.parent.ActiveNo,"teacher")

        self.label = Gtk.Label(interests)
        box.pack_start(self.label,0,0,5)

        self.newIntB = Gtk.Button()
        self.newIntB.set_label("New User")
        self.newIntB.connect("clicked",self.newIntC)
        box.pack_start(self.newIntB,0,0,5)

        self.show_all()


    def newIntC(self,widget):
        text = self.intcombo.get_active_text()
        if text is not None:
            print("Selected: currency=%s" % text)
            #add interest to teacher
            sqlLib.setInterest(self.parent.parent.ActiveNo, "teacher", text)
            interests = sqlLib.getInterest(self.parent.parent.ActiveNo,"teacher")
            self.label.set_text(str(interests))


    def on_int_combo_changed(self, widget):
        text = self.intcombo.get_active_text()
        if text is not None:
            print("Selected: currency=%s" % text)
