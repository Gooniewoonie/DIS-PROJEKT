from flask import Flask
import psycopg2
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)


app.config['SECRET_KEY'] = '64b5742e81858782e0510d41fff482e1'


conn = psycopg2.connect(
    dbname='DISPROJEKT',
    user='postgres',
    password='123',
    host='127.0.0.1',
    port='5430'
)

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'Login.login'
login_manager.login_message_category = 'info'

roles = ["admin","free-user", "bronze-user", "silver-user","gold-user"]
mysession = {"state": "initializing","role" : "Not assigned", "id": 0 , "age" : 202212}


from webapp.Login.routes import Login
app.register_blueprint(Login)




