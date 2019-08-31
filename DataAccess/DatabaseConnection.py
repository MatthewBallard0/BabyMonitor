host = "BabyMonitor.db"
'''
import sqlite3
from sqlite3 import Error
 
class sqlConnector():
    def __init__(self, host):
        self.host = host

    def getAllUsers(self):
        conn = sqlite3.connect(self.host)
        cursor = conn.cursor()
        cursor.execute(''''''SELECT * FROM USERS'''''')
        return cursor.fetchall()
    def loginUserWithPassword(self, username, password):
        print(username, password)
        conn = sqlite3.connect(self.host)
        cursor = conn.cursor()
        cursor.execute("SELECT User_Name, User_Password " +
                          "FROM USERS " +
                          "WHERE User_Name='"+str(username)+"' AND " +
                                "User_Password='"+str(password)+"';")
        return cursor.fetchall()
    def showTables(self):
        conn = sqlite3.connect(self.host)
        cursor = conn.cursor()
        cursor.execute(''''''SELECT name, sql
                          FROM sqlite_master
                          WHERE type='table' AND
                                name='USERS' AND
                                name NOT LIKE 'sqlite_%';'''''')
        return cursor.fetchall()

if __name__ == '__main__':
    con = sqlConnector('pentestQuest.db')
    print(con.loginUserWithPassword('root', 'toor'))
'''
