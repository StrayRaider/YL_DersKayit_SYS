import gi
from libs import sqlLib

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk




class RootWin(Gtk.VBox):
    def __init__(self,parent):
        Gtk.VBox.__init__(self)
        self.parent = parent
        self.label = Gtk.Label("Student Win")
        self.pack_start(self.label,0,0,5)
        
        self.newUserB = Gtk.Button()
        self.newUserB.set_label("New User")
        self.newUserB.connect("clicked",self.newUserC)
        
        self.pack_start(self.newUserB,0,0,5)

        self.allStudentsB = Gtk.Button()
        self.allStudentsB.set_label("New User")
        self.allStudentsB.connect("clicked",self.allStudentsC)
        
        self.pack_start(self.allStudentsB,0,0,5)


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
        sqlLib.createRandomStudent(3)
        box = self.get_content_area()
        self.parent = parent
        self.set_default_size(650, 600)


        self.StudentStore = Gtk.ListStore(str,str,str,str,str,str)
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



        self.StudentTree.append_column(noColumn)
        self.StudentTree.append_column(unoColumn)
        self.StudentTree.append_column(nameColumn)
        self.StudentTree.append_column(snameColumn)
        self.StudentTree.append_column(transkriptColumn)
        self.StudentTree.append_column(gradeColumn)

        l_scrolled = Gtk.ScrolledWindow()
        box.pack_start(l_scrolled,1,1,10)
        l_scrolled.add(self.StudentTree)


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

        self.show_all()



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
            if sqlLib.createNewUser(userId, userPwd,role):
                self.destroy()

