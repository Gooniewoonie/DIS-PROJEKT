from flask import Flask,request,render_template
import psycopg2
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)


app.config['SECRET_KEY'] = ''

db = "dbname= 'DISPROJEKT' user = 'postgres' host = '127.0.0.1' password = ''"
# TODO: Find password, and check dbname, user etc.
conn = psycopg2.connect(db)

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

roles = ["admin","free-user", "bronze-user", "silver-user","gold-user"]
print(roles)
mysession = {"state": "initializing","role" : "Not assigned", "id": 0 , "age" : 202212}


from appDIS import Login

app.register_blueprint(Login)




