import gi
from libs import sqlLib, student

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

        self.messageLabel = Gtk.Label("message : ")
        self.pack_start(self.messageLabel,0,0,5)

        #self.connect("draw",self.updateMessages)
        print(self.parent.ActiveNo)


        self.reqLB = Gtk.Button()
        self.reqLB.set_label("Requests")
        self.reqLB.connect("clicked",self.reqLBC)
        self.pack_start(self.reqLB,0,0,5)

        self.reqAB = Gtk.Button()
        self.reqAB.set_label("Requset Sendable Students")
        self.reqAB.connect("clicked",self.reqABC)
        self.pack_start(self.reqAB,0,0,5)


        self.MessageB = Gtk.Button()
        self.MessageB.set_label("Message")
        self.MessageB.connect("clicked",self.updateMessages)
        self.pack_start(self.MessageB,0,0,5)

        self.regEntery = Gtk.Entry()
        self.regEntery.set_placeholder_text(" Sicil ")
        self.pack_start(self.regEntery,0,0,5)



    def updateMessages(self,widget):
        regNo = sqlLib.getTeacherData(self.parent.ActiveNo)[0][1]
        sqlLib.getStudentsNoReqForTeacher(regNo)

        self.dialog = readMessages(self,regNo,"teacher")
        response = self.dialog.run()



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

    def reqLBC(self,widget):
        regNo = sqlLib.getTeacherData(self.parent.ActiveNo)[0][1]
        self.dialog = reqAndMessages(self,regNo)
        response = self.dialog.run()

    def reqABC(self,widget):
        self.dialog = reqAbleStudents(self)
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

        self.newLessonB = Gtk.Button()
        self.newLessonB.set_label("New Lesson")
        self.newLessonB.connect("clicked",self.newLesson)
        box.pack_start(self.newLessonB,0,0,5)

        self.show_all()

    def newLesson(self, widget):
        tData = sqlLib.getTeacherData(self.parent.parent.ActiveNo)[0]
        print("tData : ",tData)
        text = self.nameEntery.get_text()
        if text is not None:
            print("Selected: currency=%s" % text)
            sqlLib.createNewLesson(text, sqlLib.genLessonNo(text) ,tData[1])

class InterestDialog(Gtk.Dialog):
    def __init__(self, parent,role="teacher"):
        super().__init__(title="Interest")
        self.role = role
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

        interests = sqlLib.getInterest(self.parent.parent.ActiveNo,self.role)

        self.label = Gtk.Label(interests)
        box.pack_start(self.label,0,0,5)

        self.newIntB = Gtk.Button()
        self.newIntB.set_label("New Interest")
        self.newIntB.connect("clicked",self.newIntC)
        box.pack_start(self.newIntB,0,0,5)

        self.show_all()


    def newIntC(self,widget):
        text = self.intcombo.get_active_text()
        if text is not None:
            print("Selected: currency=%s" % text)
            #add interest to teacher
            print(self.role)
            sqlLib.setInterest(self.parent.parent.ActiveNo, self.role, text)
            interests = sqlLib.getInterest(self.parent.parent.ActiveNo,self.role)
            self.label.set_text(str(interests))

    def on_int_combo_changed(self, widget):
        text = self.intcombo.get_active_text()
        if text is not None:
            print("Selected: currency=%s" % text)

class reqAndMessages(Gtk.Dialog):
    def __init__(self, parent,regNo):
        super().__init__(title="Student Requests")
        self.parent = parent
        self.regNo = regNo
        self.set_default_size(650, 600)
        box = self.get_content_area()

        self.intFilter = None
        self.noFilter = None

        # lessonNo, lessonName, StudentNo
        self.StudentLStore = Gtk.ListStore(str,str,str,bool)
        self.StudentLTree = Gtk.TreeView(self.StudentLStore)

        cell = Gtk.CellRendererText()
        cell.set_property("editable", True) #eğer tect değiştirilebilir olsun istersen

        noColumn = Gtk.TreeViewColumn("lessonNo",cell,text = 0)
        #noColumn.set_max_width(70)

        lNameColumn = Gtk.TreeViewColumn("lessonName",cell,text = 1)
        #lNameColumn.set_max_width(70)

        sNoColumn = Gtk.TreeViewColumn("StudentNo",cell,text = 2)
        #tNameColumn.set_max_width(70)

               
        self.StudentLTree.append_column(noColumn)
        self.StudentLTree.append_column(lNameColumn)
        self.StudentLTree.append_column(sNoColumn)

        check_cell = Gtk.CellRendererToggle()
        check_cell.connect("toggled", self.acceptClicked,3)
        t_column = Gtk.TreeViewColumn(" Accept ",check_cell)
        t_column.add_attribute(check_cell,"active",3)

        self.StudentLTree.append_column(t_column)

        check_cell = Gtk.CellRendererToggle()
        check_cell.connect("toggled", self.rejectClicked,4)
        t_column = Gtk.TreeViewColumn(" Reject ",check_cell)
        t_column.add_attribute(check_cell,"active",4)

        self.StudentLTree.append_column(t_column)

        #yeni satırlar oluşturma
        #self.iSongStore.append(["song_name",True,"url"])
        l_scrolled = Gtk.ScrolledWindow()
        box.pack_start(l_scrolled,1,1,10)
        l_scrolled.add(self.StudentLTree)

        self.updateListStore()

        label = Gtk.Label(label="This is a dialog to display additional information")

        box.add(label)
        self.show_all()

    def updateListStore(self):
        self.StudentLStore.clear()
        print(type(self.parent.parent.ActiveNo))
        activeNo = self.parent.parent.ActiveNo
        for req in sqlLib.getReqs(self.regNo):
            print(req)      
            reqD = []
            reqD.append(str(req[3]))
            # get lesson Name
            reqD.append(str(sqlLib.getLessonName(req[3])[0][0]))
            reqD.append(str(req[1]))
              
            print(reqD)      
        try:
            self.StudentLStore.append([*reqD, False])
        except:
            print("no request founded")

    def acceptClicked(self,widget,path, column):
        iter = self.StudentLStore.get_iter(path)
        reqData = []
        for i in range(0,column+1):
            reqData.append(self.StudentLStore[iter][i])
        print(reqData)
        print("Accepted")
        regNo = sqlLib.getTeacherData(self.parent.parent.ActiveNo)[0][1]
        sqlLib.delLessonReq(reqData[2], reqData[0])
        sqlLib.acceptLesson(reqData[2],regNo,reqData[0])

            #create req
            #if self.StudentLStore[iter][column]:
                #self.createMessager(regNo)
                #sqlLib.newReq(studentNo, regNo, lessonNo)
            #delete req
            #else:
        self.show_all()
        self.updateListStore()

    def rejectClicked(self,widget,path,column):
        iter = self.StudentLStore.get_iter(path)
        reqData = []
        for i in range(0,column):
            reqData.append(self.StudentLStore[iter][i])
        regNo = sqlLib.getTeacherData(self.parent.parent.ActiveNo)[0][1]
        sqlLib.delLessonReq(reqData[2], reqData[0])

        self.show_all()
        self.updateListStore()

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



class readMessages(Gtk.Dialog):
    def __init__(self, parent,number, role):
        super().__init__(title="My Messages")
        self.parent = parent
        self.set_default_size(650, 600)
        box = self.get_content_area()
        self.set_border_width(10)

        l_scrolled = Gtk.ScrolledWindow()
        box.pack_start(l_scrolled,1,1,10)

        box_outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        l_scrolled.add(box_outer)

        listbox = Gtk.ListBox()
        listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        box_outer.pack_start(listbox, True, True, 0)


        print(" ")
        #print(self.parent.ActiveNo)
        #print("reg : ",regNo)
        if number:
            message = sqlLib.getMessages(number, role)
            txtmessage = ""
            for i in message:
                txtmessage = txtmessage + str(i)
                #print(txtmessage)
                #self.messageLabel.set_text("message : " + txtmessage)

                row = Gtk.ListBoxRow()
                hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
                row.add(hbox)
                vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
                hbox.pack_start(vbox, True, True, 0)

                label2 = Gtk.Label(label=str(i), xalign=0)
                vbox.pack_start(label2, True, True, 0)

                listbox.add(row)
        self.show_all()







class reqAbleStudents(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Req Able Students")
        self.parent = parent
        self.set_default_size(650, 600)
        box = self.get_content_area()

        #Student No, Name+Surname
        self.StudentLStore = Gtk.ListStore(str,str,bool)
        self.StudentLTree = Gtk.TreeView(self.StudentLStore)

        cell = Gtk.CellRendererText()
        cell.set_property("editable", True) #eğer tect değiştirilebilir olsun istersen

        noColumn = Gtk.TreeViewColumn("lessonNo",cell,text = 0)

        lNameColumn = Gtk.TreeViewColumn("lessonName",cell,text = 1)

        self.StudentLTree.append_column(noColumn)
        self.StudentLTree.append_column(lNameColumn)

        check_cell = Gtk.CellRendererToggle()
        check_cell.connect("toggled", self.requestClicked,2)
        t_column = Gtk.TreeViewColumn(" Request ",check_cell)
        t_column.add_attribute(check_cell,"active",2)

        self.StudentLTree.append_column(t_column)

        l_scrolled = Gtk.ScrolledWindow()
        box.pack_start(l_scrolled,1,1,10)
        l_scrolled.add(self.StudentLTree)

        self.updateListStore()

        label = Gtk.Label(label="This is a dialog to display additional information")

        box.add(label)
        self.show_all()

    def updateListStore(self):
        self.StudentLStore.clear()
        print(type(self.parent.parent.ActiveNo))
        activeNo = self.parent.parent.ActiveNo
        regNo = sqlLib.getTeacherData(self.parent.parent.ActiveNo)[0][1]
        students = sqlLib.getStudentsNoReqForTeacher(regNo)
        for studentUNo in students:
            studentData = sqlLib.getStudentData(studentUNo)
            lessonData = []
            reqData = []
            #print("lesson : ",lesson)
            lessonData.append(str(studentData[1]))
            lessonData.append(str(studentData[2] + " " + studentData[3]))
            lessonData.append(False)
            self.StudentLStore.append([*lessonData])

    def requestClicked(self,widget,path, column):
        if path is not None:
            iter = self.StudentLStore.get_iter(path)
            print(self.StudentLStore[iter][column])
            self.StudentLStore[iter][column]= not self.StudentLStore[iter][column]

            studentData = []
            for i in range(0,column+1):
                studentData.append(self.StudentLStore[iter][i])
            print(studentData)
            print("requested")
            studentNo = studentData[0]

            if self.StudentLStore[iter][column]:
                regNo = sqlLib.getTeacherData(self.parent.parent.ActiveNo)[0][1]
                self.createMessager(studentNo)
                #req tablosuna ters datalarla gönderim yapılacak
                sqlLib.newReq(regNo, studentNo, lessonNo)
            else:
                sqlLib.delReq(regNo,studentNo, lessonNo)
        self.show_all()

    def createMessager(self,studentNo):
        regNo = sqlLib.getTeacherData(self.parent.parent.ActiveNo)[0][1]
        print("here",regNo)
        self.dialog = student.Messager(self,studentNo, regNo)
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

