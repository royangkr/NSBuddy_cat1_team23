from datetime import date
import sqlite3
from sqlite3 import Error

dbfile = 'nsbuddy.db'


# Initialise our required tables
def init():

    try:
        # Establish connection
        connection = sqlite3.connect(dbfile)
        cursor = connection.cursor()

        # Create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS USER(
                USERID TEXT PRIMARY KEY,
                GENDER TEXT,
                ORD TEXT,
                NAME TEXT DEFAULT ''
            );
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS FEEDBACK(
                USERID TEXT,
                DATETIME TEXT,
                MESSAGE TEXT,
                FOREIGN KEY (USERID)
                    REFERENCES USER (USERID)
                        ON UPDATE NO ACTION
                        ON DELETE NO ACTION
            );
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ALERT(
                USERID TEXT,
                DATETIME TEXT,
                ALERT TEXT,
                MESSAGE TEXT,
                FOREIGN KEY (USERID)
                    REFERENCES USER (USERID)
                        ON UPDATE NO ACTION
                        ON DELETE NO ACTION
            );
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS PCINTERVIEW(
                USERID TEXT,
                DATETIME TEXT,
                STATUS TEXT,
                FOREIGN KEY (USERID)
                    REFERENCES USER (USERID)
                        ON UPDATE NO ACTION
                        ON DELETE NO ACTION
            );
        ''')
        connection.commit()
    
    except Error as e:
        print(e)
    
    finally:
        if connection: connection.close()


# Add user's gender
def add_user_gender(userid, gender):

    try:
        # Establish connection
        connection = sqlite3.connect(dbfile)
        cursor = connection.cursor()

        # Find whether row exists
        cursor.execute('''
            SELECT * 
            FROM USER
            WHERE USERID = ?;
        ''', (userid,))

        # If row not found, create new row
        if len(cursor.fetchall()) == 0:
            cursor.execute('''
                INSERT INTO USER (USERID, GENDER) VALUES
                (?, ?);
            ''', (userid, gender))

        # Update existing row if exists
        else:
            cursor.execute('''
                UPDATE USER
                SET GENDER = ?
                WHERE USERID = ?;
            ''', (gender, userid))

        connection.commit()
    
    except Error as e:
        print(e)
    
    finally:
        if connection: connection.close()


# Add user's ord date
def add_user_ord(userid, ord):

    try:
        # Establish connection
        connection = sqlite3.connect(dbfile)
        cursor = connection.cursor()

        # Find whether row exists
        cursor.execute('''
            SELECT * 
            FROM USER
            WHERE USERID = ?;
        ''', (userid,))

        # If row not found, create new row
        if len(cursor.fetchall()) == 0:
            cursor.execute('''
                INSERT INTO USER (USERID, ORD) VALUES
                (?, ?);
            ''', (userid, ord))

        # Update existing row if exists
        else:
            cursor.execute('''
                UPDATE USER
                SET ORD = ?
                WHERE USERID = ?;
            ''', (ord, userid))

        connection.commit()
    
    except Error as e:
        print(e)
    
    finally:
        if connection: connection.close()


# Add user's name
def add_user_name(userid, name):

    try:
        # Establish connection
        connection = sqlite3.connect(dbfile)
        cursor = connection.cursor()

        # Find whether row exists
        cursor.execute('''
            SELECT * 
            FROM USER
            WHERE USERID = ?;
        ''', (userid,))

        # If row not found, create new row
        if len(cursor.fetchall()) == 0:
            cursor.execute('''
                INSERT INTO USER (USERID, NAME) VALUES
                (?, ?);
            ''', (userid, name))

        # Update existing row if exists
        else:
            cursor.execute('''
                UPDATE USER
                SET NAME = ?
                WHERE USERID = ?;
            ''', (name, userid))

        connection.commit()
    
    except Error as e:
        print(e)
    
    finally:
        if connection: connection.close()


# Add feedback
def add_feedback(userid, datetime, message):

    try:
        # Establish connection
        connection = sqlite3.connect(dbfile)
        cursor = connection.cursor()

        # Find whether user exists in user table
        cursor.execute('''
            SELECT * 
            FROM USER
            WHERE USERID = ?;
        ''', (userid,))

        # If user not found, create user
        if len(cursor.fetchall()) == 0:
            cursor.execute('''
                INSERT INTO USER (USERID) VALUES (?);
            ''', (userid, ))

        # Add feedback into table
        cursor.execute('''
            INSERT INTO FEEDBACK (USERID, DATETIME, MESSAGE) VALUES (?,?,?);
        ''', (userid, datetime, message))

        connection.commit()
    
    except Error as e:
        print(e)
    
    finally:
        if connection: connection.close()


# Add alert
def add_alert(userid, datetime, alert, message):

    try:
        # Establish connection
        connection = sqlite3.connect(dbfile)
        cursor = connection.cursor()

        # Find whether user exists in user table
        cursor.execute('''
            SELECT * 
            FROM USER
            WHERE USERID = ?;
        ''', (userid,))

        # If user not found, create user
        if len(cursor.fetchall()) == 0:
            cursor.execute('''
                INSERT INTO USER (USERID) VALUES (?);
            ''', (userid, ))

        # Add alert into table
        cursor.execute('''
            INSERT INTO ALERT (USERID, DATETIME, ALERT, MESSAGE) VALUES (?,?,?,?);
        ''', (userid, datetime, alert, message))

        connection.commit()
    
    except Error as e:
        print(e)
    
    finally:
        if connection: connection.close()


# Add pcinterview
def add_pcinterview(userid, datetime, status):

    try:
        # Establish connection
        connection = sqlite3.connect(dbfile)
        cursor = connection.cursor()

        # Find whether user exists in user table
        cursor.execute('''
            SELECT * 
            FROM USER
            WHERE USERID = ?;
        ''', (userid,))

        # If user not found, create user
        if len(cursor.fetchall()) == 0:
            cursor.execute('''
                INSERT INTO USER (USERID) VALUES (?);
            ''', (userid, ))

        # Add pcinterview into table
        cursor.execute('''
            INSERT INTO PCINTERVIEW (USERID, DATETIME, STATUS) VALUES (?,?,?);
        ''', (userid, datetime, status))

        connection.commit()
    
    except Error as e:
        print(e)
    
    finally:
        if connection: connection.close()
        
def update_pc_interview(userid, datetime, status):

    try:
        # Establish connection
        connection = sqlite3.connect(dbfile)
        cursor = connection.cursor()

        # Find whether row exists
        cursor.execute('''
            SELECT * 
            FROM PCINTERVIEW
            WHERE USERID = ? AND STATUS NOT IN ('completed','failed');
        ''', (userid,))

        # If row not found, add pc interview
        row=cursor.fetchone()
        if not row:
            return False

        # Update existing row if exists
        else:
            #print(str(row[1]))
            cursor.execute('''
                UPDATE PCINTERVIEW
                SET STATUS = ?
                WHERE USERID = ? AND DATETIME = ?;
            ''', (status, userid, row[1]))
        

        connection.commit()
        return True
    except Error as e:
        print(e)
    
    finally:
        if connection: connection.close()


# SELECT * FROM USER
def query_user_table():
    try:
        # Establish connection
        connection = sqlite3.connect(dbfile)
        cursor = connection.cursor()

        # Query table
        cursor.execute('''
            SELECT *
            FROM USER;
        ''')

        return cursor.fetchall()
    
    except Error as e:
        print(e)
    
    finally:
        if connection: connection.close()


# SELECT * FROM FEEDBACK
def query_feedback_table():
    try:
        # Establish connection
        connection = sqlite3.connect(dbfile)
        cursor = connection.cursor()

        # Query table
        cursor.execute('''
            SELECT *
            FROM FEEDBACK;
        ''')

        return cursor.fetchall()
    
    except Error as e:
        print(e)
    
    finally:
        if connection: connection.close()


# SELECT * FROM ALERT
def query_alert_table():
    
    try:
        # Establish connection
        connection = sqlite3.connect(dbfile)
        cursor = connection.cursor()

        # Query table
        cursor.execute('''
            SELECT *
            FROM ALERT;
        ''')

        return cursor.fetchall()
    
    except Error as e:
        print(e)
    
    finally:
        if connection: connection.close()


# SELECT * FROM PCINTERVIEW
def query_pcinterview_table():
    try:
        # Establish connection
        connection = sqlite3.connect(dbfile)
        cursor = connection.cursor()

        # Query table
        cursor.execute('''
            SELECT *
            FROM PCINTERVIEW;
        ''')

        return cursor.fetchall()
    
    except Error as e:
        print(e)
    
    finally:
        if connection: connection.close()


# Returns a list of feedback with user names
def display_feedback():
    try:
        # Establish connection
        connection = sqlite3.connect(dbfile)
        cursor = connection.cursor()

        # Query table
        cursor.execute('''
            SELECT U.NAME, F.MESSAGE, F.DATETIME 
            FROM FEEDBACK F
            INNER JOIN USER U
            ON F.USERID = U.USERID
        ''')

        return cursor.fetchall()
    
    except Error as e:
        print(e)
    
    finally:
        if connection: connection.close()


# Returns a list of alerts with user names
def display_alert():
    try:
        # Establish connection
        connection = sqlite3.connect(dbfile)
        cursor = connection.cursor()

        # Query table
        cursor.execute('''
            SELECT U.NAME, A.MESSAGE, A.DATETIME, A.ALERT
            FROM ALERT A
            INNER JOIN USER U
            ON A.USERID = U.USERID
        ''')

        return cursor.fetchall()
    
    except Error as e:
        print(e)
    
    finally:
        if connection: connection.close()


# Returns a list of pcinterviews with user names and status
def display_pcinterview():
    try:
        # Establish connection
        connection = sqlite3.connect(dbfile)
        cursor = connection.cursor()

        # Query table
        cursor.execute('''
            SELECT U.NAME, P.STATUS, P.DATETIME
            FROM PCINTERVIEW P
            INNER JOIN USER U
            ON P.USERID = U.USERID
        ''')

        return cursor.fetchall()
    
    except Error as e:
        print(e)
    
    finally:
        if connection: connection.close()
        
def delete_alert(userid, datetime):

    try:
        # Establish connection
        connection = sqlite3.connect(dbfile)
        cursor = connection.cursor()

        # Find whether user exists in user table
        cursor.execute('''
            DELETE FROM ALERT
            WHERE USERID = ? AND DATETIME = ?;
        ''', (userid, datetime))

        connection.commit()
    
    except Error as e:
        print(e)
    
    finally:
        if connection: connection.close()
        
def delete_feedback(userid, datetime):

    try:
        # Establish connection
        connection = sqlite3.connect(dbfile)
        cursor = connection.cursor()

        # Find whether user exists in user table
        cursor.execute('''
            DELETE FROM FEEDBACK
            WHERE USERID = ? AND DATETIME = ?;
        ''', (userid, datetime))

        connection.commit()
    
    except Error as e:
        print(e)
    
    finally:
        if connection: connection.close()
        
def delete_pcinterview(userid, datetime):

    try:
        # Establish connection
        connection = sqlite3.connect(dbfile)
        cursor = connection.cursor()

        # Find whether user exists in user table
        cursor.execute('''
            DELETE FROM PCINTERVIEW
            WHERE USERID = ? AND DATETIME = ?;
        ''', (userid, datetime))

        connection.commit()
    
    except Error as e:
        print(e)
    
    finally:
        if connection: connection.close()
        
if __name__ == '__main__':
    init()
    print(str(display_alert()))
    print(str(display_feedback()))
    print(str(display_pcinterview()))
    