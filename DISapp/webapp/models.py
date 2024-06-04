from datetime import datetime
from webapp import conn, login_manager
from flask_login import UserMixin
from psycopg2 import sql

@login_manager.user_loader
def load_user(user_id):
    cur = conn.cursor()
    cur.execute("""
    SELECT * FROM users
    WHERE id = %s
    """, (int(user_id),))
    if cur.rowcount > 0:
        return User(cur.fetchone())
    else:
        return None

class User(UserMixin):
    def __init__(self, user_data):
        self.id = user_data[0]
        self.username = user_data[1]
        self.email = user_data[2]
        self.password = user_data[3]
        self.role = user_data[4]

    def get_id(self):
       return self.id

def insert_user(username, email, password, role):
    cur = conn.cursor()
    sql = """
    INSERT INTO users(username, email, password, role)
    VALUES (%s, %s, %s, %s)
    """
    cur.execute(sql, (username, email, password, role))
    conn.commit()
    cur.close()

def select_user(username):
    cur = conn.cursor()
    sql = """
    SELECT * FROM users
    WHERE username = %s
    """
    cur.execute(sql, (username,))
    user = User(cur.fetchone()) if cur.rowcount > 0 else None
    cur.close()
    return user

def select_user_by_id(user_id):
    cur = conn.cursor()
    sql = """
    SELECT * FROM users
    WHERE id = %s
    """
    cur.execute(sql, (user_id,))
    user = User(cur.fetchone()) if cur.rowcount > 0 else None
    cur.close()
    return user
