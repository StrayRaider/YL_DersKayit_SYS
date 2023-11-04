from libs import sqlLib, window
import psycopg2

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

sqlLib.connect()


#sqlLib.dropLogIn()
#sqlLib.droptable("ActiveLessons")
sqlLib.createLogIn()
sqlLib.createMessages()
sqlLib.createReq()
sqlLib.createStudentTable()
sqlLib.createActiveLessons()
#sqlLib.droptable("Teachers")
sqlLib.createTeacherTable()
sqlLib.createAcceptedLessons()
sqlLib.droptable("Root")
sqlLib.createRootTable()
sqlLib.setRootData(1,100,300)

#sqlLib.droptable("Lessons")
#sqlLib.createLessons()
#sqlLib.createStudentsLessons()

sqlLib.getAllSL()

sqlLib.createNewUser("root", "root","root")
sqlLib.createNewUser("emre", "1234","student")

if(sqlLib.LogIn("root", "root", "root")):
    print("root loginnig")

if(sqlLib.LogIn("emre", "1234", "student")):
    print("root loginnig")



win = window.MyWindow()
win.connect("destroy", window.quit_app)
win.show_all()
Gtk.main()

sqlLib.closeDB()
