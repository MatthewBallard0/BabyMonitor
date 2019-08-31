import sqlite3
from sqlite3 import Error
 
 
def create_connection():
    """
        create a database connection to a database that resides
        in the memory
    """
    try:
        conn = sqlite3.connect('pentestQuest.db')
        c = conn.cursor()
# Create table - COUNTRY


        c.execute('''
            INSERT INTO users (userID, username, email, password, type) VALUES ('root', 'root@root.com', 'toor', 1, 0);
            ''')
        c.execute('''
            INSERT INTO users (userID, username, email, password, type) VALUES ('root1', 'root1@root.com', 'toor', 2, -1);
                        ''')
        c.execute('''
            INSERT INTO users (userID, username, email, password, type) VALUES ('root2', 'root2@root.com', 'toor', 2, -1);
                        ''')
        c.execute('''
            INSERT INTO users (userID, username, email, password, type) VALUES ('root3', 'root3@root.com', 'toor', 2, -1);
                        ''')
        c.execute('''
            INSERT INTO users (userID, username, email, password, type) VALUES ('root4', 'root4@root.com', 'toor', 2, -1);
                        ''')
        c.execute('''
            INSERT INTO users (userID, username, email, password, type) VALUES ('root5', 'root5@root.com', 'toor', 2, -1);
                        ''')
        c.execute('''
            INSERT INTO users (userID, username, email, password, type) VALUES ('root6', 'root6@root.com', 'toor', 1, 1);
        ''')

                 
        conn.commit()
        c.execute('''SELECT * FROM USERS''')
        print(c.fetchall())
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        conn.close()
 
if __name__ == '__main__':
    create_connection()

