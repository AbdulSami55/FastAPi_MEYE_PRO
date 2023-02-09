
from sql import MySQL


class EnrollApi:
    def __init__(self,enroll) -> None:
        self.enroll = enroll
        
    def enroll_details(self):
        sql = MySQL()
        sql.__enter__()
        cursor = sql.conn.cursor()
        cursor.execute(f'''
                SELECT * FROM ENROLL
                    ''')
        lst=[]
        for row in cursor.fetchall():
            lst.append(self.enroll.Enroll(courseID=row.CourseID,studentID=row.StudentID,id=row.ID))

    
        return {"data":lst
               }
    def update_enroll_details(self,enroll):
        sql = MySQL()
        sql.__enter__()
        cursor = sql.conn.cursor()
        cursor.execute(f'''
                   UPDATE ENROLL SET 
                   CourseID='{enroll.courseID}' ,  StudentID='{enroll.studentID}'
                   WHERE  ID='{enroll.id}'
                   ''')
        return {"data":enroll}
    def delete_enroll_details(self,enroll):
        sql = MySQL()
        sql.__enter__()
        cursor = sql.conn.cursor()
        cursor.execute(f'''
                   DELETE FROM ENROLL WHERE ID = '{enroll.id}'
                    ''')
    
        return {"data":"okay"}
    def add_enroll(self,enroll):
        sql = MySQL()
        sql.__enter__()
        cursor = sql.conn.cursor()
        cursor.execute(f'''
                INSERT INTO ENROLL
                VALUES
                ('{enroll.courseID}','{enroll.studentID}')
                ''')
        return {"data":"okay"}
