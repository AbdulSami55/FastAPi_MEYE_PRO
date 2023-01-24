    
from sql import MySQL


class CheckTimeApi:
    def __init__(self,checktime) -> None:
        self.checktime = checktime
        
    def checktime_details(self):
        sql = MySQL()
        sql.__enter__()
        cursor = sql.conn.cursor()
        cursor.execute(f'''
                SELECT * FROM CheckTime
                    ''')
        checktime=None
        for row in cursor.fetchall():
            checktime = self.checktime.CheckTime(tsid = row.TS_ID,id=row.ID,totaltimein=row.TOTAL_TIME_IN,totaltimeout=row.TOTAL_TIME_OUT)
        
        return {"data":checktime
               }
    
    def checksingletime_details(self,tsid):
        sql = MySQL()
        sql.__enter__()
        cursor = sql.conn.cursor()
        cursor.execute(f'''
                SELECT * FROM CheckTime WHERE TS_ID='{tsid}'
                    ''')
        checktime=None
        for row in cursor.fetchall():
            checktime = self.checktime.CheckTime(tsid = row.TS_ID,id=row.ID,totaltimein=row.TOTAL_TIME_IN,totaltimeout=row.TOTAL_TIME_OUT)
        
        return {"data":checktime
               }
        
    def update_checktime_details(self,checktime):
        sql = MySQL()
        sql.__enter__()
        cursor = sql.conn.cursor()
        cursor.execute(f'''
                   UPDATE CheckTime SET TS_ID = '{checktime.tsid}',
                   TOTAL_TIME_IN='{checktime.totaltimein},
                   TOTAL_TIME_OUT='{checktime.totaltimeout}'
                   WHERE  ID='{checktime.id}'
                   ''')
    
        return {
                "data":checktime
                }
    def delete_checktime_details(self,checktime):
        sql = MySQL()
        sql.__enter__()
        cursor = sql.conn.cursor()
        cursor.execute(f'''
                   DELETE FROM CheckTime WHERE ID = '{checktime.id}'
                    ''')
    
        return {"data":"okay"}
    def add_checktime(self,checktime):
        sql = MySQL()
        sql.__enter__()
        cursor = sql.conn.cursor()
        cursor.execute(f'''
                INSERT INTO CheckTime
                VALUES
                ('{checktime.tsid}','{checktime.totaltimein}','{checktime.totaltimeout}')
                ''')

        return {"data":"okay"}