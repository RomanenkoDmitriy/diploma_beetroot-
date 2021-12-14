from datetime import datetime

from flask_login import UserMixin

from todo import db, manager


@manager.user_loader
def load_user(user_id):
    return User.get(user_id)


class User (db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String, unique=True, nullable=False)
    user_hash = db.Column(db.TEXT, nullable=False)
    announcement = db.relationship('Announcement', backref='announcement', lazy=True)
    data = db.Column(db.DateTime, default=datetime.utcnow())


class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    text = db.Column(db.TEXT, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow())
    path_img = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return '< Announcement%r>' % self.id
