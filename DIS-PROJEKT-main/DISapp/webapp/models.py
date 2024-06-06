from datetime import datetime
from webapp import conn, login_manager
from flask_login import UserMixin
import psycopg2

@login_manager.user_loader
def load_user(user_id):
    try:
        cur = conn.cursor()
        user_types = [
            ('FreeUser', 'F_userID'),
            ('BronzeUser', 'B_userID'),
            ('SilverUser', 'S_userID'),
            ('GoldUser', 'G_userID'),
            ('Admins', 'A_userID')
        ]

        for table, id_column in user_types:
            cur.execute(f"SELECT {id_column}, name, password, '{table}' FROM {table} WHERE {id_column} = %s", (int(user_id),))
            if cur.rowcount > 0:
                user_data = cur.fetchone()
                cur.close()
                return User(user_data)

        cur.close()
        return None
    except psycopg2.Error as e:
        conn.rollback()
        print(f"Error loading user: {e}")
        return None

class User(UserMixin):
    def __init__(self, user_data):
        self.id = user_data[0]
        self.name = user_data[1]
        self.password = user_data[2]
        self.role = user_data[3]

    def get_id(self):
        return self.id

def insert_user(username, password, role):
    try:
        cur = conn.cursor()
        
        if role == 'free-user':
            cur.execute("""
                INSERT INTO FreeUser (password, name)
                VALUES (%s, %s)
                RETURNING F_userID
            """, (password, username))
            user_id = cur.fetchone()[0]
            cur.execute("""
                INSERT INTO Accounts (created_date, F_userID)
                VALUES (CURRENT_DATE, %s)
            """, (user_id,))
        elif role == 'bronze-user':
            cur.execute("""
                INSERT INTO BronzeUser (password, name)
                VALUES (%s, %s)
                RETURNING B_userID
            """, (password, username))
            user_id = cur.fetchone()[0]
            cur.execute("""
                INSERT INTO Accounts (created_date, B_userID)
                VALUES (CURRENT_DATE, %s)
            """, (user_id,))
        elif role == 'silver-user':
            cur.execute("""
                INSERT INTO SilverUser (password, name)
                VALUES (%s, %s)
                RETURNING S_userID
            """, (password, username))
            user_id = cur.fetchone()[0]
            cur.execute("""
                INSERT INTO Accounts (created_date, S_userID)
                VALUES (CURRENT_DATE, %s)
            """, (user_id,))
        elif role == 'gold-user':
            cur.execute("""
                INSERT INTO GoldUser (password, name)
                VALUES (%s, %s)
                RETURNING G_userID
            """, (password, username))
            user_id = cur.fetchone()[0]
            cur.execute("""
                INSERT INTO Accounts (created_date, G_userID)
                VALUES (CURRENT_DATE, %s)
            """, (user_id,))
        elif role == 'admin':
            cur.execute("""
                INSERT INTO Admins (password, name)
                VALUES (%s, %s)
                RETURNING A_userID
            """, (password, username))
            user_id = cur.fetchone()[0]
            cur.execute("""
                INSERT INTO Accounts (created_date, A_userID)
                VALUES (CURRENT_DATE, %s)
            """, (user_id,))

        conn.commit()
        cur.close()
    except psycopg2.Error as e:
        conn.rollback()
        print(f"Error inserting user: {e}")



def select_user(username):
    try:
        cur = conn.cursor()
        user_types = ['FreeUser', 'BronzeUser', 'SilverUser', 'GoldUser', 'Admins']
        for table in user_types:
            cur.execute(f"SELECT name, password, '{table}' FROM {table} WHERE name = %s", (username,))
            if cur.rowcount > 0:
                user_data = cur.fetchone()
                user_data = (cur.rowcount, *user_data) 
                cur.close()
                return User(user_data)
        cur.close()
        return None
    except psycopg2.Error as e:
        conn.rollback()
        print(f"Error selecting user: {e}")
        return None

def select_user_by_id(user_id):
    try:
        cur = conn.cursor()
        user_types = [
            ('FreeUser', 'F_userID'),
            ('BronzeUser', 'B_userID'),
            ('SilverUser', 'S_userID'),
            ('GoldUser', 'G_userID'),
            ('Admins', 'A_userID')
        ]

        for table, id_column in user_types:
            cur.execute(f"SELECT {id_column}, name, password, '{table}' FROM {table} WHERE {id_column} = %s", (int(user_id),))
            if cur.rowcount > 0:
                user_data = cur.fetchone()
                cur.close()
                return User(user_data)
        cur.close()
        return None
    except psycopg2.Error as e:
        conn.rollback()
        print(f"Error selecting user by id: {e}")
        return None

def search_users(pattern):
    users = []
    queries = {
        'FreeUser': 'SELECT F_userID, name, password, \'FreeUser\' FROM FreeUser WHERE name ~* %s',
        'BronzeUser': 'SELECT B_userID, name, password, \'BronzeUser\' FROM BronzeUser WHERE name ~* %s',
        'SilverUser': 'SELECT S_userID, name, password, \'SilverUser\' FROM SilverUser WHERE name ~* %s',
        'GoldUser': 'SELECT G_userID, name, password, \'GoldUser\' FROM GoldUser WHERE name ~* %s',
        'Admins': 'SELECT A_userID, name, password, \'Admins\' FROM Admins WHERE name ~* %s',
    }

    try:
        cur = conn.cursor()
        for role, query in queries.items():
            cur.execute(query, (pattern,))
            results = cur.fetchall()
            for result in results:
                users.append(User(result))
        cur.close()
    except psycopg2.Error as e:
        conn.rollback()
        print(f"errror searching users: {e}")
    return users



    
