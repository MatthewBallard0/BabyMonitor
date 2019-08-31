import sqlite3
from DataAccess import DatabaseConnection as db
from sqlite3 import Error

class userDAL():
    def __init__(self):
        pass
    '''
    lol wut is sql injection
    '''
    def loginUserWithPassword(self, username, password):
        conn = sqlite3.connect("BabyMonitor.db")
        cursor = conn.cursor()
        cursor.execute("SELECT username, password " +
                          "FROM USERS " +
                          "WHERE username='"+str(username)+"' AND " +
                                "password='"+str(password)+"';")
        return(cursor.fetchall())
