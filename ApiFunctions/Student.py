
from sql import MySQL
import Model.User as mUser
import ApiFunctions.User as apiUser

class StudentApi:
    def __init__(self,student) -> None:
        self.student = student
        
    def studentDetails(self):
        sql = MySQL()
        sql.__enter__()
        cursor = sql.conn.cursor()
        cursor.execute(f'''
                SELECT * FROM STUDENT 
                    ''')
        lst=[]
        for row in cursor.fetchall():
           lst.append(self.student.Student(aridNo=row.AridNo,name=row.Name,
                                           image=row.Image,password=row.Password))
        
        return lst
    
    def studentCourseOffered(self,studentCourseOffered):
        sql = MySQL()
        sql.__enter__()
        cursor = sql.conn.cursor()
        cursor.execute(f'''
               SELECT * FROM STUDENT WHERE AridNo NOT IN (SELECT s.AridNo 
               FROM OFFERED_COURSES oc INNER JOIN SECTION_OFFER so 
               ON oc.ID=so.CourseOfferId INNER JOIN ENROLL e  ON e.SectionOfferID=so.ID
               INNER JOIN STUDENT s ON s.AridNo=e.StudentID
               AND SessionId=(SELECT TOP 1 
               SESSION.ID FROM SESSION ORDER BY ID DESC)
               AND oc.CourseName IN {tuple(studentCourseOffered)})
                    ''')
        lst=[]
        for row in cursor.fetchall():
           lst.append(self.student.Student(aridNo=row.AridNo,name=row.Name,
                                           image=row.Image,password=row.Password))
        
        return lst
            
        
        
   
    def addStudent(self,student):
        sql = MySQL()
        sql.__enter__()
        cursor = sql.conn.cursor()
        user = mUser.User
        user.id=0
        user.userID=student.aridNo
        user.name=student.name
        user.password = student.password
        user.role="Student"
        user.image=student.image
        user_object = apiUser.UserApi(user=user)
        result = user_object.add_user(user=user)
        if result=="Added":
            cursor.execute(f'''
                    INSERT INTO STUDENT
                    VALUES
                    ('{student.aridNo}','{student.name}','{student.image}','{student.password}')
                    ''')
        return result
