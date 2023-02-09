    
from datetime import datetime
from sql import MySQL


class CheckTimeDetailsApi:
    def __init__(self,checktimedetails) -> None:
        self.checktimedetails = checktimedetails
        
    def checktimedetails_details(self):
        sql = MySQL()
        sql.__enter__()
        cursor = sql.conn.cursor()
        cursor.execute(f'''
                SELECT * FROM CheckTimeDetails
                    ''')
        lst=[]
        for row in cursor.fetchall():
            lst.append(self.checktimedetails.CheckTimeDetails(checkTimeID = row.CheckTimeID,id=row.ID,timein=row.TIME_IN,timeout=row.TIME_OUT))
        
        return {"data":lst
               }
    def update_checktimedetails_details(self,checktimedetails):
        sql = MySQL()
        sql.__enter__()
        cursor = sql.conn.cursor()
        cursor.execute(f'''
                   UPDATE CheckTimeDetails SET CheckTimeID = '{checktimedetails.checkTimeID}',
                   TIME_IN='{checktimedetails.timein},
                   TIME_OUT='{checktimedetails.timeout}'
                   WHERE  ID='{checktimedetails.id}'
                   ''')
    
        return {
                "data":checktimedetails
                }
    def delete_checktimedetails_details(self,checktimedetails):
        sql = MySQL()
        sql.__enter__()
        cursor = sql.conn.cursor()
        cursor.execute(f'''
                   DELETE FROM CheckTimeDetails WHERE ID = '{checktimedetails.id}'
                    ''')
    
        return {"data":"okay"}
    def add_checktimedetails(self,checktimedetails):
        sql = MySQL()
        sql.__enter__()
        cursor = sql.conn.cursor()
        t = datetime(checktimedetails.timein.year,checktimedetails.timein.month, checktimedetails.timein.day, checktimedetails.timein.hour, checktimedetails.timein.minute)
        t.strftime(f'%Y%m%d %H:%M:%S')
        t1 = datetime(checktimedetails.timeout.year,checktimedetails.timeout.month, checktimedetails.timeout.day, checktimedetails.timeout.hour, checktimedetails.timeout.minute)
        t1.strftime(f'%Y%m%d %H:%M:%S')
        cursor.execute(f'''
                INSERT INTO CHECKTIMEDETAILS
                VALUES
                ('{checktimedetails.checkTimeID}','{t}','{t1}')
                ''')

        return {"data":"okay"}
