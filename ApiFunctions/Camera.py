
from sql import MySQL


class CameraApi:
    def __init__(self,cam) -> None:
        self.cam = cam
        
    def camera_details(self,did):
        sql = MySQL()
        sql.__enter__()
        cursor = sql.conn.cursor()
        cursor.execute(f'''
                SELECT * FROM CAMERA WHERE DID ='{did}' 
                    ''')
        lst=[]
        for row in cursor.fetchall():
           lst.append(self.cam.Camera(id=row.ID,did=row.DID,vid=row.V_ID,no=row.NO))
        
        return {"data":lst}
        
    def update_camera_details(self,camera):
        sql = MySQL()
        sql.__enter__()
        cursor = sql.conn.cursor()
        cursor.execute(f'''
                   UPDATE CAMERA SET DID = '{camera.did}',
                   NO='{camera.no}' ,  V_ID='{camera.vid}'
                   WHERE ID ='{camera.id}'
                   ''')
    
        return {"data":camera}
    def delete_camera_details(self,camera):
        sql = MySQL()
        sql.__enter__()
        cursor = sql.conn.cursor()
        cursor.execute(f'''
                   DELETE FROM CAMERA WHERE ID = '{camera.id}'
                    ''')
    
        return {"data":"okay"}
    def add_camera(self,camera):
        sql = MySQL()
        sql.__enter__()
        cursor = sql.conn.cursor()
        cursor.execute(f'''
                INSERT INTO CAMERA
                VALUES
                ('{camera.did}','{camera.vid}','{camera.no}')
                ''')
        return {"data":"okay"}
