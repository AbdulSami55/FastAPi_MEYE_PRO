    
from sql import MySQL
import Model.User as muser
import Model.TeacherSlots as mteacherslots
import Model.Recordings as mrecordings
import Model.TimeTable as mtimetable 
import Model.Section as msection
import Model.Venue as mvenue
import Model.Course as mcourse

class RecordingsApi:
    def __init__(self,recordings) -> None:
        self.recordings = recordings
        
    def recordings_details(self):
        sql = MySQL()
        sql.__enter__()
        cursor = sql.conn.cursor()
        cursor.execute(f'''
                SELECT * FROM RECORDINGS
                    ''')
        lst=[]
        for row in cursor.fetchall():
            lst.append(self.recordings.Recordings(id=row.ID,teacherSlotID=row.TeachID,
                                                  filename=row.FILENAME,
                                                  date=row.DATE))
        
        return {"data":lst}
    
    def recordings_details_byteacherid(self,teacherid):
        sql = MySQL()
        sql.__enter__()
        cursor = sql.conn.cursor()
        lstteacherslot=[]
        lstrecordings=[]
        lsttimetable=[]
        lstsection=[]
        lstcourse=[]
        lstvenue=[]
        cursor.execute(f"SELECT * FROM TEACH WHERE TeacherID='{teacherid}'")
        for teachid in cursor.fetchall():
            tempcursor = sql.conn.cursor()
            tempcursor.execute(f'''
                    SELECT TS.*,R.*,TM.*,S.*,C.*,V.* FROM MEYE_USER TEACHER, 
                    TEACHERSLOTS TS INNER JOIN RECORDINGS R ON  R.TeacherSlotID=TS.ID , TEACH TH INNER JOIN  TIMETABLE TM ON TM.ID=TH.TimeTableID 
                    INNER JOIN SECTION S ON TM.SectionID=S.ID INNER JOIN VENUE V ON TM.VenueID=V.ID INNER JOIN COURSE C ON TM.CourseID=C.ID
                    WHERE TH.TeacherID='{teacherid}' AND TEACHER.ID='{teacherid}' AND TS.STATUS!=0
                    AND TS.TeachID={teachid.ID}
                        ''')
            
            
            for row in tempcursor.fetchall():
                st = row[10].split(':')
                et = row[11].split(':')
                st = f'{st[0]}:{st[1]}'
                et = f'{et[0]}:{et[1]}'
                lstteacherslot.append(mteacherslots.TeacherSlot(id=row[0],teachID=row[1],slot=row[2],status=row[3]))
                lstrecordings.append(self.recordings.Recordings(id=row[4],teacherSlotID=row[5],
                                                    filename=row[6],
                                                    date=str(row[7])))
                lsttimetable.append(mtimetable.TimeTable(id=row[8],sectionID=row[9],starttime = st,
                                                        endtime=et,day=row[13],courseCode=row[12],venueID=row[14]))
                lstsection.append(msection.Section(id=row[15],name=row[16]))
                lstcourse.append(mcourse.Course(id=row[17],courseCode=row[18],creditHours=row[19],name=row[20]))
                lstvenue.append(mvenue.Venue(id=row[21],name=row[22]))
        return {"teacherslot":lstteacherslot,
                "recordings":lstrecordings,
                "timetable":lsttimetable,
                "section":lstsection,
                "course":lstcourse,
                "venue":lstvenue}
    
    def update_recordings_details(self,recordings):
        sql = MySQL()
        sql.__enter__()
        cursor = sql.conn.cursor()
        cursor.execute(f'''
                   UPDATE RECORDINGS SET 
                   TeachID='{recordings.teacherSlotID}',FILENAME='{recordings.filename}',
                   DATE='{recordings.date}'
                   WHERE  ID='{recordings.id}'
                   ''')

        return {
                "data":recordings
                }
    def delete_recordings_details(self,recordings):
        sql = MySQL()
        sql.__enter__()
        cursor = sql.conn.cursor()
        cursor.execute(f'''
                   DELETE FROM RECORDINGS WHERE ID = '{recordings.id}'
                    ''')
    
        return {"data":"okay"}
    def add_recordings(self,recordings):
        sql = MySQL()
        sql.__enter__()
        cursor = sql.conn.cursor()
        cursor.execute(f'''
                INSERT INTO RECORDINGS
                VALUES
                ('{recordings.teacherSlotID}','{recordings.filename}','{recordings.date}')
                ''')
        return {"data":"okay"}
