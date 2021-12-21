
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
# from todo.utils.utils import redirect_user

# from todo.anons import anons

UPLOAD_FOLDER = 'home/dimon/diplom_beetroot/static'

app = Flask(__name__)

# app.register_blueprint(anons)
app.secret_key = 'diploma beetroot academy'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/dimon/diplom_beetroot/data_base/db_user.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
manager = LoginManager(app)
manager.login_view = 'login_user_page'
manager.login_message = 'Log in to view closed content'
manager.login_message_category = 'success'


from todo import routs

