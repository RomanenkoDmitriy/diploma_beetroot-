
from flask import Flask, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
# from flask_admin import Admin, AdminIndexView, expose






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


# class HomeAdmin(AdminIndexView):
#     def is_accessible(self):
#         return current_user.has_role('admin')
#
#     def inaccessible_callback(self, name, **kwargs):
#         return redirect(url_for('admin_index', next=request.url))
#
#     @expose('/admin')
#     def admin_index(self):
#         return self.render('admin/base_admin.html')
#
#
# admin = Admin(app, name='Admin', index_view=HomeAdmin())



from todo import routs

