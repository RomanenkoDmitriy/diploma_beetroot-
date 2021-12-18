from datetime import datetime

from flask_login import UserMixin

from todo import db, manager


@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User (db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String, unique=True, nullable=False)
    user_hash = db.Column(db.TEXT, nullable=False)
    email = db.Column(db.String, unique=True)
    data = db.Column(db.DateTime, default=datetime.utcnow())
    avatar = db.Column(db.String)
    announcement = db.relationship('Announcement', backref='announcement', lazy=True)

    def change_login(self, login):
        self.login = login
        db.session.add(self)
        db.session.commit()

    def change_password(self, password):
        self.user_hash = password
        db.session.add(self)
        db.session.commit()

    def change_email(self, email):
        self.email = email
        db.session.add(self)
        db.session.commit()

    def del_user(self):
        db.session.delete(self)
        db.session.commit()

    def add_avatar(self):
        pass


class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    text = db.Column(db.TEXT, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow())
    path_img = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return '< Announcement%r>' % self.id

