import pyodbc
class MySQL:
    def __init__(self):
        self.conn = None

    def __enter__(self):
        self.conn =pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-KNM0289;'
                      'Database=MEYEPRO;'
                      'Trusted_Connection=yes;')
        self.conn.autocommit = True

    def __exit__(self, *args):
        if self.conn:
            self.conn.close()
            self.conn = None