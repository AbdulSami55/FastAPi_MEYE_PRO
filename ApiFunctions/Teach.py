    
from sql import MySQL

class TeachApi:
    def __init__(self,teach) -> None:
        self.teach = teach
        
    def teach_details(self,teacherid):
        sql = MySQL()
        sql.__enter__()
        cursor = sql.conn.cursor()
        cursor.execute(f'''
                SELECT * FROM TEACH WHERE T_ID='{teacherid}'
                    ''')
        lst=[]
        for row in cursor.fetchall():
            lst.append(self.teach.Teach(id=row.ID,tmid=row.TM_ID,tid=row.T_ID))
            
        return {"data":lst}
    def update_teach_details(self,teach):
        sql = MySQL()
        sql.__enter__()
        cursor = sql.conn.cursor()
        cursor.execute(f'''
                   UPDATE TEACH SET TM_ID = '{teach.tmid}',
                   T_ID='{teach.tid}'
                   WHERE  ID = '{teach.id}' 
                   ''')
    
        return {
               "data":teach
                }
    def delete_teach_details(self,teach):
        sql = MySQL()
        sql.__enter__()
        cursor = sql.conn.cursor()
        cursor.execute(f'''
                   DELETE FROM TEACH WHERE ID = '{teach.id}'
                    ''')
    
        return {"data":"okay"}
    def add_teach(self,teach):
        sql = MySQL()
        sql.__enter__()
        cursor = sql.conn.cursor()
        cursor.execute(f'''
                            SELECT * FROM MEYE_USER WHERE ID='{teach.tid}'
                            ''')
        role=''
        for row in cursor.fetchall():
            role=row.ROLE
        if role=='Teacher':
            cursor.execute(f'''
                            SELECT * FROM TEACH WHERE T_ID='{teach.tid}' 
                            AND TM_ID='{teach.tmid}'
                            ''')
            count=0
            for row in cursor.fetchall():
                count=1
            if count==0:
                cursor.execute(f'''
                        SELECT * FROM TIMETABLE
                        WHERE ID=
                        '{teach.tmid}'
                        ''')
                cid=-1
                for row in cursor.fetchall():
                   cid = row.C_ID
                cursor.execute(f'''
                        SELECT * FROM COURSE
                        WHERE ID=
                        '{cid}'
                        ''')
                cr_hour=-1
                for row in cursor.fetchall():
                   cr_hour = row.CR_HOURS
                try:
                    cursor.execute(f'''
                            INSERT INTO TEACH
                            VALUES
                            ('{teach.tmid}','{teach.tid}')
                            ''')
                    cursor.execute(f'''
                            SELECT * FROM TEACH
                            WHERE TM_ID=
                            '{teach.tmid}' AND T_ID='{teach.tid}'
                            ''')
                    th_id=-1
                    for i in cursor.fetchall():
                        th_id=i.ID
                    cursor.execute(f'''
                            INSERT INTO RULES
                            VALUES
                            ('{th_id}','{False}','{False}','{False}')
                            ''')
                    if cr_hour==3:
                        for i in range(1,33):
                            cursor.execute(f'''
                            INSERT INTO TEACHERSLOTS
                            VALUES
                            ('{th_id}','{i}','{0}')
                            ''')
                    elif cr_hour==2:
                        for i in range(1,17):
                            cursor.execute(f'''
                            INSERT INTO TEACHERSLOTS
                            VALUES
                            ('{th_id}','{i}','{0}')
                            ''')
                    elif cr_hour==4:
                        for i in range(1,49):
                            cursor.execute(f'''
                            INSERT INTO TEACHERSLOTS
                            VALUES
                            ('{th_id}','{i}','{0}')
                            ''')
                except:
                     cursor.execute(f'''
                            DELETE FROM TEACH
                             WHERE TM_ID=
                            '{teach.tmid}' AND T_ID='{teach.tid}'
                            ''')
                     cursor.execute(f'''
                            DELETE FROM TEACHERSLOTS
                            WHERE TH_ID=
                            '{th_id}'
                            ''')
                     return {"data":"Something Went Wrong"}
                    
                

                return {"data":"okay"}
            else:
                return {"data":"teacher already teach this class"}
        else:
            return {"data":"User is not teacher"}
