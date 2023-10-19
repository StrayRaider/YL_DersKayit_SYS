import psycopg2

conn = None
cursor = None

def connect():
    global conn
    global cursor
    conn = psycopg2.connect(database="DersKayitSys",
                        host="localhost",
                        user="postgres",
                        port="5432")
    cursor = conn.cursor()

def createLogIn():
    createLogInTable = """ 
        CREATE TABLE IF NOT EXISTS LogIn (
        UserNo INT PRIMARY KEY,
        Password VARCHAR(255),
        UserId VARCHAR(255),
        UserRole VARCHAR(255))
     """
    try:
        cursor.execute(createLogInTable)
    except:
        print("error createing log in table")


def dropLogIn():
    dropLogIn = """ DROP TABLE LogIn """
    cursor.execute(dropLogIn)

def createNewUser(userName, passwd,role):
    UserNo = genUserNo()
    print(UserNo)
    if LogIn(userName, passwd, role):
        print("error this user is allready exist")
    else:
        ınsertNew = """ INSERT INTO LogIn VALUES ({},'{}' ,'{}', '{}');  """.format(UserNo, passwd, userName, role)
        cursor.execute(ınsertNew)

def LogIn( Id, Password, role):
    IdPassword = """ SELECT * FROM LogIn WHERE UserId = '{}' and Password = '{}' and UserRole = '{}'""".format(Id, Password, role)
    cursor.execute(IdPassword)
    data = cursor.fetchone()
    print(data)
    if(data != None):
        return True
    else:
        return False

def genUserNo():
    cursor.execute("SELECT * FROM LogIn")
    idList = []
    try:
        for user in  cursor.fetchall():
            idList.append(user[0])
        return max(idList) + 1 
    except:
        print("error no user No founded")
        return 1
 
def closeDB():
    conn.commit()
    cursor.close()
    conn.close()
