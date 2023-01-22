
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
            lst.append(self.course.Course(name=row.NAME,id=row.ID,
                                          cid=row.CID,cr_hr=row.CR_HOURS))

        
        return {"data":lst}
    
    def update_course_details(self,course):
        sql = MySQL()
        sql.__enter__()
        cursor = sql.conn.cursor()
        cursor.execute(f'''
                   UPDATE COURSE SET CID = '{course.cid}',
                   CR_HOURS='{course.cr_hr}' ,  NAME='{course.name}'
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
                ('{course.cid}','{course.cr_hr}','{course.name}')
                ''')
        return {"data":"okay"}
