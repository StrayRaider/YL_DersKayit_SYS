from libs import sqlLib
import psycopg2

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class MyWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Youtube Installation")
        self.main_box = Gtk.HBox()
        self.add(self.main_box)


def quit_app(arg):
    print("quiting..")
    Gtk.main_quit()
    print("All Done")

win = MyWindow()
win.connect("destroy", quit_app)
win.show_all()
Gtk.main()





conn = sqlLib.connect();
cursor = conn.cursor()

#LogIn

sqlLib.createLogIn(cursor)

sqlLib.createNewUser(cursor, 1234, "elif")

if(sqlLib.LogIn(cursor, "emre", "123")):
    print("loginnig")


cursor.execute("SELECT * FROM LogIn")

# it returns single line
# use fetchall instead
print(cursor.fetchall())


sqlLib.dropLogIn(cursor)

conn.commit()
cursor.close()
conn.close()

