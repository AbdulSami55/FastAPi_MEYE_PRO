import os
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
            lst.append(self.user.User(id=row.ID,userID=row.UserID,
                                 name=row.Name,password=row.Password,
                                 image=row.Image,role=row.Role))
    
        return lst
    
    def single_user_details(self,teacherName):
        sql = MySQL()
        sql.__enter__()
        cursor = sql.conn.cursor()
        cursor.execute(f'''
                SELECT * FROM MEYE_USER WHERE Name='{teacherName}'
                    ''')
        user=None
        for row in cursor.fetchall():
            user = self.user.User(id=row.ID,userID=row.UserID,
                                 name=row.Name,password=row.Password,
                                 image=row.Image,role=row.Role)
    
        return {"data":user}
    
    
    def update_user_details(self,user):
        sql = MySQL()
        sql.__enter__()
        cursor = sql.conn.cursor()
        cursor.execute(f'''
                   UPDATE MEYE_USER SET UserID = '{user.userID}',
                   Name='{user.name}',Password='{user.password}' ,
                   Image={user.image},Role={user.role}
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
            count=0
            sql = MySQL()
            sql.__enter__()
            cursor = sql.conn.cursor()
            cursor.execute(f'''
                    SELECT COUNT(UserId) as 'count' From MEYE_USER Where UserId='{user.userID}'
                    ''')
            for row in cursor.fetchall():
                count=row.count
            if count==0:
                try:
                    cursor.execute(f'''
                        INSERT INTO MEYE_USER
                        VALUES
                        ('{user.userID}','{user.name}','{user.password}','{user.image}','{user.role.value}')
                        ''')
                except:
                    cursor.execute(f'''
                        INSERT INTO MEYE_USER
                        VALUES
                        ('{user.userID}','{user.name}','{user.password}','{user.image}','{user.role}')
                        ''')
                
                return "Added"
            else:
                cursor.execute(f'''
                    SELECT Image  From MEYE_USER Where UserId='{user.userID}'
                    ''')
                image=''
                for row in cursor.fetchall():
                    image=row.Image
                if image!=user.image:
                    try:
                        os.remove(f'UserImages/{user.role.value}/{user.image}')
                    except:
                        os.remove(f'UserImages/{user.role}/{user.image}')
                return "Already Exists"
            
        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            if sqlstate == '23000':
                return "Already Exists"
            else:
                return "Error"
            
    def user_details_by_id(self,userId,password):
        sql = MySQL()
        sql.__enter__()
        cursor = sql.conn.cursor()
        cursor.execute(f'''
                SELECT * FROM MEYE_USER WHERE UserID='{userId}'
                    ''')
        
        for data in cursor.fetchall():
            cursor.execute(f'''
                SELECT * FROM MEYE_USER WHERE UserID='{userId}' and Password='{password}'
                    ''')
            for user in cursor.fetchall():
               return self.user.User(id=user.ID,userID=user.UserID,
                                 name=user.Name,password=user.Password,
                                 image=user.Image,role=user.Role)
            return "Invalid Password"
        return "User Not Found"
    
    