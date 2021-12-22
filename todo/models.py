from datetime import datetime

from flask_login import UserMixin

from todo import db, manager


@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User (db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String, unique=True, nullable=False)
    user_hash = db.Column(db.TEXT, nullable=False)
    email = db.Column(db.String, unique=True)
    data = db.Column(db.DateTime, default=datetime.utcnow())
    avatar = db.Column(db.String)
    announcement_table = db.relationship('Announcement', backref='user')

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

    def add_avatar(self, path):
        self.avatar = path
        db.session.add(self)
        db.session.commit()



class Announcement(db.Model):
    __tablename__ = 'announcement'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    text = db.Column(db.TEXT, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    images_announcements = db.relationship('ImagesAnnouncement', backref='announcement')

    def change_title(self, title):
        self.title = title
        db.session.add(self)
        db.session.commit()

    def change_text(self, text):
        self.text = text
        db.session.add(self)
        db.session.commit()

    def del_announcement(self):
        db.session.delete(self)
        db.session.commit()


class ImagesAnnouncement(db.Model):
    __tablename__ = 'imagesannouncement'

    id = db.Column(db.Integer, primary_key=True)
    path_img = db.Column(db.String)
    id_announcement = db.Column(db.Integer, db.ForeignKey('announcement.id'))

    def __str__(self):
        return f'{self.path_img}'





