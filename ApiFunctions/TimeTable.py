import datetime
import pyodbc
import Model.Section as msection
import Model.Course as mcourse
import Model.Venue as mvenue
from sql import MySQL

class TimeTableApi:
    def __init__(self,timetable) -> None:
        self.timetable = timetable
        
    def timetable_details(self,timetableid):
        sql = MySQL()
        sql.__enter__()
        cursor = sql.conn.cursor()
        cursor.execute(f'''
                SELECT * FROM TIMETABLE WHERE ID='{timetableid}'
                    ''')
        timetable = ''
        section = ''
        venue =''
        course = ''
        for row in cursor.fetchall():
            st = row.START_TIME.split(':')
            et = row.END_TIME.split(':')
            st = f'{st[0]}:{st[1]}'
            et = f'{et[0]}:{et[1]}'
            timetable = self.timetable.TimeTable(id=row.ID,sectionID=row.SectionID
                                                ,starttime=st,
                                                endtime=et,
                                                day=row.DAY,courseID=row.CourseID,
                                                venueID=row.VenueID)
            cursor.execute(f'''
                SELECT * FROM SECTION WHERE ID='{row.SectionID}'
                    ''')
            for i in  cursor.fetchall():
                section = msection.Section(id=i.ID,name=i.NAME)
            cursor.execute(f'''
                SELECT * FROM COURSE WHERE ID='{row.CourseID}'
                    ''')
            for i in  cursor.fetchall():
                course = mcourse.Course(id=i.ID,courseID=i.CourseID,creditHours=i.CreditHours,name=i.Name)
            cursor.execute(f'''
                SELECT * FROM VENUE WHERE ID='{row.VenueID}'
                    ''')
            for i in  cursor.fetchall():
                venue = mvenue.Venue(id=i.ID,name=i.NAME)
          
   
        return {"timetable":timetable,
                "section":section,
                "course":course,
                "venue":venue}
    def update_timetable_details(self,timetable):
        sql = MySQL()
        sql.__enter__()
        cursor = sql.conn.cursor()
        cursor.execute(f'''
                   UPDATE TIMETABLE SET
                   SectionID='{timetable.sectionID}' , START_TIME='{timetable.starttime}',
                   END_TIME='{timetable.endtime}',DAY='{timetable.day}',CourseID='{timetable.courseID}',VenueID='{timetable.venueID}'
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
        stime_object = datetime.datetime.strptime(timetable.starttime.value, '%H:%M').time()
        etime_object = datetime.datetime.strptime(timetable.endtime.value, '%H:%M').time()
        day = timetable.day.value
        
        cursor.execute(f'''
                    SELECT * FROM TIMETABLE WHERE
                START_TIME='{stime_object}' AND END_TIME =
                '{etime_object}'
               AND DAY='{day}' AND VenueID='{timetable.venueID}'
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
                    '{timetable.sectionID}' , '{stime_object}',
                    '{etime_object}','{timetable.courseID}','{day}','{timetable.venueID}')
                        ''')
                return {"data":"okay"}
                
            
            except pyodbc.Error as ex:
                    return {"data":"error"}
        else:
            return {"data":"ae"}
        
    def getalltimetable(self):
        try:
            sql = MySQL()
            sql.__enter__()
            cursor = sql.conn.cursor()
            cursor.execute(f'''
                    SELECT * FROM TIMETABLE
                        ''')
            lsttimetable = []
            for row in cursor.fetchall():
                st = row.START_TIME.split(':')
                et = row.END_TIME.split(':')
                st = f'{st[0]}:{st[1]}'
                et = f'{et[0]}:{et[1]}'
                lsttimetable.append(self.timetable.TimeTable(id=row.ID,sectionID=row.SectionID
                                                    ,starttime=st,
                                                    endtime=et,
                                                    day=row.DAY,courseID=row.CourseID,
                                                    venueID=row.VenueID))
            return lsttimetable
        except:
            return [] 
        
    