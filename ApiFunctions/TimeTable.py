import datetime
import pyodbc
from sql import MySQL

class TimeTableApi:
    def __init__(self,timetable) -> None:
        self.timetable = timetable
        
    def timetable_details(self):
        sql = MySQL()
        sql.__enter__()
        cursor = sql.conn.cursor()
        cursor.execute(f'''
                SELECT TIMETABLE.*,s.Name From TIMETABLE  
                INNER JOIN SESSION s on 
                TIMETABLE.SessionId = s.ID
                    ''')
        lstTimeTable = []
        for row in cursor.fetchall():
            st = row.StartTime.split(':')
            et = row.EndTime.split(':')
            st = f'{st[0]}:{st[1]}'
            et = f'{et[0]}:{et[1]}'
            lstTimeTable.append(self.timetable.TimeTable(id=row.ID,discipline=row.Discipline
                                                ,starttime=st,
                                                endtime=et,
                                                day=row.Day,courseCode=row.CourseCode,
                                                venue=row.Venue,
                                                teacherName=row.TeacherName,
                                                courseName=row.CourseName,
                                                sessionName=row.Name,
                                                sessionId=row.SessionId))
            
        return {"data":lstTimeTable}
    def update_timetable_details(self,timetable):
        sql = MySQL()
        sql.__enter__()
        cursor = sql.conn.cursor()
        cursor.execute(f'''
                   UPDATE TIMETABLE SET
                   Discipline='{timetable.discipline}' , StartTime='{timetable.starttime}',
                   EndTime='{timetable.endtime}',Day='{timetable.day}',CourseCode='{timetable.courseCode}',Venue='{timetable.venue}'
                   WHERE ID ='{timetable.id}' 
                   ''')
    
        return {"data":timetable}
    def delete_timetable_details(self,timetable):
        sql = MySQL()
        sql.__enter__()
        cursor = sql.conn.cursor()
        cursor.execute(f'''
                   DELETE FROM TIMETABLE WHERE ID = '{timetable.id}'
                    ''')
    
        return {"data":"okay"}
    def add_timetable(self,timetable):
        sql = MySQL()
        sql.__enter__()
        cursor = sql.conn.cursor()
        stime_object = datetime.datetime.strptime(str(timetable.starttime).replace(" ", ""), '%H:%M').time()
        etime_object = datetime.datetime.strptime(str(timetable.endtime).replace(" ", ""), '%H:%M').time()
        day = timetable.day
        session_id=-1
        cursor.execute("SELECT TOP 1 * FROM SESSION ORDER BY ID DESC")
        for i in cursor.fetchall():
            session_id=i.ID
        cursor.execute(f'''
                    SELECT * FROM TIMETABLE WHERE
                StartTime='{stime_object}' AND EndTime =
                '{etime_object}'
               AND Day='{day}' AND Venue='{timetable.venue}'
                    ''')
        count =0
        for row in cursor.fetchall():
            count=1
            
        if count==0:
            try:
                cursor.execute(f'''
                        INSERT INTO TIMETABLE
                        VALUES
                        (
                            '{timetable.courseCode}','{timetable.courseName}',
                            '{timetable.teacherName}',
                            '{timetable.discipline}' ,'{timetable.venue}',
                            '{day}', '{stime_object}',
                            '{etime_object}','{session_id}')
                        ''')
                return {"data":"okay"}
                
            
            except pyodbc.Error as ex:
                    return {"data":"error"}
        else:
            return {"data":"ae"}
        
    