    
from sql import MySQL


class RulesApi:
    def __init__(self,rules) -> None:
        self.rules = rules
        
    def add_rules(self,rules,teacherName):
        sql = MySQL()
        sql.__enter__()
        cursor = sql.conn.cursor()
        lstTimetableId=[]
        for timetable in rules:
            lstTimetableId.append(timetable.timeTableId)
        cursor.execute(f'''
                     SELECT r.TimetableId FROM RULES r Inner JOin 
                     TIMETABLE t on t.ID=r.TimetableId Where t.TeacherName='{teacherName}'  
                       ''')
        for row in cursor.fetchall():
            if row.TimetableId not in lstTimetableId:
                cursor.execute(f'''
                        Delete FROM RULES  Where TimetableId={row.TimetableId}  
                        ''')
        for i in rules:
            cursor.execute(f'''
                       SELECT * FROM RULES WHERE TimeTableId='{i.timeTableId}'
                       ''')
            count=0
            for row in cursor.fetchall():
                count+=1
                cursor.execute(f'''
                       Update RULES Set StartRecord='{i.startRecord}',
                       MidRecord='{i.midRecord}',EndRecord='{i.endRecord}',
                       FullRecord='{i.fullRecord}'
                       WHERE TimeTableId='{i.timeTableId}'
                       ''')
            if count==0: 
                cursor.execute(f'''
                        INSERT INTO RULES
                        VALUES
                        ('{i.timeTableId}','{i.startRecord}','{i.midRecord}',
                        '{i.endRecord}','{i.fullRecord}')
                        ''')

        return "Added"
