from datetime import datetime
from typing import List
import cv2
import face_recognition
import numpy as np
from sql import MySQL
import Model.Attendance as mattendace
import main 
class AttendanceApi:
    def __init__(self,attendance) -> None:
        self.attendance = attendance
        
    def attendance_details(self,dvrID):
        sql = MySQL()
        sql.__enter__()
        cursor = sql.conn.cursor()
        cursor.execute(f'''
                SELECT * FROM ATTENDANCE 
                    ''')
        lst=[]
        for row in cursor.fetchall():
           lst.append(self.cam.Attendance(id=row.ID,dvrID=row.DvrID,venueID=row.VenueID,portNumber=row.PortNumber))
        
        return {"data":lst}
        
    def update_attendance_details(self,attendance):
        sql = MySQL()
        sql.__enter__()
        cursor = sql.conn.cursor()
        cursor.execute(f'''
                   UPDATE ATTENDANCE SET StudyID = '{attendance.studentid}',
                   DATE='{attendance.date}' ,  STATUS='{attendance.status}'
                   WHERE ID ='{attendance.id}'
                   ''')
    
        return {"data":attendance}
    def delete_attendance_details(self,attendance):
        sql = MySQL()
        sql.__enter__()
        cursor = sql.conn.cursor()
        cursor.execute(f'''
                   DELETE FROM ATTENDANCE WHERE ID = '{attendance.id}'
                    ''')
    
        return {"data":"okay"}
    async def add_attendance(self,attendance:List[mattendace.Attendance]):
        sql = MySQL()
        sql.__enter__()
        cursor = sql.conn.cursor()
        for data in attendance:
            cursor.execute(f'''
                    INSERT INTO ATTENDANCE
                    VALUES
                    ('{data.enrollId}','{data.status}','{data.date}')
                    ''')
            if data.status==False:
                await  main.send_notification("","Absent")
        return "Attendance Marked"
    
    async def mark_attendance(self,img):
        sql = MySQL()
        sql.__enter__()
        cursor = sql.conn.cursor()
        # test_image =  face_recognition.load_image_file(img)
        # face_encodings = face_recognition.face_encodings(test_image)
        test_image = cv2.imread(img)
        test_image = cv2.resize(test_image, (0, 0), fx=0.5, fy=0.5)
        face_locations = face_recognition.face_locations(test_image)
        face_encodings = face_recognition.face_encodings(test_image,face_locations)
        lst=[]
        cursor.execute(f'''                 
                       SELECT  s.*,e.ID,t.StartTime FROM TIMETABLE t Inner Join OFFERED_COURSES oc On
                       oc.CourseCode=t.CourseCode Inner Join SECTION_OFFER so On so.CourseOfferId=oc.ID Inner Join
                       ENROLL e on e.SectionOfferID=so.ID Inner Join STUDENT s on
                       s.AridNo = e.StudentID WHERE t.TeacherName Like 'Dr. Hassan%' AND
                       t.Day='Friday' AND t.StartTime='11:30:00.000000'
                       ''')
        
        for row in cursor.fetchall():
            lst.append(self.mark_and_save_attendance(face_encodings,row.Image,row.ID,row.Name))
            print(f'''
                  {row.Name} Attendance Marked
                  ''')
        return lst
    


    def mark_attendance_by_video(self,img,lstAttendance,index):
        sql = MySQL()
        sql.__enter__()
        cursor = sql.conn.cursor()
        # test_image =  face_recognition.load_image_file(img)
        # face_encodings = face_recognition.face_encodings(test_image)
        # test_image = cv2.imread(img)
        test_image=img
        test_image = cv2.resize(test_image, (0, 0), fx=0.5, fy=0.5)
        face_locations = face_recognition.face_locations(test_image)
        face_encodings = face_recognition.face_encodings(test_image,face_locations)
        lst=[]
        cursor.execute(f'''                 
                       SELECT  s.*,e.ID,t.StartTime FROM TIMETABLE t Inner Join OFFERED_COURSES oc On
                       oc.CourseCode=t.CourseCode Inner Join SECTION_OFFER so On so.CourseOfferId=oc.ID Inner Join
                       ENROLL e on e.SectionOfferID=so.ID Inner Join STUDENT s on
                       s.AridNo = e.StudentID WHERE t.TeacherName Like 'Dr. Hassan%' AND
                       t.Day='Friday' AND t.StartTime='11:30:00.000000'
                       ''')
        
        for row in cursor.fetchall():
            lst.append(self.mark_and_save_attendance(face_encodings,row.Image,row.ID,row.Name))
            print(f'''
                  {row.Name} Attendance Marked
                  ''')
        lstAttendance[index]=lst
    
    def mark_and_save_attendance(self,face_encodings,Image,ID,Name):
        try:
            image = cv2.imread(f'UserImages/Student/{Image}')
            image = cv2.resize(image, (0, 0), fx=0.5, fy=0.5)
            image_encodings = face_recognition.face_encodings(image)[0]
        except:
            image =  face_recognition.load_image_file(f'UserImages/Student/{Image}')
            image_encodings = face_recognition.face_encodings(image)[0]
        # img = cv2.imread(f'UserImages/Student/{Image}')
        # height, width = img.shape[:2]
        # new_width = 640
        # new_height = int(new_width * height / width)
        # img = cv2.resize(img, (new_width, new_height))
        # image_encodings = face_recognition.face_encodings(img)
        count=0
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(np.expand_dims(image_encodings,axis=0),face_encoding,tolerance=0.55)
            if True in matches:
                print(np.linalg.norm(np.expand_dims(image_encodings,axis=0) - face_encoding, axis=1))
                count+=1
                return mattendace.Attendance(id=0,enrollId=ID,date=str(datetime.now().date()),status=True,name=Name)
                
        if count==0:
            return mattendace.Attendance(id=0,enrollId=ID,date=str(datetime.now().date()),status=False,name=Name)
        
                
