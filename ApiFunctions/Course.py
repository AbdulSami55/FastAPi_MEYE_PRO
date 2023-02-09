
from sql import MySQL


class CourseApi:
    def __init__(self,course) -> None:
        self.course = course
        
    def course_details(self):
        sql = MySQL()
        sql.__enter__()
        cursor = sql.conn.cursor()
        cursor.execute(f'''
                SELECT * FROM COURSE
                    ''')
        lst=[]
        for row in cursor.fetchall():
            lst.append(self.course.Course(name=row.Name,id=row.ID,
                                          courseID=row.CourseID,creditHours=row.CreditHours))

        
        return {"data":lst}
    
    def update_course_details(self,course):
        sql = MySQL()
        sql.__enter__()
        cursor = sql.conn.cursor()
        cursor.execute(f'''
                   UPDATE COURSE SET CourseID = '{course.courseID}',
                   CreditHours='{course.creditHours}' ,  Name='{course.name}'
                   WHERE  ID='{course.id}'
                   ''')
    
        return {"data":course}
    def delete_course_details(self,course):
        sql = MySQL()
        sql.__enter__()
        cursor = sql.conn.cursor()
        cursor.execute(f'''
                   DELETE FROM COURSE WHERE ID = '{course.id}'
                    ''')
    

        return {"data":"okay"}
    def add_course(self,course):
        sql = MySQL()
        sql.__enter__()
        cursor = sql.conn.cursor()
        cursor.execute(f'''
                INSERT INTO COURSE
                VALUES
                ('{course.courseID}','{course.creditHours}','{course.name}')
                ''')
        return {"data":"okay"}
