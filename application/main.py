from libs import sqlLib, window
import psycopg2

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk






sqlLib.connect()

#LogIn

sqlLib.createLogIn()

sqlLib.createNewUser(1234, "elif")

if(sqlLib.LogIn("emre", "123")):
    print("loginnig")


#cursor.execute("SELECT * FROM LogIn")
# it returns single line
# use fetchall instead
#print(cursor.fetchall())
#sqlLib.dropLogIn()


win = window.MyWindow()
win.connect("destroy", window.quit_app)
win.show_all()
Gtk.main()

sqlLib.closeDB()
