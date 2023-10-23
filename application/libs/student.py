import gi
from libs import ocrRead, sqlLib
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf

DRAG_ACTION = Gdk.DragAction.COPY
(TARGET_ENTRY_TEXT, TARGET_ENTRY_PIXBUF) = range(2)
(COLUMN_TEXT, COLUMN_PIXBUF) = range(2)

class StudentWin(Gtk.VBox):
    def __init__(self,parent):
        Gtk.VBox.__init__(self)
        self.parent = parent
        self.label = Gtk.Label("Student Win")
        self.pack_start(self.label,0,0,5)
        
        self.drop_area = DropArea(self)
        self.pack_start(self.drop_area, 0, 0, 5)

        self.add_text_targets()
        sqlLib.getStudentsLessons(self.parent.ActiveNo)
        
    def studentLogInC(self,widget):
        self.parent.stack.set_visible_child_name("read_url")
    
    def teacherLogInC(self,widget):
        self.parent.stack.set_visible_child_name("select_size")

    def rootLogInC(self,widget):
        self.parent.stack.set_visible_child_name("select_size")

    def add_text_targets(self, button=None):
        self.drop_area.drag_dest_set_target_list(None)
        self.drag_source_set_target_list(None)

        self.drop_area.drag_dest_add_text_targets()
        self.drag_source_add_text_targets()
        

class DropArea(Gtk.Label):
    def __init__(self, parent):
        self.parent = parent
        Gtk.Label.__init__(self)
        self.set_label("Transkrip Yükle!")
        self.drag_dest_set(Gtk.DestDefaults.ALL, [], DRAG_ACTION)

        self.connect("drag-data-received", self.on_drag_data_received)

    def on_drag_data_received(self, widget, drag_context, x, y, data, info, time):
        if info == TARGET_ENTRY_TEXT:
            text = data.get_text()
            #ocr bağlantısı kurulacak
            file = text.split(".pdf")[0]
            file = file+".pdf"
            print("recieved : "+ text)
            lessonList = ocrRead.runOcr(file)
            sqlLib.NewStudentLessons(self.parent.parent.ActiveNo, lessonList)
            sqlLib.getAllSL()

        elif info == TARGET_ENTRY_PIXBUF:
            pixbuf = data.get_pixbuf()
            width = pixbuf.get_width()
            height = pixbuf.get_height()

            print("Received pixbuf with width %spx and height %spx" % (width, height))

        else:
            print("unknown recieved")

