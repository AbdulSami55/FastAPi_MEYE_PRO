    
from sql import MySQL

class TeachApi:
    def __init__(self,teach) -> None:
        self.teach = teach
        
    def teach_details(self,teacherid):
        sql = MySQL()
        sql.__enter__()
        cursor = sql.conn.cursor()
        cursor.execute(f'''
                SELECT * FROM TEACH WHERE TeacherID='{teacherid}'
                    ''')
        lst=[]
        for row in cursor.fetchall():
            lst.append(self.teach.Teach(id=row.ID,timeTableID=row.TimeTableID,teacherID=row.TeacherID))
            
        return {"data":lst}
    def update_teach_details(self,teach):
        sql = MySQL()
        sql.__enter__()
        cursor = sql.conn.cursor()
        cursor.execute(f'''
                   UPDATE TEACH SET TimeTableID = '{teach.timeTableID}',
                   TeacherID='{teach.teacherID}'
                   WHERE  ID = '{teach.id}' 
                   ''')
    
        return {
               "data":teach
                }
    def delete_teach_details(self,teach):
        sql = MySQL()
        sql.__enter__()
        cursor = sql.conn.cursor()
        cursor.execute(f'''
                   DELETE FROM TEACH WHERE ID = '{teach.id}'
                    ''')
    
        return {"data":"okay"}
    def add_teach(self,teach):
        sql = MySQL()
        sql.__enter__()
        cursor = sql.conn.cursor()
        cursor.execute(f'''
                            SELECT * FROM MEYE_USER WHERE ID='{teach.teacherID}'
                            ''')
        role=''
        for row in cursor.fetchall():
            role=row.ROLE
        if role=='Teacher':
            cursor.execute(f'''
                            SELECT * FROM TEACH WHERE TeacherID='{teach.teacherID}' 
                            AND TimeTableID='{teach.timeTableID}'
                            ''')
            count=0
            for row in cursor.fetchall():
                count=1
            if count==0:
                cursor.execute(f'''
                        SELECT * FROM TIMETABLE
                        WHERE ID=
                        '{teach.timeTableID}'
                        ''')
                courseCode=-1
                for row in cursor.fetchall():
                   courseCode = row.CourseID
                cursor.execute(f'''
                        SELECT * FROM COURSE
                        WHERE ID=
                        '{courseCode}'
                        ''')
                cr_hour=-1
                for row in cursor.fetchall():
                   cr_hour = row.CreditHours
                try:
                    cursor.execute(f'''
                            INSERT INTO TEACH
                            VALUES
                            ('{teach.timeTableID}','{teach.teacherID}')
                            ''')
                    cursor.execute(f'''
                            SELECT * FROM TEACH
                            WHERE TimeTableID=
                            '{teach.timeTableID}' AND TeacherID='{teach.teacherID}'
                            ''')
                    teachID=-1
                    for i in cursor.fetchall():
                        teachID=i.ID
                    cursor.execute(f'''
                            INSERT INTO RULES
                            VALUES
                            ('{teachID}','{False}','{False}','{False}')
                            ''')
                    if cr_hour==3:
                        for i in range(1,33):
                            cursor.execute(f'''
                            INSERT INTO TEACHERSLOTS
                            VALUES
                            ('{teachID}','{i}','{0}')
                            ''')
                    elif cr_hour==2:
                        for i in range(1,17):
                            cursor.execute(f'''
                            INSERT INTO TEACHERSLOTS
                            VALUES
                            ('{teachID}','{i}','{0}')
                            ''')
                    elif cr_hour==4:
                        for i in range(1,49):
                            cursor.execute(f'''
                            INSERT INTO TEACHERSLOTS
                            VALUES
                            ('{teachID}','{i}','{0}')
                            ''')
                except:
                     cursor.execute(f'''
                            DELETE FROM TEACH
                             WHERE TimeTableID=
                            '{teach.timeTableID}' AND TeacherID='{teach.teacherID}'
                            ''')
                     cursor.execute(f'''
                            DELETE FROM TEACHERSLOTS
                            WHERE TeachID=
                            '{teachID}'
                            ''')
                     return {"data":"Something Went Wrong"}
                    
                

                return {"data":"okay"}
            else:
                return {"data":"teacher already teach this class"}
        else:
            return {"data":"User is not teacher"}
