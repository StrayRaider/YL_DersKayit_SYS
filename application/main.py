from libs import sqlLib, window
import psycopg2

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

sqlLib.connect()

#sqlLib.dropLogIn()
sqlLib.droptable("LogIn")
sqlLib.createLogIn()
sqlLib.createStudentTable()
sqlLib.createActiveLessons()
sqlLib.droptable("Teachers")
sqlLib.createTeacherTable()

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


#cursor.execute("SELECT * FROM LogIn")
# it returns single line
# use fetchall instead
#print(cursor.fetchall())



win = window.MyWindow()
win.connect("destroy", window.quit_app)
win.show_all()
Gtk.main()

sqlLib.closeDB()
