


from datetime import datetime
import face_recognition
import cv2
import numpy as np
from sql import MySQL
import Model.Attendance as mattendace
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
    def add_attendance(self,attendance):
        sql = MySQL()
        sql.__enter__()
        cursor = sql.conn.cursor()
        cursor.execute(f'''
                INSERT INTO ATTENDANCE
                VALUES
                ('{attendance.studentid}','{attendance.teacherSlotID}','{attendance.date}','{attendance.status}')
                ''')
        return {"data":"okay"}
    
    def mark_attendance(self,teacherslot,img):
        sql = MySQL()
        sql.__enter__()
        cursor = sql.conn.cursor()
        temp_image_path = f'UserImages/Student'

        test_image =  face_recognition.load_image_file(temp_image_path)
        face_locations = face_recognition.face_locations(test_image)
        face_encodings = face_recognition.face_encodings(test_image,face_locations)
        # image_encodings
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(np.expand_dims(face_encoding,axis=0),face_encoding)
            if True in matches:
                self.teachertimeinframes+=1
            else:
                self.teachertimeoutframes+=1
            count=0
        cursor.execute(f'''
                       SELECT * FROM  STUDY WHERE TeachID='{teacherslot.teachID}'
                       ''')
        for row in cursor.fetchall():
           
            self.add_attendance( mattendace.Attendance(id=0,studentid=row.ID,teacherSlotID=teacherslot.id,date=datetime.now(),status=False))
