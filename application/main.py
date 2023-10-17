from libs import sqlLib
import psycopg2


conn = sqlLib.connect();
cursor = conn.cursor()


createLogInTable = """ 
    CREATE TABLE LogIn (
    UserNo INT PRIMARY KEY,
    Password VARCHAR(255),
    UserId VARCHAR(255))
 """

cursor.execute(createLogInTable)


ınsertNew = """ INSERT INTO LogIn VALUES ('1', 'emre');  """
cursor.execute(ınsertNew)

def LogIn(Id, Password):
    IdPassword = """ SELECT * FROM LogIn WHERE UserId = '{}' and Password = '{}' """.format(Id, Password)
    cursor.execute(IdPassword)
    print(cursor.fetchone())


LogIn("emre", "123")

command = """
    CREATE TABLE emre (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
)"""

cursor.execute(command)

ınsertNew = """ INSERT INTO emre VALUES ('1', 'emre');  """
cursor.execute(ınsertNew)

cursor.execute("SELECT * FROM emre WHERE id = 1")

# it returns single line
# use fetchall instead
print(cursor.fetchone())

