
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
            lst.append(self.course.Course(name=row.CourseName,
                                          courseCode=row.CourseCode))

        
        return {"data":lst}
    
    def update_course_details(self,course):
        sql = MySQL()
        sql.__enter__()
        cursor = sql.conn.cursor()
        cursor.execute(f'''
                   UPDATE COURSE SET CourseCode = '{course.courseCode}',
                   CourseName='{course.courseName}'
                   WHERE CourseCode = '{course.courseCode}'
                   ''')
    
        return {"data":course}
    def delete_course_details(self,course):
        sql = MySQL()
        sql.__enter__()
        cursor = sql.conn.cursor()
        cursor.execute(f'''
                   DELETE FROM COURSE WHERE Course_Code = '{course.courseCode}'
                    ''')
    

        return {"data":"okay"}
    def add_course(self,course):
        sql = MySQL()
        sql.__enter__()
        cursor = sql.conn.cursor()
        cursor.execute(f'''
                INSERT INTO COURSE
                VALUES
                ('{course.courseCode}','{course.courseName}')
                ''')
        return {"data":"okay"}
