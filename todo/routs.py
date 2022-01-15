from os.path import join, dirname, realpath

import flask_login
from flask import request, render_template, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_login import login_user, login_required, logout_user, current_user

from todo import app, db, logger
from todo.models import User, Announcement, ImagesAnnouncement
from todo.utils.utils import avatar_img, answer_bal


#Index------------------------------------------------------------------------------------------

@app.route('/')
def index_page():
    try:
        if Announcement.query.all():
            image = ImagesAnnouncement.query.all()
            logger.info(f'{index_page.__name__} OK')

            return render_template('index.html',
                                   announcement=Announcement.query.order_by(Announcement.date.desc()).all(),
                                   img=image, title='Home page')
        else:
            flash('No ads')
            return render_template('index.html', title='Home page')
    except Exception as e:
        flash('An error occured, please try again')
        logger.error(f'{index_page.__name__} {e}')
        return render_template('index.html', title='Home page')




@app.route('/category/<string:chapter>')
def announcement_chapter(chapter):
    try:
        announcement = Announcement.query.filter_by(chapter=chapter).all()
    except Exception as e:
        logger.error(f'{announcement_chapter.__name__} {e}')
        flash('An error occured, please try again')
        return render_template('index.html', announcement=announcement, title='Announcement chapter')
    else:
        logger.info(f'{announcement_chapter.__name__} OK')
        return render_template('index.html', announcement=announcement, title='Announcement chapter')

#User----------------------------------------------------------------------------------------------

@app.route('/register', methods=['GET', 'POST'])
def register():
    try:
        if request.method == 'POST':
            login = request.form['login']
            password = request.form['password']
            password1 = request.form['password1']
            email = request.form['email']
            user_hash = generate_password_hash(password)
            if password == password1:
                user = User.query.filter_by(login=login).first()
                if user:
                    flash('Choose another username')
                    return render_template('register.html', title='Register')
                user = User.query.filter_by(email=email).first()
                if user:
                    flash('Choose another email')
                    return render_template('register.html', title='Register')
                user_db = User(login=login, user_hash=user_hash, email=email)

                db.session.add(user_db)
                db.session.commit()
                return redirect(url_for('login_user_page'))
            else:
                flash('Password mismatch')
    except Exception as e:
        logger.error(f'{register.__name__} {e}')
        flash('An error occured, please try again')
        db.session.rollback()
        return render_template('register.html', title='Register')
    else:
        logger.info(f'{register.__name__} OK')
    return render_template('register.html', title='Register')


@app.route('/login_user', methods=['GET', 'POST'])
def login_user_page():
    try:
        if request.method == 'POST':
            login_form = request.form.get('login')
            password_form = request.form.get('password')
            next_page = request.args.get('next_page')
            if login_form and password_form:
                user_new = User.query.filter_by(login=login_form).first()
                if user_new is not None:

                    if check_password_hash(user_new.user_hash, password_form):
                        login_user(user_new)
                        if next_page:
                            return redirect(next_page)
                        return redirect(url_for('index_page'))
                    else:
                        flash('Password is incorrect')
                else:
                    flash('Invalid login')
            else:
                flash('Enter login and password')
    except Exception as e:
        logger.error(f'{login_user_page.__name__} {e}')
        flash('An error occured, please try again')
        return render_template('login.html', title='Login')
    else:
        logger.info(f'{login_user_page.__name__} ok')
    return render_template('login.html', title='Login')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def user_logout():
    try:
        logout_user()
        logger.info(f'{user_logout.__name__} OK')
        return redirect(url_for('index_page'))
    except Exception as e:
        flash('An error occured, please try again')
        logger.error(f'{user_logout.__name__} {e}')




@app.route('/personal_area', methods=['GET', 'POST'])
@login_required
def personal_area():
    try:
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
                flash('Your login has been changed')
            elif old_password and new_password:

                if check_password_hash(user.user_hash, old_password):
                    user.change_password(generate_password_hash(new_password))
                    flash('Your password has been changed')
                else:
                    flash('Invalid password')

            elif email:
                user.change_email(email)
                flash('Your email has been changed')

            elif delete_user:
                announcements = Announcement.query.filter_by(user_id=user_id).all()
                for anons in announcements:
                    img = ImagesAnnouncement.query.filter_by(id_announcement=anons.id).first()
                    anons.del_announcement()
                    img.del_image()
                user.del_user()
                return redirect(url_for('index_page'))

            elif file:
                path = join(dirname(realpath(__file__)), 'static', secure_filename(file.filename))
                avatar_img(file, path)
                user.add_avatar(file.filename)
        logger.info(f'{personal_area.__name__} OK')
    except Exception as e:
        db.session.rollback()
        logger.error(f'{personal_area.__name__} {e}')
        flash('An error occured, please try again')
        return render_template('personal_area.html', title='Personal area')
    return render_template('personal_area.html', title='Personal area')

#Announcement-------------------------------------------------------------------------------------------------

@app.route('/create_announcement', methods=['GET', 'POST'])
@login_required
def create_announcement():
    try:
        title = request.form.get('title')
        text = request.form.get('text')
        file = request.files.get('foto')
        chapter = request.form.get('chapter')
        contact = request.form.get('contact')

        if request.method == 'POST':
            new_announcement = Announcement(title=title, text=text, chapter=chapter,
                                            contact_details=contact, user_id=current_user.id)

            db.session.add(new_announcement)
            db.session.commit()
            if file:
                path = join(dirname(realpath(__file__)), 'static', secure_filename(file.filename))
                images = ImagesAnnouncement(path_img=file.filename, id_announcement=new_announcement.id)
                db.session.add(images)
                db.session.commit()
                avatar_img(file, path)
            flash('Announcement created')

        logger.info(f'{create_announcement.__name__} OK')
    except Exception as e:
        logger.error(f'{create_announcement.__name__} {e}')
        db.session.rollback()
        flash('An error occured, please try again')
        return render_template('add_announcement.html', title='Create announcement')
    return render_template('add_announcement.html', title='Create announcement')


@app.route('/editing_announcement', methods=['GET', 'POST'])
@login_required
def editing_announcement():
    try:
        change = request.form.get('change')
        del_anons = request.form.get('delete')
        if request.method == 'POST':
            if del_anons:
                anons = Announcement.query.filter_by(id=del_anons).first()
                anons.del_announcement()
            elif change:
                return render_template('change_anons.html', chenge_anons=Announcement.query.filter_by(id=change).first())
        logger.info(f'{editing_announcement.__name__} OK')
    except Exception as e:
        logger.error(f'{editing_announcement.__name__} {e}')
        flash('An error occured, please try again')
        return render_template('editing_announsement.html', announsement=current_user.announcement_table,
                               title='Editing announcement')
    return render_template('editing_announsement.html', announsement=current_user.announcement_table,
                           title='Editing announcement')


@app.route('/<int:id_anons>/change_anons', methods=['GET', 'POST'])
@login_required
def change_anons(id_anons):
    try:
        title = request.form.get('title')
        text = request.form.get('text')

        if request.method == 'POST':
            anons = Announcement.query.filter_by(id=id_anons).first()

            if title and text:
                anons.change_title(title)
                anons.change_text(text)
            elif title:
                anons.change_title(title)
            elif text:
                anons.change_text(text)
        logger.info(f'{change_anons.__name__} OK')
    except Exception as e:
        logger.error(f'{change_anons.__name__} {e}')
        db.session.rollback()
        flash('An error occured, please try again')
        return render_template('change_anons.html', chenge_anons=Announcement.query.filter_by(id=id_anons).first(),
                           title='Change anons')
    return render_template('change_anons.html', chenge_anons=Announcement.query.filter_by(id=id_anons).first(),
                           title='Change anons')

@app.route('/<int:id_anons>/announsement', methods=['GET', 'POST'])
@login_required
def announsement(id_anons):
    try:
        announcement = Announcement.query.filter_by(id=id_anons).first()
        img = ImagesAnnouncement.query.filter_by(id_announcement=id_anons).first()
        if request.method == 'POST':
            answ = request.form.get('answ')
            if answ:
                answer = answer_bal()
                flash(answer)
        logger.info(f'{announsement.__name__} OK')
    except Exception as e:
        logger.error(f'{announsement.__name__} {e}')
        flash('An error occured, please try again')
        return render_template('anonsment.html', announcement=announcement, img=img,  title='Announcement')
    return render_template('anonsment.html', announcement=announcement, img=img,  title='Announcement')

#Admin--------------------------------------------------------------------------------------

@app.route('/admin/', methods=['GET', 'POST'])
def login_admin():
    try:
        if request.method == 'POST':
            login_form = request.form.get('login')
            password_form = request.form.get('password')
            admin = User.query.filter_by(active=True, login=login_form).first()
            if admin:
                if check_password_hash(admin.user_hash, password_form):
                    login_user(admin)
                    return redirect(url_for('admin_user'))
                else:
                    flash('Invalid password')
            else:
                flash('Invalid login')
    except Exception as e:
        logger.error(f'{login_admin.__name__} {e}')
        flash('An error occured, please try again')
        return render_template('admin_login.html', title='Login admin')
    else:
        logger.info(f'{login_admin.__name__} OK')
    return render_template('admin_login.html', title='Login admin')


@app.get('/admin/admin_user')
@login_required
def admin_user():
    try:
        logger.info(f'{admin_user.__name__} OK')
        return render_template('admin.html', users=User.query.filter_by(active=None), title='Admin page')
    except Exception as e:
        logger.error(f'{admin_user.__name__} {e}')
        flash('An error occured, please try again')
        return render_template('admin.html', users=User.query.filter_by(active=None), title='Admin page')


@app.route('/admin/admins')
@login_required
def all_admins():
    try:
        logger.info(f'{all_admins.__name__} OK')
        return render_template('admin.html', users=User.query.filter_by(active=True), title='Admin page')
    except Exception as e:
        logger.error(f'{all_admins.__name__} {e}')
        return render_template('admin.html', users=User.query.filter_by(active=True), title='Admin page')



@app.route('/admin/admin_announcement', methods=['GET', 'POST'])
@login_required
def admin_anons():
    try:
        if request.method == 'POST':
            anons = request.form.get('delete')
            announcement = Announcement.query.filter_by(id=anons).first()
            announcement.del_announcement()
        logger.info(f'{admin_anons.__name__} OK')
    except Exception as e:
        logger.error(f'{admin_anons.__name__} {e}')
        db.session.rollback()
        flash('An error occured, please try again')
    return render_template('admin.html', anons=Announcement.query.all(), title='Admin page')


@app.route('/admin/change_anons/<int:id_user>', methods=['GET', 'POST'])
@login_required
def data_user(id_user):
    try:
        user = User.query.filter_by(id=id_user).first()
        anons = Announcement.query.filter_by(user_id=id_user).all()
        if request.method == 'POST':
            del_user = request.form.get('del')
            change_pass = request.form.get('password')
            del_anons = request.form.get('del_an')
            admin_appoint = request.form.get('admin_appoint')

            if admin_appoint:
                admin = User.query.filter_by(id=id_user).first()
                admin.active = True
                db.session.add(admin)
                db.session.commit()
            if del_user:
                user.del_user()
                for anon in anons:
                    img = ImagesAnnouncement.query.filter_by(id_announcement=anon.id).first()
                    anon.del_announcement()
                    img.del_image()
                return redirect(url_for('admin_user'))
            if change_pass:
                user.change_password(generate_password_hash(change_pass))
            if del_anons:
                an = Announcement.query.filter_by(id=del_anons).first()
                an.del_announcement()
        logger.info(f'{data_user.__name__} OK')
    except Exception as e:
        logger.error(f'{data_user.__name__} {e}')
        flash('An error occured, please try again')
        db.session.rollback()
    return render_template('data_user.html', user=user, anons=anons, title='Admin')


@app.after_request
def redirect_user(response):
    if response.status == '401 UNAUTHORIZED':
        return redirect(f'{url_for("login_user_page")}?next_page={request.url}')
    return response
