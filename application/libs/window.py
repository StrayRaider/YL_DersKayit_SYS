from libs import way, student, teacher, root, logIn
from gi.repository import Gtk

class MyWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title=" Proje Dersi Kayıt Sistemi ")

        self.stack = Gtk.Stack()
        self.add(self.stack)
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.stack.set_transition_duration(3000)
        self.stack.add_titled(way.WayWin(self),"way_select","choice_screen")
        self.stack.add_titled(root.RootWin(self),"root_way","choice_screen")
        self.stack.add_titled(student.StudentWin(self),"student_way","choice_screen")
        self.stack.add_titled(teacher.TeacherWin(self),"teacher_way","choice_screen")
        self.stack.add_titled(logIn.LogInWin(self),"LogIn_way","choice_screen")
        self.way = ""

        self.main_box = Gtk.HBox()
        self.add(self.main_box)
        left_box = Gtk.Box()
        right_box = Gtk.Box()
        mid_box = Gtk.Box()
        self.main_box.pack_start(left_box,1,1,10)
        self.main_box.pack_start(mid_box,1,1,10)
        self.main_box.pack_start(right_box,1,1,10)

        #student button
        self.button = Gtk.Button(label=" Student LogIn ")
        left_box.pack_start(self.button,0,0,10)
        self.button.connect("clicked", self.studentLogIn)

        self.button = Gtk.Button(label=" Student LogIn ")
        mid_box.pack_start(self.button,0,0,10)
        self.button.connect("clicked", self.studentLogIn)

        self.button = Gtk.Button(label=" Student LogIn ")
        right_box.pack_start(self.button,0,0,10)
        self.button.connect("clicked", self.studentLogIn)


        #treeview ve list store oluşturulması
        #list store oluştururken sütunların hangi tipte değişken tutacağı belirtilir
        self.iSongStore = Gtk.ListStore(str,bool,str,bool)
        self.iSongTree = Gtk.TreeView(self.iSongStore)
        #içinde tutacağı değişken tipine göre bölme oluşturulması
        cell = Gtk.CellRendererText()
        cell.set_property("editable", True) #eğer tect değiştirilebilir olsun istersen
        #stun tanımlama işlemi 1. argüman stun adı, 2. tutacağı hücre tipi 3, ekleme
        #yaparken listenin kaçıncı argümanını alacağı
        column = Gtk.TreeViewColumn("Song To Download",cell,text = 0)
        column.set_max_width(200)
        u_column = Gtk.TreeViewColumn("Url",cell,text = 2)

        #check button stunu oluşturma işlemi
        #uygun hücre oluşturma
        check_cell = Gtk.CellRendererToggle()
        del_cell = Gtk.CellRendererToggle()
        #hücre içi widget fonksiyon bağlantısı
        #check_cell.connect("toggled", self.tree_but_toggle,1,"i")
        #del_cell.connect("toggled", self.del_tree_obj,3,"i")
        #satır oluşturma 1. satır adı 2. hücre tipi
        t_column = Gtk.TreeViewColumn("->",check_cell)
        del_column = Gtk.TreeViewColumn("del",del_cell)
        #stuna argümanları dışarda bu fonksiyonla da verebilirsin
        t_column.add_attribute(check_cell,"active",1)
        u_column.set_max_width(70)
        t_column.set_max_width(30)
        del_column.set_max_width(30)

        #stun treeview ekleme işlemi
        self.iSongTree.append_column(t_column)
        self.iSongTree.append_column(del_column)
        self.iSongTree.append_column(u_column)
        self.iSongTree.append_column(column)
 
        #yeni satırlar oluşturma
        #self.iSongStore.append(["song_name",True,"url"])
        l_scrolled = Gtk.ScrolledWindow()
        left_box.pack_start(l_scrolled,1,1,10)
        l_scrolled.add(self.iSongTree)


    def studentLogIn(widget,signal):
        print("student login")


def quit_app(arg):
    print("quiting..")
    Gtk.main_quit()
    print("All Done")

