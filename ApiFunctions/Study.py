    
from sql import MySQL


class StudyApi:
    def __init__(self,study) -> None:
        self.study = study
        
    def study_details(self):
        sql = MySQL()
        sql.__enter__()
        cursor = sql.conn.cursor()
        cursor.execute(f'''
                SELECT * FROM STUDY
                    ''')
        lst=[]
        for row in cursor.fetchall():
            lst.append(self.study.Study(id=row.ID,teachID=row.TeachID,eid=row.E_ID))
        
        return {"data":lst}
    def update_study_details(self,study):
        sql = MySQL()
        sql.__enter__()
        cursor = sql.conn.cursor()
        cursor.execute(f'''
                   UPDATE STUDY SET 
                   TeachID='{study.teachID}',E_ID='{study.eid}'
                   WHERE  ID='{study.id}'
                   ''')
    
        return {
                "data":study
                }
    def delete_study_details(self,study):
        sql = MySQL()
        sql.__enter__()
        cursor = sql.conn.cursor()
        cursor.execute(f'''
                   DELETE FROM STUDY WHERE ID = '{study.id}'
                    ''')
    
      
        return {"data":"okay"}
    def add_study(self,study):
        sql = MySQL()
        sql.__enter__()
        cursor = sql.conn.cursor()
        cursor.execute(f'''
                INSERT INTO STUDY
                VALUES
                ('{study.teachID}','{study.eid}')
                ''')

        return {"data":"okay"}
