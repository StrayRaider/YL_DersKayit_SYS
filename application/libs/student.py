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

        self.connect("draw",self.updateStudentInfo)

        self.lessonButton = Gtk.Button()
        self.lessonButton.set_label("Show Lessons")
        self.lessonButton.connect("clicked",self.lessonButtonC)
        self.pack_start(self.lessonButton,0,0,5)
        
        self.drop_area = DropArea(self)
        self.pack_start(self.drop_area, 0, 0, 5)

        self.add_text_targets()
        sqlLib.getStudentsLessons(self.parent.ActiveNo)

        self.nameL = Gtk.Label(label="Name : ")
        self.surnameL = Gtk.Label(label="surname : ")
        self.studentNoL = Gtk.Label(label="Student Number : ")
        self.noteL = Gtk.Label(label="Grade Avarage : ")

        self.pack_start(self.nameL,0,0,5)
        self.pack_start(self.surnameL,0,0,5)
        self.pack_start(self.studentNoL,0,0,5)
        self.pack_start(self.noteL,0,0,5)

        self.turnbackB = Gtk.Button()
        self.turnbackB.set_label("Back")
        self.turnbackB.connect("clicked",self.turnbackBC)
        self.pack_start(self.turnbackB,0,0,5)

        self.updateStudentInfo(None,None)
        
    def add_text_targets(self, button=None):
        self.drop_area.drag_dest_set_target_list(None)
        self.drag_source_set_target_list(None)

        self.drop_area.drag_dest_add_text_targets()
        self.drag_source_add_text_targets()

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

    def updateStudentInfo(self,widget,cr):
        studentData = sqlLib.getStudentData(self.parent.ActiveNo)
        print(studentData)
        if studentData and studentData != []:
            self.nameL.set_text("Name : {}".format(studentData[2]))
            self.surnameL.set_text("surname : {}".format(studentData[3]))
            self.studentNoL.set_text("Student Number : {}".format(studentData[1]))
            self.noteL.set_text("Grade Avarage : {}".format(studentData[5]))

        
class LessonDialog(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="My Lessons")
        self.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK
        )
        self.parent = parent
        self.set_default_size(650, 600)
        box = self.get_content_area()


        #----------------------------------İndirilecekler Listesi
        #treeview ve list store oluşturulması
        #list store oluştururken sütunların hangi tipte değişken tutacağı belirtilir
        self.StudentLStore = Gtk.ListStore(str,str,str,str)
        self.StudentLTree = Gtk.TreeView(self.StudentLStore)
        #içinde tutacağı değişken tipine göre bölme oluşturulması
        cell = Gtk.CellRendererText()
        cell.set_property("editable", True) #eğer tect değiştirilebilir olsun istersen
        #stun tanımlama işlemi 1. argüman stun adı, 2. tutacağı hücre tipi 3, ekleme
        #yaparken listenin kaçıncı argümanını alacağı
        recColumn = Gtk.TreeViewColumn("rec",cell,text = 0)
        recColumn.set_max_width(70)

        sNocolumn = Gtk.TreeViewColumn("Student No",cell,text = 1)
        sNocolumn.set_max_width(70)

        lNocolumn = Gtk.TreeViewColumn("Lesson No",cell,text = 2)
        lNocolumn.set_max_width(70)

        notecolumn = Gtk.TreeViewColumn("Note ",cell,text = 3)
        notecolumn.set_max_width(70)
               
        self.StudentLTree.append_column(recColumn)
        self.StudentLTree.append_column(sNocolumn)
        self.StudentLTree.append_column(lNocolumn)
        self.StudentLTree.append_column(notecolumn)

        #check button stunu oluşturma işlemi
        #uygun hücre oluşturma
        #check_cell = Gtk.CellRendererToggle()
        #del_cell = Gtk.CellRendererToggle()
        #hücre içi widget fonksiyon bağlantısı
        #check_cell.connect("toggled", self.tree_but_toggle,1,"i")
        #del_cell.connect("toggled", self.del_tree_obj,3,"i")
        #satır oluşturma 1. satır adı 2. hücre tipi
        #t_column = Gtk.TreeViewColumn("->",check_cell)
        #del_column = Gtk.TreeViewColumn("del",del_cell)
        #stuna argümanları dışarda bu fonksiyonla da verebilirsin
        #t_column.add_attribute(check_cell,"active",1)
        #t_column.set_max_width(30)
        #del_column.set_max_width(30)

        #stun treeview ekleme işlemi
        #self.iSongTree.append_column(t_column)
        #self.iSongTree.append_column(del_column)
        #self.iSongTree.append_column(u_column)
        #self.iSongTree.append_column(recColumn)
 
        #yeni satırlar oluşturma
        #self.iSongStore.append(["song_name",True,"url"])
        l_scrolled = Gtk.ScrolledWindow()
        box.pack_start(l_scrolled,1,1,10)
        l_scrolled.add(self.StudentLTree)

        print(type(self.parent.parent.ActiveNo))
        activeNo = self.parent.parent.ActiveNo
        for i in sqlLib.getStudentsLessons(activeNo):
            print(i)
            string_list = []
            for item in i:
                string_list.append(str(item))
                
            self.StudentLStore.append([*string_list])


        label = Gtk.Label(label="This is a dialog to display additional information")

        box.add(label)
        self.show_all()


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
            lessonList, studentData = ocrRead.runOcr(file)
            sqlLib.NewStudentLessons(self.parent.parent.ActiveNo, lessonList)
            sqlLib.createNewStudent(self.parent.parent.ActiveNo, *studentData, file)
            self.parent.updateStudentInfo()
            sqlLib.getAllSL()

        elif info == TARGET_ENTRY_PIXBUF:
            pixbuf = data.get_pixbuf()
            width = pixbuf.get_width()
            height = pixbuf.get_height()

            print("Received pixbuf with width %spx and height %spx" % (width, height))

        else:
            print("unknown recieved")

