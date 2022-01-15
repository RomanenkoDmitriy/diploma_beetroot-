import logging
from logging import config

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager





UPLOAD_FOLDER = 'home/dimon/diplom_beetroot/static'
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'my_formatter': {
            'format': '{levelname} {asctime} {message}',
            'style': '{'
        },
    },

    'handlers': {
        'file_handler': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/home/dimon/diplom_beetroot/logger.txt',
            'mode': 'a',
            'encoding': 'UTF-8',
            'formatter': 'my_formatter',
        },
    },

    'loggers': {
        'logger': {
            'handlers': ['file_handler'],
            'level': 'DEBUG',
            'propagate': True
        }
    }
}

app = Flask(__name__)

app.secret_key = 'diploma beetroot academy'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/dimon/diplom_beetroot/data_base/db_user.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

manager = LoginManager(app)


logger = logging.getLogger('logger')
logging.config.dictConfig(LOGGING_CONFIG)

from todo import routs

