import psycopg2
import re

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
    print("created No ",UserNo)
    if LogIn(userName, passwd, role):
        print("error this user is allready exist")
        return 0
    else:
        ınsertNew = """ INSERT INTO LogIn VALUES ('{}' , '{}' ,'{}', '{}');  """.format(UserNo, passwd, userName, role)
        cursor.execute(ınsertNew)
        return 1

def LogIn( Id, Password, role):
    IdPassword = """ SELECT UserNo FROM LogIn WHERE UserId = '{}' and Password = '{}' and UserRole = '{}'""".format(Id, Password, role)
    cursor.execute(IdPassword)
    data = cursor.fetchall()
    data = re.findall("[0-9]",str(data))
    if(data != None):
        return data
    else:
        return False

def getLogIn():
    IdPassword = """ SELECT * FROM LogIn"""
    cursor.execute(IdPassword)
    data = cursor.fetchall()
    print(data)

def genUserNo():
    cursor.execute("SELECT UserNo FROM LogIn")
    idList = []
    try:
        for user in  cursor.fetchall():
            idList.append(user[0])
        print("returned : ",max(idList) + 1 )
        return max(idList) + 1 
    except:
        print("error no user No founded")
        return 1

def getBig(table):
    cursor.execute("SELECT rec FROM {}".format(table))
    idList = []
    try:
        for user in  cursor.fetchall():
            idList.append(user[0])
        return max(idList) + 1 
    except:
        print("error no user No founded")
        return 1

def createLessons():
    create = """ 
        CREATE TABLE IF NOT EXISTS Lessons (
        LessonNo INT PRIMARY KEY,
        LessonName VARCHAR(255))
     """
    try:
        cursor.execute(create)
    except:
        print("error createing lessons table")

def createStudentsLessons():
    create = """ 
        CREATE TABLE IF NOT EXISTS StudentsLessons (
        rec INT PRIMARY KEY,
        StudentNo INT,
        LessonNo INT,
        Note VARCHAR(2))
     """
    try:
        cursor.execute(create)
    except:
        print("error createing studentslesson table")

def NewStudentLessons(studentNo,lessonList):
    for lesson in lessonList:
        rec = getBig("StudentsLessons")
        lessonNo = lesson[0]
        try:
            lessonNote = lesson[1]
        except:
            pass
        if lessonNote == None:
            lessonNote == '--'
        ınsertNew = """ INSERT INTO StudentsLessons VALUES ({},'{}' ,'{}', '{}');  """.format(rec, studentNo[0],lessonNo, lessonNote)
        cursor.execute(ınsertNew)
    print("rec : ",rec)

def getAllSL():
    ınsertNew = """ SELECT * FROM StudentsLessons"""
    cursor.execute(ınsertNew)
    lessonList = cursor.fetchall()
    print("List : ",lessonList)

def getStudentsLessons(StudentNo):
    ınsertNew = """ SELECT * FROM StudentsLessons WHERE StudentNo = '{}'  """.format(StudentNo)
    cursor.execute(ınsertNew)
    lessonList = cursor.fetchall()
    print("List : ",lessonList)
    return lessonList
    
def createStudentTable():
    create = """ 
        CREATE TABLE IF NOT EXISTS Students (
        UserNo INT PRIMARY KEY,
        StudentNo INT,
        Name VARCHAR(50),
        SurName VARCHAR(50),
        TranskriptPath VARCHAR(255),
        Note VARCHAR(10))
     """
        #Interests VARCHAR(255),
        #DealRequestCount INT,
        #DealState VARCHAR(50),
    try:
        cursor.execute(create)
    except:
        print("error createing students table")


def createNewStudent(userNo, studentNo,name,surName, note,transkriptPath):
    ınsertNew = """ INSERT INTO Students VALUES ('{}' , '{}' ,'{}', '{}','{}','{}');  """.format(userNo, studentNo, name, surName, transkriptPath, note)
    cursor.execute(ınsertNew)

def getStudentData(userNo):
    if userNo != -1:
        ınsertNew = """ SELECT * FROM Students WHERE UserNo = '{}';  """.format(userNo)
        cursor.execute(ınsertNew)
        return cursor.fetchall()[0]


def createStudentTable():
    create = """ 
        CREATE TABLE IF NOT EXISTS Teachers (
        UserNo INT PRIMARY KEY,
        RegtNo INT,
        Name VARCHAR(50),
        SurName VARCHAR(50),
        TranskriptPath VARCHAR(255),
        Note VARCHAR(10))
     """
        #Interests VARCHAR(255),
        #DealRequestCount INT,
        #DealState VARCHAR(50),
    try:
        cursor.execute(create)
    except:
        print("error createing teachers table")




def closeDB():
    conn.commit()
    cursor.close()
    conn.close()
