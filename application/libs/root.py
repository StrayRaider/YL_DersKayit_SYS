import gi, random
from libs import sqlLib, dialogs

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class RootWin(Gtk.VBox):
    def __init__(self,parent):
        Gtk.VBox.__init__(self)
        self.parent = parent
        self.label = Gtk.Label("Root Win")
        self.pack_start(self.label,0,0,5)

        self.connect("draw",self.updateTime)
        
        self.newUserB = Gtk.Button()
        self.newUserB.set_label("New User")
        self.newUserB.connect("clicked",self.newUserC)
        
        self.pack_start(self.newUserB,0,0,5)

        self.allStudentsB = Gtk.Button()
        self.allStudentsB.set_label("Student Datas")
        self.allStudentsB.connect("clicked",self.allStudentsC)

        self.allUsersB = Gtk.Button()
        self.allUsersB.set_label("User Datas")
        self.allUsersB.connect("clicked",self.allUsersBC)
        self.pack_start(self.allUsersB,0,0,5)

        self.turnbackB = Gtk.Button()
        self.turnbackB.set_label("Back")
        self.turnbackB.connect("clicked",self.turnbackBC)
        self.pack_start(self.turnbackB,0,0,5)

        self.hBox = Gtk.HBox()
        self.reqlabel = Gtk.Label("Req Limit")
        self.hBox.pack_start(self.reqlabel,0,0,5)

        self.reqEntery = Gtk.Entry()
        self.reqEntery.set_placeholder_text(" Req Limit ")
        self.hBox.pack_start(self.reqEntery,0,0,5)
        self.pack_start(self.hBox, 0,0,5)

        self.hBox = Gtk.HBox()
        self.messagelabel = Gtk.Label("Message Len Limit")
        self.hBox.pack_start(self.messagelabel,0,0,5)

        self.mesLEntery = Gtk.Entry()
        self.mesLEntery.set_placeholder_text(" Message Len Limit ")
        self.hBox.pack_start(self.mesLEntery,0,0,5)
        self.pack_start(self.hBox, 0,0,5)

        hBox = Gtk.HBox()
        timeoutlabel = Gtk.Label("Set Timeout")
        hBox.pack_start(timeoutlabel,0,0,5)

        self.timeoutEntery = Gtk.Entry()
        self.timeoutEntery.set_placeholder_text(" Timeout ")
        hBox.pack_start(self.timeoutEntery,0,0,5)

        self.updateButton = Gtk.Button()
        self.updateButton.set_label("Update Root Data")
        self.updateButton.connect("clicked",self.updateButtonC)
        hBox.pack_start(self.updateButton,0,0,5)

        self.pack_start(hBox, 0,0,5)

        self.hBox = Gtk.HBox()

        self.studentCEntery = Gtk.Entry()
        self.studentCEntery.set_placeholder_text(" Create Student Count")
        self.hBox.pack_start(self.studentCEntery,0,0,5)
        self.pack_start(self.hBox, 0,0,5)

        self.createS = Gtk.Button()
        self.createS.set_label("Create Student")
        self.createS.connect("clicked",self.createSC)
        self.hBox.pack_start(self.createS,0,0,5)

        rootD = sqlLib.getRootData()
        if rootD != []:
            self.reqEntery.set_text(str(rootD[0][1]))
            self.mesLEntery.set_text(str(rootD[0][2]))
            self.timeoutEntery.set_text(str(rootD[0][3]))

        
        self.pack_start(self.allStudentsB,0,0,5)

        self.fillS = Gtk.Button()
        self.fillS.set_label("Create Student")
        self.fillS.connect("clicked",self.fillBC)
        self.pack_start(self.fillS,0,0,5)

    def fillBC(self, widget):
        self.dialog = fillStudentDialog(self)
        response = self.dialog.run()
        self.dialog.destroy()

    def updateTime(self,widget,cr):
        rootTime = sqlLib.getRootData()[0][3]
        timeO = rootTime-self.parent.activeTime
        if timeO >= 0:
            self.label.set_text("Root Win"+" Timeout : {}".format(timeO))
        else:
            if self.parent.isEnded == False:
                dialog = dialogs.textMessage(self,"Time Ended ")
                response = dialog.run()
                dialog.destroy()
                self.parent.isEnded = True

    def allUsersBC(self, widget):
        self.dialog = allUsersDialog(self)
        response = self.dialog.run()
        self.dialog.destroy()

    def createSC(self, widget):
        studentC = self.studentCEntery.get_text()
        sqlLib.createRandomStudent(studentC)

    def updateButtonC(self, widget):
        reqL = self.reqEntery.get_text()
        messageL = self.mesLEntery.get_text()
        timeout = self.timeoutEntery.get_text()
        sqlLib.setRootData(reqL,messageL,timeout)
        

    def turnbackBC(self,widget):
        self.parent.stack.set_visible_child_name("way_select")
        sqlLib.closeDB()
        sqlLib.connect()

    def newUserC(self,widget):
        self.dialog = NewUserDialog(self)
        response = self.dialog.run()
        if response == Gtk.ResponseType.OK:
            print("The OK button was clicked")
            self.dialog.destroy()

    def allStudentsC(self,widget):
        self.dialog = allStudentsDialog(self)
        response = self.dialog.run()
        if response == Gtk.ResponseType.OK:
            print("The OK button was clicked")
            self.dialog.destroy()
    

class allStudentsDialog(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="My Lessons")
        box = self.get_content_area()
        self.parent = parent
        self.set_default_size(650, 600)


        self.StudentStore = Gtk.ListStore(str,str,str,str,str,str,str)
        self.StudentTree = Gtk.TreeView(self.StudentStore)
        #içinde tutacağı değişken tipine göre bölme oluşturulması
        cell = Gtk.CellRendererText()
        cell.set_property("editable", True) #eğer tect değiştirilebilir olsun istersen
        #stun tanımlama işlemi 1. argüman stun adı, 2. tutacağı hücre tipi 3, ekleme
        #yaparken listenin kaçıncı argümanını alacağı

        #datas : number, name, surname, avarageGrade, transkriptPath

        unoColumn = Gtk.TreeViewColumn("User No",cell,text = 0)
        unoColumn.set_max_width(100)

        noColumn = Gtk.TreeViewColumn("Student Number",cell,text = 1)
        noColumn.set_max_width(100)

        nameColumn = Gtk.TreeViewColumn("Name",cell,text = 2)
        nameColumn.set_max_width(100)

        snameColumn = Gtk.TreeViewColumn("SurName",cell,text = 3)
        snameColumn.set_max_width(100)

        transkriptColumn = Gtk.TreeViewColumn("Transkript Path",cell,text = 4)
        transkriptColumn.set_max_width(170)
        
        gradeColumn = Gtk.TreeViewColumn("GradeAvarage",cell,text = 5)
        gradeColumn.set_max_width(100)

        gradeColumn = Gtk.TreeViewColumn("Interest",cell,text = 6)
        gradeColumn.set_max_width(100)



        self.StudentTree.append_column(noColumn)
        self.StudentTree.append_column(unoColumn)
        self.StudentTree.append_column(nameColumn)
        self.StudentTree.append_column(snameColumn)
        self.StudentTree.append_column(transkriptColumn)
        self.StudentTree.append_column(gradeColumn)

        l_scrolled = Gtk.ScrolledWindow()
        box.pack_start(l_scrolled,1,1,10)
        l_scrolled.add(self.StudentTree)

        try:
            for userNo in sqlLib.getStudents():
                print("userNo :",userNo)
                studentData = sqlLib.getStudentData(userNo)
                print(studentData)
                x = 0
                sData = []
                for i in studentData:
                    sData.append(str(studentData[x]))
                    x+=1
                self.StudentStore.append([*sData])
        except:
            pass

        self.show_all()

class NewTeacgerDialog(Gtk.Dialog):
    def __init__(self, parent, userNo):
        super().__init__(title="New Teacher")
        box = self.get_content_area()
        self.parent = parent
        self.userNo = userNo
        self.set_default_size(650, 600)

        self.regEntery = Gtk.Entry()
        self.regEntery.set_placeholder_text(" Sicil ")
        box.pack_start(self.regEntery,0,0,5)

        self.nameEntery = Gtk.Entry()
        self.nameEntery.set_placeholder_text(" Name ")
        box.pack_start(self.nameEntery,0,0,5)

        self.surnameEntery = Gtk.Entry()
        self.surnameEntery.set_placeholder_text(" Surname ")
        box.pack_start(self.surnameEntery,0,0,5)

        self.maxSEntery = Gtk.Entry()
        self.maxSEntery.set_placeholder_text(" Max Student ")
        box.pack_start(self.maxSEntery,0,0,5)

        self.newTeacherB = Gtk.Button()
        self.newTeacherB.set_label("Create User")
        self.newTeacherB.connect("clicked",self.createTeacherC)
        box.pack_start(self.newTeacherB,0,0,5)

        self.show_all()

    def createTeacherC(self, widget):
        reg = self.regEntery.get_text()
        name = self.nameEntery.get_text()
        surname = self.surnameEntery.get_text()
        maxS = self.maxSEntery.get_text()
        sqlLib.createnewTeacher(self.userNo, reg, name, surname, maxS)
        self.destroy()

class NewUserDialog(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="My Lessons")
        self.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK
        )
        box = self.get_content_area()
        self.parent = parent
        self.set_default_size(650, 600)

        self.idEntery = Gtk.Entry()
        self.idEntery.set_placeholder_text(" ID ")
        box.pack_start(self.idEntery,0,0,5)

        self.pwdEntery = Gtk.Entry()
        self.pwdEntery.set_placeholder_text(" Password ")
        box.pack_start(self.pwdEntery,0,0,5)

        self.logInB = Gtk.Button()
        self.logInB.set_label("Create User")
        self.logInB.connect("clicked",self.CreateC)
        box.pack_start(self.logInB,0,0,5)


	
        roles = [
            "student",
            "teacher"
        ]
        self.rolecombo = Gtk.ComboBoxText()
        self.rolecombo.set_entry_text_column(0)
        self.rolecombo.connect("changed", self.on_currency_combo_changed)
        for role in roles:
            self.rolecombo.append_text(role)

        self.rolecombo.set_active(0)
        box.pack_start(self.rolecombo, False, False, 0)

        self.show_all()

    def on_currency_combo_changed(self, widget):
        text = self.rolecombo.get_active_text()
        if text is not None:
            print("Selected: currency=%s" % text)

    def CreateC(self,widget):
        role = self.rolecombo.get_active_text()
        if role is not None:
            print("Selected: currency=%s" % role)
            userId = self.idEntery.get_text()
            userPwd = self.pwdEntery.get_text()
            userNo = sqlLib.createNewUser(userId, userPwd,role)
            if userNo != 0:
                if role == "teacher":
                    self.parent.dialog = NewTeacgerDialog(self.parent,userNo)
                    response = self.parent.dialog.run()
                self.destroy()



class allUsersDialog(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="My Lessons")
        box = self.get_content_area()
        self.parent = parent
        self.set_default_size(650, 600)


        self.StudentStore = Gtk.ListStore(str,str,str,str)
        self.StudentTree = Gtk.TreeView(self.StudentStore)
        #içinde tutacağı değişken tipine göre bölme oluşturulması
        cell = Gtk.CellRendererText()
        cell.set_property("editable", True) #eğer tect değiştirilebilir olsun istersen
        #stun tanımlama işlemi 1. argüman stun adı, 2. tutacağı hücre tipi 3, ekleme
        #yaparken listenin kaçıncı argümanını alacağı

        #datas : number, name, surname, avarageGrade, transkriptPath

        unoColumn = Gtk.TreeViewColumn("User No",cell,text = 0)
        unoColumn.set_max_width(100)

        noColumn = Gtk.TreeViewColumn("Password",cell,text = 1)
        noColumn.set_max_width(100)

        nameColumn = Gtk.TreeViewColumn("User ID",cell,text = 2)
        nameColumn.set_max_width(100)

        roleColumn = Gtk.TreeViewColumn("User Role",cell,text = 3)
        roleColumn.set_max_width(100)

        self.StudentTree.append_column(noColumn)
        self.StudentTree.append_column(unoColumn)
        self.StudentTree.append_column(nameColumn)
        self.StudentTree.append_column(roleColumn)

        l_scrolled = Gtk.ScrolledWindow()
        box.pack_start(l_scrolled,1,1,10)
        l_scrolled.add(self.StudentTree)

        #try:
        if 1:
            for userNo in sqlLib.getLogIn():
                print("userNo :",userNo)
                sData = []
                for i in userNo:
                    sData.append(str(i))
                self.StudentStore.append([*sData])
        #except:
        #    pass

        self.show_all()


class fillStudentDialog(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="My Lessons")
        box = self.get_content_area()
        self.parent = parent
        self.set_default_size(650, 600)

        ways = [
            "random",
        ]
        self.rolecombo = Gtk.ComboBoxText()
        self.rolecombo.set_entry_text_column(0)
        self.rolecombo.connect("changed", self.on_currency_combo_changed)
        for way in ways:
            self.rolecombo.append_text(way)
        box.pack_start(self.rolecombo,0,0,5)

        self.fillS = Gtk.Button()
        self.fillS.set_label("Create Student")
        self.fillS.connect("clicked",self.fillBC)
        box.pack_start(self.fillS,0,0,5)

        self.show_all()

    def on_currency_combo_changed(self,widget):
        pass

    def fillBC(self, widget):
        print("students are filling to all lessons")
        # tüm öğrencileri al
        # her öğrencinin tüm alabileceği dersleri bul
        # kontenjanı olan herhangi bir hocaya ata
        #tüm açılan dersleri bul

        # rec, lessonNo, name, regNo


        #her bir öğrenci için
        students = sqlLib.getStudents()
        for student in students:
            #açılan tüm dersleri al
            activeLessons = sqlLib.getActiveLessons()
            activeLessonNo = []
            for alesson in activeLessons:
                if alesson[1] not in activeLessonNo:
                    activeLessonNo.append(alesson[1])
            print(activeLessonNo)

            studentData = sqlLib.getStudentData(student) 
            if studentData:
                studentNo = studentData[1]
                print(studentData)
                acceptedL = sqlLib.getAcceptedLessonNo(studentNo)
                for studentsAles in acceptedL:
                    if studentsAles in activeLessonNo:
                        activeLessonNo.remove(studentsAles)
                print("new one",activeLessonNo)
            #alınacak ders
                for getLesson in activeLessonNo:
                    teachers = sqlLib.getActiveLessonTeachers(getLesson)
                    print(teachers,len(teachers))
                    randt = random.randint(0,len(teachers)-1)
                    regNo = teachers[randt]
                    counter = 0
                    while not sqlLib.isTeacherAbleToGet(regNo):
                        print("\n burada \n",regNo)
                        randt = random.randint(0,len(teachers)-1)
                        regNo = teachers[randt]
                        counter += 1
                        if counter > 20:
                            break

                    print("Reg No : ", regNo)
                    # for this lesson this reg no this student has accepted
                    sqlLib.acceptLesson(studentNo, regNo, getLesson)


        # her bir hoca için teachersL = sqlLib.getTeachersActiveL(regNo)


