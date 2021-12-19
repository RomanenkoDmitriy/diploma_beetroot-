import os

import flask_login
from flask import request, render_template, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

from todo import app
from todo.models import User, db, Announcement, ImagesAnnouncement


@app.route('/')
def index_page():
    if Announcement.query.all():
        return render_template('index.html', announcement=Announcement.query.order_by(Announcement.date.desc()).all())
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        password1 = request.form['password1']
        email = request.form['email']
        user_hash = generate_password_hash(password)
        if password == password1:
            user_db = User(login=login, user_hash=user_hash, email=email)
            try:
                db.session.add(user_db)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                # return render_template('base.html', error=str(e))
        else:
            flash('Password mismatch')
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

            # redirect_page = request.args.get('next')
            return redirect(url_for('index_page'))
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


@app.route('/personal_area', methods=['GET', 'POST'])
@login_required
def personal_area():
    user = flask_login.current_user
    user_id = user.id

    if request.method == 'POST':
        login = request.form.get('login')
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        email = request.form.get('email')
        delete_user = request.form.get('delete')
        file = request.files.get('avatar')
        anonc = request.form.get('anonc')
        editing = request.form.get('editing')

        if anonc:
            return redirect('create_announcement')
        if editing:
            return redirect('editing_announcement')

        if login:
            user.change_login(login)
            return render_template('personal_area.html', user=User.query.filter_by(id=user_id).first().login)
        elif old_password and new_password:

            if check_password_hash(user.user_hash, old_password):
                user.change_password(generate_password_hash(new_password))
                return render_template('personal_area.html', user=User.query.filter_by(id=user_id).first().user_hash)
            else:
                flash('Invalid password')

        elif email:
            user.change_email(email)
            return render_template('personal_area.html', user=User.query.filter_by(id=user_id).first().email)
        elif delete_user:
            user.del_user()
            return redirect(url_for('index_page'))
        elif file:
            path = os.path.join(os.getcwd(), 'static', f'{user.login}.jpg')
            file.save(path)

    return render_template('personal_area.html')


@app.route('/create_announcement', methods=['GET', 'POST'])
@login_required
def create_announcement():
    title = request.form.get('title')
    text = request.form.get('text')

    if request.method == 'POST':
        new_announcement = Announcement(title=title, text=text, user_id=current_user.id)
        try:
            db.session.add(new_announcement)
            db.session.commit()
            flash('Announcement created')
            return render_template('add_announcement.html', anonc=current_user.announcement_table)
        except Exception as e:
            db.session.rollback()
            return render_template('add_announcement.html', error=str(e))
    return render_template('add_announcement.html', anonc=current_user.announcement_table)


@app.route('/editing_announcement', methods=['GET', 'POST'])
@login_required
def editing_announcement():
    change = request.form.get('change')
    del_anons = request.form.get('delete')
    if request.method == 'POST':
        if del_anons:
            anons = Announcement.query.filter_by(id=del_anons).first()
            anons.del_announcement()
        elif change:
            return render_template('change_anons.html', chenge_anons=Announcement.query.filter_by(id=change).first())
    return render_template('editing_announsement.html', announsement=current_user.announcement_table)


@app.route('/change_anons', methods=['GET', 'POST'])
@login_required
def change_anons():
    title = request.form.get('title')
    text = request.form.get('text')
    id_anons = request.form.get('id_anons')
    if request.method == 'POST':
        return render_template('change_anons.html', ia_a=id_anons)
        anons = Announcement.query.filter_by(id=id_anons).first()
        if title and text:
            anons.change_title(title)
            anons.change_text(text)
        elif title:
            anons.change_title(title)
        elif text:
            anons.change_text(text)
    return render_template('change_anons.html', chenge_anons=Announcement.query.filter_by(id=change).first())


# @app.after_request
# @login_required
# def redirect_page(response):
#     if response.status.code == 401:
#         return redirect(f'{url_for("login_user_page")}?next={request.url}')
#     return response

