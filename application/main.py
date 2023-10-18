from libs import sqlLib
import psycopg2


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

