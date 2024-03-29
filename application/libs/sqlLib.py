import psycopg2
import re, random
from libs import dialogs

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

def getUserInfo(userNo):
    getdata = """ SELECT * FROM LogIn WHERE UserNo = '{}';""".format(userNo)
    cursor.execute(getdata)
    data = cursor.fetchall()
    data = re.findall("[0-9]+",str(data))
    if(data != None):
        return data
    else:
        return False

def dropLogIn():
    dropLogIn = """ DROP TABLE LogIn """
    cursor.execute(dropLogIn)

def droptable(table):
    dropLogIn = """ DROP TABLE {} """.format(table)
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
        closeDB()
        connect()
        return UserNo

def LogIn( Id, Password, role):
    IdPassword = """ SELECT UserNo FROM LogIn WHERE UserId = '{}' and Password = '{}' and UserRole = '{}'""".format(Id, Password, role)
    cursor.execute(IdPassword)
    data = cursor.fetchall()
    data = re.findall("[0-9]+",str(data))
    if(data != None):
        return data
    else:
        return False

def getLogIn():
    IdPassword = """ SELECT * FROM LogIn"""
    cursor.execute(IdPassword)
    data = cursor.fetchall()
    print(data)
    return data

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
    cursor.execute("SELECT rec FROM {};".format(table))
    idList = []
    try:
        for user in  cursor.fetchall():
            idList.append(user[0])
        return max(idList) + 1 
    except:
        print("error '{}' record".format(table))
        return 1

def createStudentsLessons():
    create = """ 
        CREATE TABLE IF NOT EXISTS StudentsLessons (
        rec INT PRIMARY KEY,
        StudentNo INT,
        LessonNo INT,
        Note VARCHAR(2),
        Name VARCHAR(255))
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
            lessonNote == '--'
        try:
            lessonName = lesson[2]
        except:
            lessonName == '--'
        ınsertNew = """ INSERT INTO StudentsLessons VALUES ({},'{}' ,'{}', '{}','{}');  """.format(rec, studentNo[0],lessonNo, lessonNote, lessonName)
        cursor.execute(ınsertNew)
    print("rec : ",rec)

def getAllSL():
    ınsertNew = """ SELECT * FROM StudentsLessons;"""
    cursor.execute(ınsertNew)
    lessonList = cursor.fetchall()
    print("List : ",lessonList)

def getAllSLessons():
    ınsertNew = """ SELECT * FROM StudentsLessons;"""
    cursor.execute(ınsertNew)
    lessonList = cursor.fetchall()
    lessons = []
    for lesson in lessonList:
        if lesson[2] not in lessons:
            lessons.append(lesson[2])
    print("List : ",lessons)
    return lessons

def getSLessonData(lessonNo):
    ınsertNew = """ SELECT * FROM StudentsLessons WHERE LessonNo = '{}';""".format(lessonNo)
    cursor.execute(ınsertNew)
    lessonList = cursor.fetchall()
    print("List : ",lessonList)
    return lessonList


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
        Note VARCHAR(10),
        Interests VARCHAR(255))
     """
        #Interests VARCHAR(255),
        #DealRequestCount INT,
        #DealState VARCHAR(50),
    try:
        cursor.execute(create)
    except:
        print("error createing students table")


def createNewStudent(userNo, studentNo,name,surName, note,transkriptPath):
    if getStudentData(userNo) != []:
        print("user exist")
    else:
        ınsertNew = """ INSERT INTO Students VALUES ('{}' , '{}' ,'{}', '{}','{}','{}');  """.format(userNo, studentNo, name, surName, transkriptPath, note)
        cursor.execute(ınsertNew)

def getStudentData(userNo):
    if userNo != -1:
        ınsertNew = """ SELECT * FROM Students WHERE UserNo = '{}';  """.format(userNo)
        cursor.execute(ınsertNew)
        try:
            data = cursor.fetchall()[0]
            return data
        except:
            return []

def createActiveLessons():
    create = """ 
        CREATE TABLE IF NOT EXISTS ActiveLessons (
        rec INT PRIMARY KEY,
        LessonNo INT,
        LessonName VARCHAR(50),
        RegNo INT)
     """
    try:
        cursor.execute(create)
    except:
        print("error createing activeLessons table")


def getStudents():
    students = """ SELECT UserNo FROM LogIn WHERE UserRole = '{}'  """.format("student")
    cursor.execute(students)
    students = cursor.fetchall()
    print("List : ", students)
    students = parseData(students)
    return students

def getStudentNos():
    students = getStudents()
    for userNo in students:
        print(userNo)
        studentData = getStudentData(userNo)
        print(studentData)
        x = 0
        sData = []
        for i in studentData:
            if x == 1:
                sData.append(str(studentData[x]))
                break
            x+=1
    return sData

def parseData(data):
    pdata = []
    for i in data:
        i = i[0]
        pdata.append(i)
    return pdata

def createRandomStudentsLessons(studentNo):
    allLessons = getAllSLessons()
    print("all lessons here : ",allLessons)
    print("student No : ",studentNo)
    for lesson in allLessons:
        isTake = random.randint(0,1)
        if isTake:
            lessonData = getSLessonData(lesson)
            print("lesson Data :",lessonData)
            notes = ['AA','BA', 'BB','CB', 'CC', 'DC','DD','FD','FF','KK']
            noteR = random.randint(0,len(notes)-1)
            lesNote = notes[noteR] 
            listData = [[lessonData[0][2],lesNote,lessonData[0][4]]]
            studentN = []
            studentN.append(studentNo)
            NewStudentLessons(studentN,listData)

def getAllSL():
    ınsertNew = """ SELECT * FROM StudentsLessons;"""
    cursor.execute(ınsertNew)
    lessonList = cursor.fetchall()
    print("List : ",lessonList)

def createRandomStudent(count):
    for x in range(0,int(count)):
        userNo = genUserNo()
        studentNos = getStudentNos()
        studentNo = "210201"+str(random.randint(0,200))
        while studentNo in studentNos:
            studentNo = "210201"+str(random.randint(0,200))
    
        name = "student"+str(userNo)
        surName = "studentsur"+str(userNo)
        note = str(round(random.uniform(0, 4), 2))
        transkriptPath = "--"
        createNewUser(name, userNo,"student")
        createRandomStudentsLessons(studentNo)
        createNewStudent(userNo, studentNo,name,surName, note,transkriptPath)
    closeDB()
    connect()

def createTeacherTable():
    create = """ 
        CREATE TABLE IF NOT EXISTS Teachers (
        UserNo INT PRIMARY KEY,
        RegNo INT,
        Name VARCHAR(50),
        SurName VARCHAR(50),
        MaxStudent INT,
        Interests VARCHAR(255))
     """
        #Interests VARCHAR(255),
        #DealRequestCount INT,
        #DealState VARCHAR(50),
    try:
        cursor.execute(create)
    except:
        print("error createing teachers table")


def createnewTeacher(userNo, regNo, name, surname, maxStudent):
    ınsertNew = """ INSERT INTO Teachers VALUES ('{}' , '{}' ,'{}', '{}','{}', '');  """.format(userNo, regNo, name, surname, maxStudent)
    cursor.execute(ınsertNew)

def createNewLesson(lessonName, lessonNo, regNo):
    rec = getBig("ActiveLessons")
    print("aLesson rec", rec)
    ınsertNew = """ INSERT INTO ActiveLessons VALUES ('{}' , '{}' ,'{}', '{}');  """.format(rec, lessonNo, lessonName, regNo)
    cursor.execute(ınsertNew)

def getInterest(userNo, role):
    if role == "student":
        ınsertNew = """ SELECT Interests FROM Students WHERE UserNo = '{}';  """.format(userNo)
        cursor.execute(ınsertNew)
        intList = cursor.fetchall()
        intList = parseData(intList)
        print("List : ",intList)
        return intList
        
    elif role == "teacher":
        ınsertNew = """ SELECT Interests FROM Teachers WHERE UserNo = '{}';  """.format(userNo)
        cursor.execute(ınsertNew)
        intList = cursor.fetchall()
        print("List : ",intList)
        intList = parseData(intList)
        print("List : ",intList)
        return intList

def setInterest(userNo, role, interest):
    interestold = getInterest(userNo, role)
    into = ""
    if interestold != None:
        x = 0
        for i in interestold:
            if x == 0 :
                into = str(i)
            else:
                into = into + " " +str(i)
            x += 1
        if interest not in into.split(" "):
            into = into + " " +interest
    print("inter : ",into)
    if role == "student":
        ınsertNew = """ UPDATE Students SET Interests = '{}' WHERE UserNo = '{}';  """.format(into, userNo)
        cursor.execute(ınsertNew)
    elif role == "teacher":
        ınsertNew = """ UPDATE Teachers SET Interests = '{}' WHERE UserNo = '{}';  """.format(into, userNo)
        cursor.execute(ınsertNew)

def getTeacherData(userNo):
    ınsertNew = """ SELECT * FROM Teachers WHERE UserNo = '{}';  """.format(userNo)
    cursor.execute(ınsertNew)
    data = cursor.fetchall()
    return data

def getTeacherDataReg(regNo):
    ınsertNew = """ SELECT * FROM Teachers WHERE RegNo = '{}';  """.format(regNo)
    cursor.execute(ınsertNew)
    data = cursor.fetchall()
    return data

def getActiveLessons():
    #rec = getBig("ActiveLessons")
    lessonList = []
    ınsertNew = """ SELECT * FROM ActiveLessons;"""
    cursor.execute(ınsertNew)
    data = cursor.fetchall()
    print(data)
    return data

def getActiveLessonData(lessonNo, regNo):
    ınsertNew = """ SELECT * FROM ActiveLessons WHERE LessonNo = '{}' and RegNo = '{}';""".format(lessonNo,regNo)
    cursor.execute(ınsertNew)
    data = cursor.fetchall()
    print(data)
    return data

def getActiveLessonTeachers(lessonNo):
    ınsertNew = """ SELECT RegNo FROM ActiveLessons WHERE LessonNo = '{}';""".format(lessonNo)
    cursor.execute(ınsertNew)
    data = cursor.fetchall()
    data = parseData(data)
    print(data)
    return data

def getTeachersActiveLesson(regNo):
    ınsertNew = """ SELECT * FROM ActiveLessons WHERE RegNo = '{}';""".format(regNo)
    cursor.execute(ınsertNew)
    data = cursor.fetchall()
    print(data)
    return data

def genLessonNo(lessonName):
    lessons = getActiveLessons()
    lessonNos = []
    lessonNames = []
    for lesson in lessons:
        if lessonName == lesson[2]:
            return lesson[1]
        lessonNos.append(lesson[1])
    lessonNo = "200200"+str(random.randint(0,200))
    while lessonNo in lessonNos:
        lessonNo = "210201"+str(random.randint(0,200))
    return lessonNo

def createReq():
    createReqTable = """ 
        CREATE TABLE IF NOT EXISTS Req (
        rec INT PRIMARY KEY,
        StudentNo INT,
        RegNo INT,
        LessonNo INT)
     """
    try:
        cursor.execute(createReqTable)
    except:
        print("error createing req table")

def newReq(studentNo, regNo, lessonNo):
    rec = getBig("Req")
    insertNew = "INSERT INTO Req VALUES ('{}', '{}', '{}', '{}');".format(rec, studentNo, regNo, lessonNo)
    cursor.execute(insertNew)

def getAllReqs():
    ınsertNew = """ SELECT * FROM Req;"""
    cursor.execute(ınsertNew)
    data = cursor.fetchall()
    print(data)
    return data


def getReqs(regNo):
    ınsertNew = """ SELECT * FROM Req WHERE RegNo = '{}';""".format(regNo)
    cursor.execute(ınsertNew)
    data = cursor.fetchall()
    print(data)
    return data


def delReq(studentNo, regNo, lessonNo):
    delData = "DELETE FROM Req WHERE RegNo = '{}' and StudentNo = '{}' and LessonNo = '{}';".format(regNo, studentNo, lessonNo)
    cursor.execute(delData)


def delLessonReq(studentNo, lessonNo):
    delData = "DELETE FROM Req WHERE StudentNo = '{}' and LessonNo = '{}';".format(studentNo, lessonNo)
    cursor.execute(delData)


def createMessages():
    createReqTable = """ 
        CREATE TABLE IF NOT EXISTS Messages (
        rec INT PRIMARY KEY,
        StudentNo INT,
        RegNo INT,
        MessageText VARCHAR(1023))
     """
    try:
        cursor.execute(createReqTable)
    except:
        print("error createing messages table")

def sendMessage(studentNo, regNo, messageText):
    rec = getBig("Messages")
    insertNew = "INSERT INTO Messages VALUES ('{}', '{}', '{}', '{}');".format(rec, studentNo, regNo, messageText)
    cursor.execute(insertNew)

def getMessages(number, role):
    if role == "teacher":
        ınsertNew = """ SELECT * FROM Messages WHERE RegNo = '{}';""".format(number)
    else:
        ınsertNew = """ SELECT * FROM Messages WHERE StudentNo = '{}';""".format(number)
    cursor.execute(ınsertNew)
    data = cursor.fetchall()
    print("message : ",data)
    return data

def getLessonName(lessonNo):
    ınsertNew = """ SELECT LessonName FROM ActiveLessons WHERE LessonNo = '{}';""".format(lessonNo)
    cursor.execute(ınsertNew)
    data = cursor.fetchall()
    print("lessonName : ",data)
    return data


def getTeachersActiveL(regNo):
    ınsertNew = """ SELECT LessonNo FROM ActiveLessons WHERE RegNo = '{}';""".format(regNo)
    cursor.execute(ınsertNew)
    data = cursor.fetchall()
    data = parseData(data)
    print(data)
    return data
# bu ogrenci için : hocanın verdiği ders için onaylanmış talebi bulunmayan
def getStudentsNoReqForTeacher(regNo):
    teachersL = getTeachersActiveL(regNo)
    students = getStudents()
    searchedStudents = []
    for student in students:
        studentData = getStudentData(student) 
        if studentData:
            studentNo = studentData[1]
            print(studentData)
            acceptedL = getAcceptedLessonNo(studentNo)
            for lesson in teachersL:
                print("heree : ",lesson, acceptedL)
                if lesson not in acceptedL:
                    print("öğrencinin alabileceği ders var")
                    searchedStudents.append([student,lesson])
    print("accepted S : ",searchedStudents)
    return searchedStudents

def createAcceptedLessons():
    createALTable = """ 
        CREATE TABLE IF NOT EXISTS AcceptedLessons (
        rec INT PRIMARY KEY,
        StudentNo INT,
        RegNo INT,
        LessonNo INT)
     """
    try:
        cursor.execute(createALTable)
    except:
        print("error createing Aciteve Lessons table")

def getTeacherMaxStudent(regNo):
    ınsertNew = """ SELECT MaxStudent FROM Teachers WHERE RegNo = '{}';  """.format(regNo)
    cursor.execute(ınsertNew)
    data = cursor.fetchall()
    return data

def getTeacherActiveStudent(regNo):
    activeLessons = getAllAcceptedLesson()
    counter = 0
    for lesson in activeLessons:
        lessonRegNo = lesson[2]
        if int(regNo) == int(lessonRegNo):
            counter += 1
    return counter

def isTeacherAbleToGet(regNo):
    left = getTeacherMaxStudent(regNo)[0][0] - getTeacherActiveStudent(regNo)
    if left > 0:
        return 1
    else:
        return 0

def acceptLesson(studentNo, regNo, lessonNo):
    #control is acceptable
    activeStudent = getTeacherActiveStudent(regNo)
    maxStudent = getTeacherMaxStudent(regNo)[0][0]
    if activeStudent < maxStudent:
        print("able to accept")
        rec = getBig("AcceptedLessons")
        insertNew = "INSERT INTO AcceptedLessons VALUES ('{}', '{}', '{}', '{}');".format(rec, studentNo, regNo, lessonNo)
        cursor.execute(insertNew)
        closeDB()
        connect()
        return True
    else:
        dialog = dialogs.textMessage(None," Student Limit Reached ! \n not able to accept The Lesson")
        response = dialog.run()
        dialog.destroy()
        return False

def getAllAcceptedLesson():
    ınsertNew = """ SELECT * FROM AcceptedLessons;"""
    cursor.execute(ınsertNew)
    data = cursor.fetchall()
    #print("Accepted Lesson : ",data)
    return data

def getAcceptedLesson(studentNo):
    ınsertNew = """ SELECT * FROM AcceptedLessons WHERE StudentNo = '{}';""".format(studentNo)
    cursor.execute(ınsertNew)
    data = cursor.fetchall()
    print("Accepted Lesson : ",data)
    return data

def getAcceptedLessonNo(studentNo):
    ınsertNew = """ SELECT LessonNo FROM AcceptedLessons WHERE StudentNo = '{}';""".format(studentNo)
    cursor.execute(ınsertNew)
    data = cursor.fetchall()
    data = parseData(data)
    print("Accepted Lesson : ",data)
    return data

def getStudentsReqs(studentNo, lessonNo):
    ınsertNew = """ SELECT * FROM Req WHERE StudentNo = '{}' and LessonNo = '{}';""".format(studentNo, lessonNo)
    cursor.execute(ınsertNew)
    data = cursor.fetchall()
    print(data)
    return data



def getReqC(studentNo, lessonNo):
    reqs = getStudentsReqs(studentNo,lessonNo)
    counter = 0
    for req in reqs:
        counter += 1
    print(counter)
    return counter

def getStudentsAcceptedLessons(studentNo):
    #rec = getBig("ActiveLessons")
    lessonList = []
    ınsertNew = """ SELECT LessonNo FROM AcceptedLessons WHERE StudentNo = '{}';""".format(studentNo)
    cursor.execute(ınsertNew)
    data = cursor.fetchall()
    print(data)
    return data

# max mesaj uzunluğu tutulacak, öğrencinin max farklı hocaya talep açabileceği sayi
def createRootTable():
    createRTable = """ 
        CREATE TABLE IF NOT EXISTS Root (
        rec INT PRIMARY KEY,
        ReqTeacherLimit INT,
        MessageLenLimit INT,
        Timeout INT)
     """
    try:
        cursor.execute(createRTable)
    except:
        print("error createing Root table")

def setRootData(reqL, mlenL,timeout):
    delData = "DELETE FROM Root;"
    cursor.execute(delData)
    ınsertNew = """ INSERT INTO Root VALUES (0 , '{}' ,'{}','{}');  """.format(reqL, mlenL,timeout)
    cursor.execute(ınsertNew)

def getRootData():
    ınsertNew = """ SELECT * FROM Root;"""
    cursor.execute(ınsertNew)
    data = cursor.fetchall()
    return data


def closeDB():
    conn.commit()
    cursor.close()
    conn.close()
