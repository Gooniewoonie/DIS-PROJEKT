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
            cur.execute(f"SELECT {id_column}, name, '{table}' FROM {table} WHERE {id_column} = %s", (int(user_id),))
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
    
    

# class User(UserMixin):
#     def __init__(self, user_data):
#         self.id = user_data[0]
#         self.name = user_data[1]
#         self.role = user_data[2]


class User(UserMixin):
    def __init__(self, user_data):
        self.id = user_data[0]
        self.username = user_data[1]
        self.email = user_data[2]
        self.password = user_data[3]
        self.role = user_data[4]
        self.recommendation_count = user_data[5] 


    def get_id(self):
       return self.id

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
            cur.execute(f"SELECT {id_column}, name, '{table}' FROM {table} WHERE {id_column} = %s", (int(user_id),))
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
        self.role = user_data[2]

    def get_id(self):
        return self.id

def insert_user(username, email, password, role):
    table_mapping = {
        'free-user': 'FreeUser',
        'bronze-user': 'BronzeUser',
        'silver-user': 'SilverUser',
        'gold-user': 'GoldUser',
        'admin': 'Admins'
    }

    user_table = table_mapping.get(role)
    if not user_table:
        raise ValueError("Invalid role specified")

    try:
        cur = conn.cursor()
        cur.execute(f"INSERT INTO {user_table} (name, password) VALUES (%s, %s)", (username, password))
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
            cur.execute(f"SELECT * FROM {table} WHERE name = %s", (username,))
            if cur.rowcount > 0:
                user_data = cur.fetchone()
                user_role = table
                user_data = list(user_data) + [user_role]  # Add role to user_data
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
            cur.execute(f"SELECT {id_column}, name, '{table}' FROM {table} WHERE {id_column} = %s", (int(user_id),))
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
        'FreeUser': 'SELECT F_userID, name, \'FreeUser\' FROM FreeUser WHERE name ~* %s',
        'BronzeUser': 'SELECT B_userID, name, \'BronzeUser\' FROM BronzeUser WHERE name ~* %s',
        'SilverUser': 'SELECT S_userID, name, \'SilverUser\' FROM SilverUser WHERE name ~* %s',
        'GoldUser': 'SELECT G_userID, name, \'GoldUser\' FROM GoldUser WHERE name ~* %s',
        'Admins': 'SELECT A_userID, name, \'Admins\' FROM Admins WHERE name ~* %s',
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
        print(f"Error searching users: {e}")
    return users
    
