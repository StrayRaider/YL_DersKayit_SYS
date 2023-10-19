from libs import sqlLib, window
import psycopg2

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

sqlLib.connect()

sqlLib.dropLogIn()
sqlLib.createLogIn()

sqlLib.createNewUser("root", "root","root")

if(sqlLib.LogIn("root", "root", "root")):
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
