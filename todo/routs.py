from flask import request, render_template, flash, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user

from todo import app
from todo.models import User, db, load_user

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        user_hash = generate_password_hash(f'{login}{password}')
        user_db = User(login=login, user_hash=user_hash)
        try:
            db.session.add(user_db)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            # return render_template('base.html', error=str(e))
        user = User.query.all()
        return render_template('register.html', users=user)
    return render_template('register.html', users=User.query.all())


@app.route('/login', methods=['GET', 'POST'])
def login_user_page():
    login = request.form.get('login')
    password = request.form.get('password')
    if login and password:
        user_new = User.query.filter_by(login=login).first()
        if check_password_hash(user_new.user_hash, password):
            login_user(user_new)
            redirect('index.html')
        else:
            flash('Username or password is incorrect')
    else:
        flash('Enter login and password')
    return render_template('login.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def user_logout():
    logout_user()
    return render_template('index.html')


@app.route('/secret')
@login_required
def secret():
    return render_template('secret.html')
