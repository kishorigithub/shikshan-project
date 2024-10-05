from flask import Flask,request
import pymysql
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import json
from datetime import datetime 
import random
import threading
lock = threading.Lock()

app = Flask(__name__)

UPLOAD_FOLDER = 'static/files/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

CORS(app)
app.secret_key = 'any random string'

def dbConnection():
    try:
        connection = pymysql.connect(host="localhost", user="root", password="root", database="shikshana",port=3307)
        return connection
    except:
        print("Something went wrong in database Connection")

def dbClose():
    try:
        dbConnection().close()
    except:
        print("Something went wrong in Close DB Connection")

con = dbConnection()
cursor = con.cursor()

"----------------------------------------------------------------------------------------------------"

@app.route('/teacherRegister', methods=['GET', 'POST'])
def teacherRegister():
    if request.method == 'POST':
        data = request.get_json()
        
        username = data.get('username')
        print("username from react",username)
        email = data.get('email')
        mobile = data.get('mobile')
        password = data.get('password')
        standard = data.get('standard')
        typeofuser = "teacher"
        status = data.get('status')
        if typeofuser == "User":
            userid = data.get('userid')   
        else:
            userid = "Teacher_"+str(random.randint(999,9999))
            
        cursor.execute('SELECT * FROM teacher WHERE username = %s AND standard = %s AND typeofuser = %s OR id = %s', (username,standard,typeofuser,userid))
        count = cursor.rowcount
        if count > 0:        
            return "fail"
        else:
            sql1 = "INSERT INTO teacher(id, username, email, number, password, standard,reportcard,typeofuser,status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
            val1 = (userid, username, email, mobile, password, standard,"None",typeofuser,status)
            cursor.execute(sql1,val1)
            con.commit()
            return "success"
    return "fail"


@app.route('/studentRegister', methods=['GET', 'POST'])
def studentRegister():
    if request.method == 'POST':
        data = request.get_json()
        
        username = data.get('username')
        print("username from react",username)
        email = data.get('email')
        mobile = data.get('mobile')
        password = data.get('password')
        standard = data.get('standard')
        typeofuser = "student"
        status = data.get('status')
        if typeofuser == "student":
            userid = data.get('userid')   
        else:
            userid = "Teacher_"+str(random.randint(999,9999))
            
        cursor.execute('SELECT * FROM student WHERE username = %s AND standard = %s AND typeofuser = %s OR userid = %s', (username,standard,typeofuser,userid))
        count = cursor.rowcount
        if count > 0:        
            return "fail"
        else:
            sql1 = "INSERT INTO student(userid, username, email, number, password, standard,reportcard,typeofuser,status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
            val1 = (userid, username, email, mobile, password, standard,"None",typeofuser,status)
            cursor.execute(sql1,val1)
            con.commit()
            return "success"
    return "fail"
    

@app.route('/teacherlogin', methods=['GET', 'POST'])
def teacherlogin():
    if request.method == 'POST':
        data = request.get_json()
        
        username = data.get('username')
        password = data.get('password')
        standard = data.get('standard')
        typeofuser = "teacher"
        cursor.execute('SELECT * FROM teacher WHERE username = %s AND password = %s AND standard = %s AND typeofuser = %s AND status = %s', (username, password, standard, typeofuser, "Verified"))

        count = cursor.rowcount
        if count > 0:        
            return "success"
        else:
            return "fail"
        
@app.route('/getAllTeacher', methods=['GET', 'POST'])
def getAllTeacher():
    try:
        lock.acquire()
        cursor.execute('SELECT * from teacher WHERE typeofuser = %s',("teacher"))
        row = cursor.fetchall() 
        lock.release()
        # print(row)
        
        jsonObj = json.dumps(row)         
        return jsonObj
    except Exception as ex:
        print(ex)                 
        return "" 
    
@app.route('/verifyUser', methods=['GET', 'POST'])
def verifyUser():
    if request.method == 'POST':
        data = request.get_json()
        
        userid = data.get('userid')
        typeofuser = data.get('typeofuser')
        
        sql1 = "UPDATE teacher SET status = %s WHERE id = %s AND typeofuser = %s;"
        val1 = ("Verified",userid,typeofuser)
        cursor.execute(sql1,val1)
        con.commit()
        
        return "success"
    
@app.route('/uploadTimeTable', methods=['GET', 'POST'])
def uploadTimeTable():
    if request.method == 'POST':
        print("POST")
        f1 = request.files["File"]
        title = request.form["title"]
        standard = request.form["standard"]
        
        filename_secure1 = secure_filename(f1.filename)
        
        cursor.execute('SELECT * FROM timetabledata WHERE titleoftt = %s AND standard = %s', (title,standard))
        count = cursor.rowcount
        if count == 1:        
            return "exist"
        else:
            f1.save(os.path.join(app.config['UPLOAD_FOLDER'],"timetable",filename_secure1)) 
            
            current_time = datetime.now()  
            time_stamp = current_time.timestamp() 
            date_time = datetime.fromtimestamp(time_stamp)
            str_date_time = date_time.strftime("%d-%m-%Y, %H:%M:%S")
            
            sql1 = "INSERT INTO timetabledata(filename,titleoftt,standard,timestamp) VALUES (%s, %s, %s, %s);"
            val1 = ("static/files/timetable/"+filename_secure1,title,standard,str_date_time)
            cursor.execute(sql1,val1)
            con.commit()
            return "success"
        
    return "fail"

@app.route('/verifystudent', methods=['GET', 'POST'])
def verifystudent():
    if request.method == 'POST':
        data = request.get_json()
        
        userid = data.get('userid')
        typeofuser = data.get('typeofuser')
        
        sql1 = "UPDATE student SET status = %s WHERE userid = %s AND typeofuser = %s;"
        val1 = ("Verified",userid,typeofuser)
        cursor.execute(sql1,val1)
        con.commit()
        
        return "success"
    
@app.route('/getAllstudent', methods=['GET', 'POST'])
def getAllstudent():
    try:
        lock.acquire()
        cursor.execute('SELECT * from student WHERE typeofuser = %s',("student"))
        row = cursor.fetchall() 
        lock.release()
        # print(row)
        
        jsonObj = json.dumps(row)         
        return jsonObj
    except Exception as ex:
        print(ex)                 
        return "" 


@app.route('/studentlogin', methods=['GET', 'POST'])
def studentlogin():
    if request.method == 'POST':
        data = request.get_json()
        
        username = data.get('username')
        password = data.get('password')
        standard = data.get('standard')
        typeofuser = "student"
        cursor.execute('SELECT * FROM student WHERE username = %s AND password = %s AND standard = %s AND typeofuser = %s AND status = %s', (username, password, standard, typeofuser, "Verified"))

        count = cursor.rowcount
        if count > 0:        
            return "success"
        else:
            return "fail"

    

# @app.route('/uploadTimeTable', methods=['GET', 'POST'])
# def uploadTimeTable():
#     if request.method == 'POST':
#         print("POST")
#         f1 = request.files["File"]
#         title = request.form["title"]
#         standard = request.form["standard"]
        
#         filename_secure1 = secure_filename(f1.filename)
        
#         cursor.execute('SELECT * FROM timetabledata WHERE titleoftt = %s AND standard = %s', (title,standard))
#         count = cursor.rowcount
#         if count == 1:        
#             return "exist"
#         else:
#             f1.save(os.path.join(app.config['UPLOAD_FOLDER'],"timetable",filename_secure1)) 
            
#             current_time = datetime.now()  
#             time_stamp = current_time.timestamp() 
#             date_time = datetime.fromtimestamp(time_stamp)
#             str_date_time = date_time.strftime("%d-%m-%Y, %H:%M:%S")
            
#             sql1 = "INSERT INTO timetabledata(filename,titleoftt,standard,timestamp) VALUES (%s, %s, %s, %s);"
#             val1 = ("static/files/timetable/"+filename_secure1,title,standard,str_date_time)
#             cursor.execute(sql1,val1)
#             con.commit()
#             return "success"
        
#     return "fail"

# @app.route('/uploadSyllabus', methods=['GET', 'POST'])
# def uploadSyllabus():
#     if request.method == 'POST':
#         print("POST")
#         f1 = request.files["File"]
#         title = request.form["title"]
#         standard = request.form["standard"]
        
#         filename_secure1 = secure_filename(f1.filename)
        
#         cursor.execute('SELECT * FROM syllabusdata WHERE titleofs = %s AND standard = %s', (title,standard))
#         count = cursor.rowcount
#         if count == 1:        
#             return "exist"
#         else:
#             f1.save(os.path.join(app.config['UPLOAD_FOLDER'],"syllabus",filename_secure1)) 
            
#             current_time = datetime.now()  
#             time_stamp = current_time.timestamp() 
#             date_time = datetime.fromtimestamp(time_stamp)
#             str_date_time = date_time.strftime("%d-%m-%Y, %H:%M:%S")
            
#             sql1 = "INSERT INTO syllabusdata(filename,titleofs,standard,timestamp) VALUES (%s, %s, %s, %s);"
#             val1 = ("static/files/syllabus/"+filename_secure1,title,standard,str_date_time)
#             cursor.execute(sql1,val1)
#             con.commit()
#             return "success"
        
#     return "fail"

# @app.route('/uploadAssignment', methods=['GET', 'POST'])
# def uploadAssignment():
#     if request.method == 'POST':
#         print("POST")
#         f1 = request.files["File"]
#         title = request.form["title"]
#         standard = request.form["standard"]
        
#         filename_secure1 = secure_filename(f1.filename)
        
#         cursor.execute('SELECT * FROM assignmentdata WHERE titleofam = %s AND standard = %s', (title,standard))
#         count = cursor.rowcount
#         if count == 1:        
#             return "exist"
#         else:
#             f1.save(os.path.join(app.config['UPLOAD_FOLDER'],"assignment",filename_secure1)) 
            
#             current_time = datetime.now()  
#             time_stamp = current_time.timestamp() 
#             date_time = datetime.fromtimestamp(time_stamp)
#             str_date_time = date_time.strftime("%d-%m-%Y, %H:%M:%S")
            
#             sql1 = "INSERT INTO assignmentdata(filename,titleofam,standard,timestamp) VALUES (%s, %s, %s, %s);"
#             val1 = ("static/files/assignment/"+filename_secure1,title,standard,str_date_time)
#             cursor.execute(sql1,val1)
#             con.commit()
#             return "success"
        
#     return "fail"

# @app.route('/uploadAssignmentGform', methods=['GET', 'POST'])
# def uploadAssignmentGform():
#     if request.method == 'POST':
        
#         data = request.get_json()
        
#         link = data.get('link')
#         title = data.get('title')
#         standard = data.get('standard')
        
#         cursor.execute('SELECT * FROM assignmentdata WHERE titleofam = %s AND standard = %s', (title,standard))
#         count = cursor.rowcount
#         if count == 1:        
#             return "exist"
#         else:
            
#             current_time = datetime.now()  
#             time_stamp = current_time.timestamp() 
#             date_time = datetime.fromtimestamp(time_stamp)
#             str_date_time = date_time.strftime("%d-%m-%Y, %H:%M:%S")
            
#             sql1 = "INSERT INTO assignmentdata(filename,titleofam,standard,timestamp) VALUES (%s, %s, %s, %s);"
#             val1 = (link,title,standard,str_date_time)
#             cursor.execute(sql1,val1)
#             con.commit()
#             return "success"
        
#     return "fail"


# @app.route('/getSyllabus/<stdard>', methods=['GET', 'POST'])
# def getSyllabus(stdard):
#     try:
#         lock.acquire()
#         cursor.execute('SELECT * FROM syllabusdata WHERE standard = %s', (stdard))
#         row = cursor.fetchall() 
#         lock.release()
#         # print(row)
        
#         jsonObj = json.dumps(row)         
#         return jsonObj
#     except Exception as ex:
#         print(ex)                 
#         return ""
    
# @app.route('/getTimetable/<stdard>', methods=['GET', 'POST'])
# def getTimetable(stdard):
#     try:
#         lock.acquire()
#         cursor.execute('SELECT * FROM timetabledata WHERE standard = %s', (stdard))
#         row = cursor.fetchall() 
#         lock.release()
#         # print(row)
        
#         jsonObj = json.dumps(row)         
#         return jsonObj
#     except Exception as ex:
#         print(ex)                 
#         return ""
    
# @app.route('/getAssignment/<username>/<stdard>', methods=['GET', 'POST'])
# def getAssignment(username,stdard):
#     try:
#         lock.acquire()
#         # cursor.execute('SELECT * FROM assignmentdata WHERE standard = %s', (stdard))
#         cursor.execute('SELECT t1.id,t1.filename,t1.titleofam,t1.standard,t1.timestamp,t2.username,t2.assignmentpath,t2.marksobt FROM assignmentdata t1 LEFT JOIN submitedassignment t2 ON t1.titleofam = t2.title and t1.standard = t2.standard and t2.username = %s WHERE t1.standard = %s', (username,stdard))
#         row = cursor.fetchall() 
#         lock.release()
#         # print(row)
        
#         jsonObj = json.dumps(row)         
#         return jsonObj
#     except Exception as ex:
#         print(ex)                 
#         return ""
    
# @app.route('/submitAssignment', methods=['GET', 'POST'])
# def submitAssignment():
#     if request.method == 'POST':
#         print("POST")
#         f1 = request.files["File"]
#         title = request.form["title"]
#         username = request.form["username"]
#         standard = request.form["standard"]
        
#         filename_secure1 = secure_filename(f1.filename)
        
#         cursor.execute('SELECT * FROM submitedassignment WHERE username = %s AND standard = %s AND title = %s', (username,standard,title))
#         count = cursor.rowcount
#         if count == 1:        
#             return "exist"
#         else:
#             f1.save(os.path.join(app.config['UPLOAD_FOLDER'],"submittedAssignment",filename_secure1)) 
            
#             sql1 = "INSERT INTO submitedassignment(username,standard,title,assignmentpath) VALUES (%s, %s, %s, %s);"
#             val1 = (username,standard,title,"static/files/submittedAssignment/"+filename_secure1)
#             cursor.execute(sql1,val1)
#             con.commit()
#             return "success"
        
#     return "fail"

# @app.route('/submitAssignmentGoogleForm', methods=['GET', 'POST'])
# def submitAssignmentGoogleForm():
#     if request.method == 'POST':
#         data = request.get_json()
        
#         title = data.get('title')
#         username = data.get('username')
#         standard = data.get('standard') 
        
#         cursor.execute('SELECT * FROM submitedassignment WHERE username = %s AND standard = %s AND title = %s', (username,standard,title))
#         count = cursor.rowcount
#         if count == 1:        
#             return "exist"
#         else:            
#             sql1 = "INSERT INTO submitedassignment(username,standard,title,assignmentpath) VALUES (%s, %s, %s, %s);"
#             val1 = (username,standard,title,"Marked")
#             cursor.execute(sql1,val1)
#             con.commit()
#             return "success"
        
#     return "fail"

# @app.route('/getSubmitedAssignment/<std>', methods=['GET', 'POST'])
# def getSubmitedAssignment(std):
#     try:
#         lock.acquire()
#         # cursor.execute('SELECT * FROM assignmentdata WHERE standard = %s', (stdard))
#         cursor.execute('SELECT * from submitedassignment WHERE standard = %s',(std))
#         row = cursor.fetchall() 
#         lock.release()
#         # print(row)
        
#         jsonObj = json.dumps(row)         
#         return jsonObj
#     except Exception as ex:
#         print(ex)                 
#         return ""
    
# @app.route('/updateMarks', methods=['GET', 'POST'])
# def updateMarks():
#     if request.method == 'POST':
#         data = request.get_json()
        
#         idof = data.get('id')
#         username = data.get('username')
#         std = data.get('std')
#         title = data.get('title')
#         marks = data.get('marks')
        
#         sql1 = "UPDATE submitedassignment SET marksobt = %s WHERE id = %s AND username = %s AND standard = %s AND title = %s;"
#         val1 = (marks,idof,username,std,title)
#         cursor.execute(sql1,val1)
#         con.commit()
#         return "success"
    
#     return "fail"

# @app.route('/uploadElearning', methods=['GET', 'POST'])
# def uploadElearning():
#     if request.method == 'POST':
#         print("POST")
#         f1 = request.files["File"]
#         topic = request.form["topic"]
#         title = request.form["title"]
#         standard = request.form["standard"]
        
#         filename_secure1 = secure_filename(f1.filename)
        
#         cursor.execute('SELECT * FROM elearningdata WHERE titleofam = %s AND standard = %s', (title,standard))
#         count = cursor.rowcount
#         if count == 1:        
#             return "exist"
#         else:
#             f1.save(os.path.join(app.config['UPLOAD_FOLDER'],"elearning",filename_secure1)) 
            
#             current_time = datetime.now()  
#             time_stamp = current_time.timestamp() 
#             date_time = datetime.fromtimestamp(time_stamp)
#             str_date_time = date_time.strftime("%d-%m-%Y, %H:%M:%S")
            
#             sql1 = "INSERT INTO elearningdata(link,filename,titleofam,standard,timestamp) VALUES (%s, %s, %s, %s, %s);"
#             val1 = (topic,"static/files/elearning/"+filename_secure1,title,standard,str_date_time)
#             cursor.execute(sql1,val1)
#             con.commit()
#             return "success"
        
#     return "fail"

# @app.route('/getElearning/<stdard>', methods=['GET', 'POST'])
# def getElearning(stdard):
#     try:
#         lock.acquire()
#         cursor.execute('SELECT * FROM elearningdata WHERE standard = %s', (stdard))
#         row = cursor.fetchall() 
#         lock.release()
#         # print(row)
        
#         jsonObj = json.dumps(row)         
#         return jsonObj
#     except Exception as ex:
#         print(ex)                 
#         return ""

# @app.route('/chatBot', methods=['GET', 'POST'])
# def chatBot():
#     if request.method == 'POST':
#         data = request.get_json()
        
#         query = data.get('texttosend')
#         username = data.get('username')
#         standard = data.get('standard')
        
#         current_time = datetime.now()  
#         time_stamp = current_time.timestamp() 
#         date_time = datetime.fromtimestamp(time_stamp)
#         str_date_time = date_time.strftime("%H:%M")
        
#         sql1 = "INSERT INTO chatdata(chat,username,std,time) VALUES (%s, %s, %s, %s);"
#         val1 = (query,username,standard,str_date_time)
#         cursor.execute(sql1,val1)
#         con.commit()
#         return "success"
    
#     return "fail"

# @app.route('/getAllChats/<std>', methods=['GET', 'POST'])
# def getAllChats(std):
#     try:
#         lock.acquire()
#         # cursor.execute('SELECT * FROM assignmentdata WHERE standard = %s', (stdard))
#         cursor.execute('SELECT * from chatdata WHERE std = %s',(std))
#         row = cursor.fetchall() 
#         lock.release()
#         # print(row)
        
#         jsonObj = json.dumps(row)         
#         return jsonObj
#     except Exception as ex:
#         print(ex)                 
#         return ""
 
 
    
# @app.route('/getAllStud/<std>', methods=['GET', 'POST'])
# def getAllStud(std):
#     try:
#         lock.acquire()
#         cursor.execute('SELECT * from users WHERE standard = %s AND typeofuser = %s',(std,"User"))
#         row = cursor.fetchall() 
#         lock.release()
#         # print(row)
        
#         jsonObj = json.dumps(row)         
#         return jsonObj
#     except Exception as ex:
#         print(ex)                 
#         return "" 
    
# @app.route('/markAttendance', methods=['GET', 'POST'])
# def generateReport():
#     if request.method == 'POST':
#         data = request.get_json()
        
#         formlist = data.get('formlist')
#         attendance = data.get('attendance')  
#         attdate = data.get('attdate')
        
#         if len(formlist) == len(attendance):            
#             for i in range(len(formlist)):   
#                 cursor.execute('SELECT * FROM attendance WHERE studid = %s AND date = %s', (str(formlist[i][0]),attdate))
#                 count = cursor.rowcount
#                 if count > 0:            
#                     sql1 = "UPDATE attendance SET attendance = %s WHERE studid = %s AND date = %s;"
#                     val1 = (attendance[i],str(formlist[i][0]),attdate)
#                     cursor.execute(sql1,val1)
#                     con.commit()    
#                 else:            
#                     sql1 = "INSERT INTO attendance(studid,email,mobile,std,attendance,date) VALUES (%s, %s, %s, %s, %s, %s);"
#                     val1 = (str(formlist[i][0]),str(formlist[i][2]),str(formlist[i][3]),str(formlist[i][5]),attendance[i],attdate)
#                     cursor.execute(sql1,val1)
#                     con.commit()
#             return "success"  
#         else:  
#             return "fail"   
#     return "fail"

# @app.route('/getAllAttendance/<date>/<std>', methods=['GET', 'POST'])
# def getAllAttendance(date,std):
#     try:
#         lock.acquire()
#         # cursor.execute('SELECT * FROM assignmentdata WHERE standard = %s', (stdard))
#         cursor.execute('SELECT * from attendance WHERE date = %s AND std = %s',(date,std))
#         row = cursor.fetchall() 
#         lock.release()
#         # print(row)
        
#         jsonObj = json.dumps(row)         
#         return jsonObj
#     except Exception as ex:
#         print(ex)                 
#         return "" 

# @app.route('/uploadGradeCard', methods=['GET', 'POST'])
# def uploadGradeCard():
#     if request.method == 'POST':
#         f1 = request.files["File"]   
#         userid = request.form["userid"]  
#         usermail = request.form["usermail"] 
#         userstd = request.form["userstd"] 
#         imagepath = "static/files/reportcards/"+str(userid)+"-"+str(usermail)+"-"+str(userstd)+".jpg"           
#         f1.save(imagepath) 
        
#         lock.acquire()
#         sql1 = "UPDATE users SET reportcard = %s WHERE id = %s;"
#         val1 = (imagepath,str(userid))
#         cursor.execute(sql1,val1)
#         con.commit()          
#         lock.release()
        
#         return "success"
        
#     return "fail"

# @app.route('/getReoprtCard/<username>/<stdard>', methods=['GET', 'POST'])
# def getReoprtCard(username,stdard):
#     try:
#         lock.acquire()
#         cursor.execute('SELECT reportcard FROM users WHERE username = %s AND standard = %s', (username,stdard))
#         row = cursor.fetchone()
#         lock.release()
        
#         return str(row[0])
#     except Exception as ex:
#         print(ex)                 
#         return "None"
    

    
if __name__ == "__main__":
    app.run("0.0.0.0")
    
    
