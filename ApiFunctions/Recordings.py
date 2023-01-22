    
from sql import MySQL


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
            lst.append(self.recordings.Recordings(id=row.ID,tsid=row.TH_ID,
                                                  filename=row.FILENAME,
                                                  date=row.DATE))
        
        return {"data":lst}
    def update_recordings_details(self,recordings):
        sql = MySQL()
        sql.__enter__()
        cursor = sql.conn.cursor()
        cursor.execute(f'''
                   UPDATE RECORDINGS SET 
                   TH_ID='{recordings.tsid}',FILENAME='{recordings.filename}',
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
                ('{recordings.tsid}','{recordings.filename}','{recordings.date}')
                ''')
        return {"data":"okay"}
