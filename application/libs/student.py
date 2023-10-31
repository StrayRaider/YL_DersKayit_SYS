import gi
from libs import ocrRead, sqlLib, teacher
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

        self.intButton = Gtk.Button()
        self.intButton.set_label("New Interest")
        self.intButton.connect("clicked",self.intButtonC)
        self.pack_start(self.intButton,0,0,5)

        self.pack_start(self.nameL,0,0,5)
        self.pack_start(self.surnameL,0,0,5)
        self.pack_start(self.studentNoL,0,0,5)
        self.pack_start(self.noteL,0,0,5)

        self.reqLB = Gtk.Button()
        self.reqLB.set_label("Request Lesson")
        self.reqLB.connect("clicked",self.reqLBC)
        self.pack_start(self.reqLB,0,0,5)

        self.readM = Gtk.Button()
        self.readM.set_label("Read Messages")
        self.readM.connect("clicked",self.readMC)
        self.pack_start(self.readM,0,0,5)

        self.turnbackB = Gtk.Button()
        self.turnbackB.set_label("Back")
        self.turnbackB.connect("clicked",self.turnbackBC)
        self.pack_start(self.turnbackB,0,0,5)


        self.updateStudentInfo(None,None)


    def readMC(self,widget):
        studentNo = studentData = sqlLib.getStudentData(self.parent.ActiveNo)[1]
        self.dialog = teacher.readMessages(self, studentNo, "student")
        response = self.dialog.run()

    def intButtonC(self,widget):
        self.dialog = teacher.InterestDialog(self,role="student")
        response = self.dialog.run()
        
    def add_text_targets(self, button=None):
        self.drop_area.drag_dest_set_target_list(None)
        self.drag_source_set_target_list(None)

        self.drop_area.drag_dest_add_text_targets()
        self.drag_source_add_text_targets()

    def turnbackBC(self,widget):
        self.parent.stack.set_visible_child_name("way_select")
        sqlLib.closeDB()
        sqlLib.connect()

    def reqLBC(self,widget):
        self.dialog = LessonReq(self)
        response = self.dialog.run()

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
        try:
            studentData = sqlLib.getStudentData(self.parent.ActiveNo)
            #print(studentData)
            if studentData and studentData != []:
                self.nameL.set_text("Name : {}".format(studentData[2]))
                self.surnameL.set_text("surname : {}".format(studentData[3]))
                self.studentNoL.set_text("Student Number : {}".format(studentData[1]))
                self.noteL.set_text("Grade Avarage : {}".format(studentData[5]))
        except:
            pass

        
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


class LessonReq(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="My Lessons")
        self.parent = parent
        self.set_default_size(650, 600)
        box = self.get_content_area()

        self.intFilter = None
        self.noFilter = None

        # lessonNo, lessonName, TeacherName, TeacherReg
        self.StudentLStore = Gtk.ListStore(str,str,str,str,str,bool)
        self.StudentLTree = Gtk.TreeView(self.StudentLStore)

        cell = Gtk.CellRendererText()
        cell.set_property("editable", True) #eğer tect değiştirilebilir olsun istersen

        noColumn = Gtk.TreeViewColumn("lessonNo",cell,text = 0)
        #noColumn.set_max_width(70)

        lNameColumn = Gtk.TreeViewColumn("lessonName",cell,text = 1)
        #lNameColumn.set_max_width(70)

        tNameColumn = Gtk.TreeViewColumn("teacherName",cell,text = 2)
        #tNameColumn.set_max_width(70)

        interestColumn = Gtk.TreeViewColumn("TeacherInterest",cell,text = 3)
        #interestColumn.set_max_width(70)
        regColumn = Gtk.TreeViewColumn("Teacher Reg No",cell,text = 4)
               
        self.StudentLTree.append_column(noColumn)
        self.StudentLTree.append_column(lNameColumn)
        self.StudentLTree.append_column(tNameColumn)
        self.StudentLTree.append_column(interestColumn)
        self.StudentLTree.append_column(regColumn)

        #check button stunu oluşturma işlemi
        #uygun hücre oluşturma
        check_cell = Gtk.CellRendererToggle()
        #hücre içi widget fonksiyon bağlantısı
        check_cell.connect("toggled", self.requestClicked,5)
        #satır oluşturma 1. satır adı 2. hücre tipi
        t_column = Gtk.TreeViewColumn(" Request ",check_cell)
        #stuna argümanları dışarda bu fonksiyonla da verebilirsin
        t_column.add_attribute(check_cell,"active",5)
        #t_column.set_max_width(30)

        #stun treeview ekleme işlemi
        self.StudentLTree.append_column(t_column)

        #yeni satırlar oluşturma
        #self.iSongStore.append(["song_name",True,"url"])
        l_scrolled = Gtk.ScrolledWindow()
        box.pack_start(l_scrolled,1,1,10)
        l_scrolled.add(self.StudentLTree)

        self.updateListStore()

        label = Gtk.Label(label="This is a dialog to display additional information")

        self.lessonNoEntery = Gtk.Entry()
        self.lessonNoEntery.set_placeholder_text(" Lesson NO ")
        box.pack_start(self.lessonNoEntery,0,0,5)

        self.filterButton = Gtk.Button()
        self.filterButton.set_label("Filter")
        self.filterButton.connect("clicked",self.filterButtonC)
        box.pack_start(self.filterButton,0,0,5)

        interests = [
            "None",
            "OS",
            "AI"
        ]
        self.intcombo = Gtk.ComboBoxText()
        self.intcombo.set_entry_text_column(0)
        self.intcombo.connect("changed", self.on_int_combo_changed)
        for interest in interests:
            self.intcombo.append_text(interest)

        box.pack_start(self.intcombo, False, False, 5)

        box.add(label)
        self.show_all()

    def updateListStore(self):
        self.StudentLStore.clear()
        print(type(self.parent.parent.ActiveNo))
        activeNo = self.parent.parent.ActiveNo
        ActiveLessons = sqlLib.getActiveLessons()
        print(ActiveLessons)
        for lesson in ActiveLessons:
            teacherData = sqlLib.getTeacherDataReg(int(lesson[3]))[0]
            lessonData = []
            reqData = []
            #print("lesson : ",lesson)
            lessonData.append(str(lesson[1]))
            lessonData.append(str(lesson[2]))
            #print(lesson[3])
            #print(teacherData)
            lessonData.append(str(teacherData[2] + teacherData[3]))
            lessonData.append(str(teacherData[5]))
            lessonData.append(str(teacherData[1]))

            
            reqData.append(lessonData[0])
            reqData.append(lessonData[4])
            reqData.append(sqlLib.getStudentData(self.parent.parent.ActiveNo)[1])
            found = False
            lessonSellected = False
            for req in sqlLib.getReqs():
                print(req)      
                reqD = []
                reqD.append(str(req[3]))
                reqD.append(str(req[2]))
                reqD.append(req[1])
                
                print(reqData)      
                print(reqD)      
                if reqD == reqData:
                    print("\nfounded !\n")
                    lessonData.append(True)
                    found = True
                    break
            if not found:
                lessonData.append(False)

            print(self.noFilter, lessonData[0])
            if self.noFilter != None:
                lessonSellected = True
                if lessonData[0] != self.noFilter:
                    print("not sellected lesson")
                    lessonSellected = False
            else:
                lessonSellected = True

            if self.intFilter != None:
                teacherInterest = sqlLib.getInterest(teacherData[0],"teacher")[0].split(" ")
                for i in teacherInterest:
                    if i != self.intFilter:
                        print("not interested")
                    else:
                        if lessonSellected:
                            self.StudentLStore.append([*lessonData])
                            break
            else:
                if lessonSellected:
                    self.StudentLStore.append([*lessonData])

    def requestClicked(self,widget,path, column):
        if path is not None:
            iter = self.StudentLStore.get_iter(path)
            print(self.StudentLStore[iter][column])
            self.StudentLStore[iter][column]= not self.StudentLStore[iter][column]

            lessonData = []
            for i in range(0,column+1):
                lessonData.append(self.StudentLStore[iter][i])
            print(lessonData)
            print("requested")
            lessonNo = lessonData[0]
            regNo = lessonData[4]
            print(sqlLib.getStudentData(self.parent.parent.ActiveNo))
            studentNo = sqlLib.getStudentData(self.parent.parent.ActiveNo)[1]

            #create req
            if self.StudentLStore[iter][column]:
                maxTeacherC = 1
                if sqlLib.getReqC(studentNo, lessonNo) < maxTeacherC:
                    self.createMessager(regNo)
                    sqlLib.newReq(studentNo, regNo, lessonNo)
                else:
                    print("No more request limit")
            #delete req
            else:
                sqlLib.delReq(studentNo, regNo, lessonNo)
        self.show_all()

    def createMessager(self,regNo):
        studentNo = sqlLib.getStudentData(self.parent.parent.ActiveNo)[1]
        print("here",regNo)
        self.dialog = Messager(self,studentNo, regNo)
        response = self.dialog.run()
        return response

    def filterButtonC(self,widget):
        lessonNo = self.lessonNoEntery.get_text()
        if lessonNo is not None:
            print("Selected: currency=%s" % lessonNo)
            if lessonNo == "":
                self.noFilter = None
            else:    
                self.noFilter = lessonNo
            print("Filter : ",self.noFilter)
        text = self.intcombo.get_active_text()
        if text is not None:
            print("Selected: currency=%s" % text)
            if text == "None":
                self.intFilter = None
            else:    
                self.intFilter = text
            print("Filter : ",self.intFilter)
            self.updateListStore()

    def on_int_combo_changed(self, widget):
        print("changed")


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
            self.parent.updateStudentInfo(None,None)
            sqlLib.getAllSL()

        elif info == TARGET_ENTRY_PIXBUF:
            pixbuf = data.get_pixbuf()
            width = pixbuf.get_width()
            height = pixbuf.get_height()

            print("Received pixbuf with width %spx and height %spx" % (width, height))

        else:
            print("unknown recieved")



class Messager(Gtk.Dialog):
    def __init__(self, parent, studentNo, regNo):
        super().__init__(title=" Messager ")
        self.parent = parent
        self.set_default_size(650, 600)
        box = self.get_content_area()
        self.studentNo = studentNo
        self.regNo = regNo

        self.maxLen = 100

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        box.pack_start(scrolledwindow, 0, 1, 5)

        self.textview = Gtk.TextView()
        self.textbuffer = self.textview.get_buffer()
        self.textbuffer.set_text(
            " Wirte Your Message Here "
        )
        scrolledwindow.add(self.textview)

        self.sendButton = Gtk.Button()
        self.sendButton.set_label("Send")
        self.sendButton.connect("clicked",self.sendC)
        box.pack_start(self.sendButton,0,0,5)

        self.show_all()

    def sendC(self, widget):
        start_iter = self.textbuffer.get_start_iter()
        end_iter = self.textbuffer.get_end_iter()
        text = self.textbuffer.get_text(start_iter, end_iter, True)
        leng = len(text)
        print(leng)
        if leng < self.maxLen:
            print(text)
            sqlLib.sendMessage(self.studentNo, self.regNo, text)
            sqlLib.getMessages(self.regNo,"teacher")
        else:
            print("error too big data to send")
