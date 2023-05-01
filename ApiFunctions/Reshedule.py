import Model.TimeTable as mtimetable
from sql import MySQL
import Model.TimeTable as mtimetable

class RescheduleApi:
    def __init__(self,reschedule) -> None:
        self.reschedule = reschedule
        
    def getTimetable(self):
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
            lsttimetable.append(mtimetable.TimeTable(id=row.ID,sectionID=row.SectionID
                                                ,starttime=st,
                                                endtime=et,
                                                day=row.DAY,courseCode=row.CourseID,
                                                venueID=row.VenueID))
       
        # self.conn.commit()
        return {"data":lsttimetable,
                }
        
    def reschedule_details(self):
        sql = MySQL()
        sql.__enter__()
        cursor = sql.conn.cursor()
        cursor.execute(f'''
                SELECT * FROM RESCHEDULE
                    ''')
        lst=[]
        for row in cursor.fetchall():
            lst.append(self.reschedule.Reschedule(id=row.ID,teachID=row.TeachID,
                                                  venueID=row.VenueID,status=row.STATUS,
                                                  date=row.DATE))
        
        return {"data":lst}
    def update_reschedule_details(self,reschedule):
        sql = MySQL()
        sql.__enter__()
        cursor = sql.conn.cursor()
        cursor.execute(f'''
                   UPDATE RESCHEDULE SET 
                   TeachID='{reschedule.teachID}',VenueID='{reschedule.venueID}',
                   STATUS ='{reschedule.status}',
                   DATE='{reschedule.date}'
                   WHERE  ID='{reschedule.id}'
                   ''')
    
        return {
                "data":reschedule
                }
    def delete_reschedule_details(self,reschedule):
        sql = MySQL()
        sql.__enter__()
        cursor = sql.conn.cursor()
        cursor.execute(f'''
                   DELETE FROM RESCHEDULE WHERE ID = '{reschedule.id}'
                    ''')
    
        return {"data":"okay"}
    
    def add_reschedule(self,reschedule):
        sql = MySQL()
        sql.__enter__()
        cursor = sql.conn.cursor()
        if reschedule.starttime.name == reschedule.endtime.name:
            cursor.execute(f'''
                    INSERT INTO RESCHEDULE
                    VALUES
                    ('{reschedule.teachID}','{reschedule.venueID}',
                    '{reschedule.status}','{reschedule.starttime.value}'
                    ,'{reschedule.endtime.value}','{reschedule.day.value}')
                    ''')
            return {"data":"okay"}
        else:
             return {"data":"Time Miss Match"}


    def checkTeacherRescheduleClass(self,teacherName):
       sql = MySQL()
       sql.__enter__()
       cursor = sql.conn.cursor()
       cursor.execute(f'''
                    SELECT ts.ID,r.Status  FROM  TEACHERSLOTS ts left Join RESCHEDULE r
                    on r.TeacherSlotId=ts.ID Inner Join TIMETABLE t 
                    on t.ID=ts.TimeTableId Where t.TeacherName='{teacherName}' 
                    And ts.Status='Not Held'
                    ''')
       id=-1
       for row in cursor.fetchall():
           if row.Status!=0:
               id=row.ID
               break
       if id==-1:
            return "No Class Missed"
       return id