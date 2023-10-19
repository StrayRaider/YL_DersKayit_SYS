import psycopg2

def connect():
    conn = psycopg2.connect(database="DersKayitSys",
                        host="localhost",
                        user="postgres",
                        port="5432")
    return conn;

def createLogIn(cursor):
    createLogInTable = """ 
        CREATE TABLE IF NOT EXISTS LogIn (
        UserNo INT PRIMARY KEY,
        Password VARCHAR(255),
        UserId VARCHAR(255))
     """
    try:
        cursor.execute(createLogInTable)
    except:
        print("error createing log in table")


def dropLogIn(cursor):
    dropLogIn = """ DROP TABLE LogIn """
    cursor.execute(dropLogIn)

def createNewUser(cursor, passwd, userName):
    UserNo = genUserNo(cursor)
    print(UserNo)
    ınsertNew = """ INSERT INTO LogIn VALUES ({},'{}' ,'{}');  """.format(UserNo, passwd, userName)
    cursor.execute(ınsertNew)

def LogIn(cursor, Id, Password):
    IdPassword = """ SELECT * FROM LogIn WHERE UserId = '{}' and Password = '{}' """.format(Id, Password)
    cursor.execute(IdPassword)
    data = cursor.fetchone()
    print(data)
    if(data != None):
        return True
    else:
        return False

def genUserNo(cursor):
    cursor.execute("SELECT * FROM LogIn")
    idList = []
    try:
        for user in  cursor.fetchall():
            idList.append(user[0])
        return max(idList) + 1 
    except:
        print("error no user No founded")
        return 1
 
