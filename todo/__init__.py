
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from todo.anons import announcement

UPLOAD_FOLDER = 'home/dimon/diplom_beetroot/static'

app = Flask(__name__)
app.register_blueprint(announcement)
app.secret_key = 'diploma beetroot academy'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/dimon/diplom_beetroot/data_base/db_user.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
manager = LoginManager(app)


from todo import routs

