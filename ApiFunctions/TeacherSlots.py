    
from sql import MySQL

class TeacherSlots:
    def __init__(self,teacherslots) -> None:
        self.teacherslots = teacherslots
        
    def teacherslots_details(self,teacherid):
        sql = MySQL()
        sql.__enter__()
        cursor = sql.conn.cursor()
        cursor.execute(f'''
                SELECT * FROM TeacherSlots WHERE TH_ID='{teacherid}'
                    ''')
        lst=[]
        for row in cursor.fetchall():
            lst.append(self.teacherslots.TeacherSlots(id=row.ID,thid=row.TH_ID,slot=row.SLOT,status=row.STATUS))
            
        return {"data":lst}
    def update_teacherslots_details(self,teacherslots):
        sql = MySQL()
        sql.__enter__()
        cursor = sql.conn.cursor()
        cursor.execute(f'''
                   UPDATE TEACHERSLOTS SET STATUS = '{teacherslots.status}'
                   WHERE  ID = '{teacherslots.id}' 
                   ''')
    
        return {
               "data":teacherslots
                }
    def delete_teacherslots_details(self,teacherslots):
        sql = MySQL()
        sql.__enter__()
        cursor = sql.conn.cursor()
        cursor.execute(f'''
                   DELETE FROM TEACHERSLOTS WHERE TH_ID = '{teacherslots.thid}'
                    ''')
    
        return {"data":"okay"}
    def add_teacherslots(self,teacherslots):
        sql = MySQL()
        sql.__enter__()
        cursor = sql.conn.cursor()
        cursor.execute(f'''
                           INSERT INTO TEACHERSLOTS VALUES('{teacherslots.id}','{teacherslots.thid}'
                           ,'{teacherslots.slot}','{teacherslots.status}')
                            ''')
        
