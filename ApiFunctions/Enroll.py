
from sql import MySQL


class EnrollApi:
    def __init__(self,enroll) -> None:
        self.enroll = enroll
        
    def enroll_details(self):
        sql = MySQL()
        sql.__enter__()
        cursor = sql.conn.cursor()
        cursor.execute(f'''
                SELECT * FROM ENROLL
                    ''')
        lst=[]
        for row in cursor.fetchall():
            lst.append(self.enroll.Enroll(cid=row.C_ID,sid=row.S_ID,id=row.ID))

    
        return {"data":lst
               }
    def update_enroll_details(self,enroll):
        sql = MySQL()
        sql.__enter__()
        cursor = sql.conn.cursor()
        cursor.execute(f'''
                   UPDATE ENROLL SET 
                   C_ID='{enroll.cid}' ,  S_ID='{enroll.sid}'
                   WHERE  ID='{enroll.id}'
                   ''')
        return {"data":enroll}
    def delete_enroll_details(self,enroll):
        sql = MySQL()
        sql.__enter__()
        cursor = sql.conn.cursor()
        cursor.execute(f'''
                   DELETE FROM ENROLL WHERE ID = '{enroll.id}'
                    ''')
    
        return {"data":"okay"}
    def add_enroll(self,enroll):
        sql = MySQL()
        sql.__enter__()
        cursor = sql.conn.cursor()
        cursor.execute(f'''
                INSERT INTO ENROLL
                VALUES
                ('{enroll.cid}','{enroll.sid}')
                ''')
        return {"data":"okay"}
