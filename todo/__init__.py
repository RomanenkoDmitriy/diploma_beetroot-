from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = 'diploma beetroot academy'
# app.register_blueprint(routs)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/dimon/diplom_beetroot/data_base/db_user.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
manager = LoginManager(app)


from todo import routs

