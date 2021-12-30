from datetime import datetime
import os

from flask_login import current_user, UserMixin
# from flask_admin.contrib.sqla import ModelView
# from flask import request, redirect, url_for
from werkzeug.security import check_password_hash
# from flask_security import UserMixin, RoleMixin, SQLAlchemyUserDatastore
from flask_admin import Admin

from todo import db, manager


@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# roles_users = db.Table('roles_users',
#                        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
#                        db.Column('role_id', db.Integer(), db.ForeignKey('role_user.id')))


class User (db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String, unique=True, nullable=False)
    user_hash = db.Column(db.TEXT, nullable=False)
    email = db.Column(db.String, unique=True)
    data = db.Column(db.DateTime, default=datetime.utcnow())
    avatar = db.Column(db.String)
    active = db.Column(db.Boolean())
    announcement_table = db.relationship('Announcement', backref='user')
    # roles = db.relationship('RoleUser', secondary=roles_users, backref=db.backref('user', lazy='dynamic'))

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


# class RoleUser(db.Model, RoleMixin):
#     __tablename__ = 'role_user'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
#
#     def __str__(self):
#         return self.name








class Announcement(db.Model):
    __tablename__ = 'announcement'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    text = db.Column(db.TEXT, nullable=False)
    chapter = db.Column(db.String)
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


# class MyModelView(ModelView):
#
#     def is_accessible(self):
#         return current_user.has_role('admin')
#
#     def inaccessible_callback(self, name, **kwargs):
#         return redirect(url_for('login_user_page', next=request.url))


# class HomeAdmi(AdminIndexView):
#     def is_accessible(self):
#         return current_user.has_role('admin')
#
#     def inaccessible_callback(self, name, **kwargs):
#         return redirect(url_for('login', next=request.url))


# class MyAdmin:
#     def __init__(self, login, password):
#         self.login = login
#         self.password = password


# admin.add_view(MyModelView(User, db.session))
# admin.add_view(MyModelView(Announcement, db.session))
# admin.add_view(MyModelView(ImagesAnnouncement, db.session))







