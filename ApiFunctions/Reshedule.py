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


    def gettimetablebydates(self,startdate,enddate,lstday):
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
                if row.DAY in lstday:
                    lsttimetable.append(mtimetable.TimeTable(id=row.ID,sectionID=row.SectionID
                                                        ,starttime=st,
                                                        endtime=et,
                                                        day=row.DAY,courseCode=row.CourseID,
                                                        venueID=row.VenueID))
            cursor.execute(f'''
                    SELECT * FROM RESCHEDULE WHERE DATE >= '{startdate}' AND DATE <= '{enddate}' AND STATUS =0
                        ''')
            for row in cursor.fetchall():
                st = row.START_TIME.split(':')
                et = row.END_TIME.split(':')
                st = f'{st[0]}:{st[1]}'
                et = f'{et[0]}:{et[1]}'
                secid = 0
                courseCode = 0
                sql1 = MySQL()
                sql1.__enter__()
                cursor1 = sql1.conn.cursor()
                cursor1.execute(f'''
                   SELECT * FROM TEACHERSLOTS WHERE ID = '{row.TeacherSlotID}'
                        ''')
                for data in cursor1.fetchall():
                    cursor1.execute(f'''
                    SELECT * FROM TEACH WHERE ID = '{data.TeachID}'
                            ''')
                    for teachdata in cursor1.fetchall():
                        cursor1.execute(f'''
                        SELECT * FROM TIMETABLE WHERE ID = '{teachdata.TimeTableID}'
                                ''')
                        for timetabledata in cursor1.fetchall():
                            secid=timetabledata.SectionID
                            courseCode = timetabledata.CourseID
                lsttimetable.append(self.timetable.TimeTable(id=-1,sectionID=secid
                                                    ,starttime=st,
                                                    endtime=et,
                                                    day=row.DAY,
                                                    courseCode=courseCode,
                                                    venueID=row.VenueID))
            return lsttimetable
        except ZeroDivisionError:
            print(ZeroDivisionError)
            return [] 
    
                    
            