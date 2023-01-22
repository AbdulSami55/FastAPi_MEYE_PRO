import pyodbc

from sql import MySQL
class UserApi:
    def __init__(self,user) -> None:
        self.user = user
        
    def user_details(self):
        sql = MySQL()
        sql.__enter__()
        cursor = sql.conn.cursor()
        cursor.execute(f'''
                SELECT * FROM MEYE_USER
                    ''')
        lst=[]
        for row in cursor.fetchall():
            lst.append(self.user.User(id=row.ID,uid=row.UID,
                                 name=row.NAME,password=row.PASS,
                                 image=row.IMAGE,role=row.ROLE))
    
        return {"data":lst}
    
    def single_user_details(self,userid):
        sql = MySQL()
        sql.__enter__()
        cursor = sql.conn.cursor()
        cursor.execute(f'''
                SELECT * FROM MEYE_USER WHERE ID='{userid}'
                    ''')
        user=None
        for row in cursor.fetchall():
            user = self.user.User(id=row.ID,uid=row.UID,
                                 name=row.NAME,password=row.PASS,
                                 image=row.IMAGE,role=row.ROLE)
    
        return {"data":user}
    
    
    def update_user_details(self,user):
        sql = MySQL()
        sql.__enter__()
        cursor = sql.conn.cursor()
        cursor.execute(f'''
                   UPDATE MEYE_USER SET UID = '{user.uid}',
                   NAME='{user.name}',PASS='{user.password}' ,
                   IMAGE={user.image},ROLE={user.role}
                   WHERE ID ='{user.id}' ''')
    
        return {"data":user}
    def delete_user_details(self,user):
        sql = MySQL()
        sql.__enter__()
        cursor = sql.conn.cursor()
        cursor.execute(f'''
                   DELETE FROM MEYE_USER WHERE ID = '{user.id}'
                    ''')

        return {"data":"okay"}
    def add_user(self,user):
        try:
            sql = MySQL()
            sql.__enter__()
            cursor = sql.conn.cursor()
            cursor.execute(f'''
                    INSERT INTO MEYE_USER
                    VALUES
                    ('{user.uid}','{user.name}','{user.password}','{user.image}','{user.role.value}')
                    ''')
            return {"data":"okay"
                    }
        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            if sqlstate == '23000':
                return {"data":"ae"}
            else:
                return {"data":"error"}
                
        