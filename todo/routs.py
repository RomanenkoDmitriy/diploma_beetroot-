from os.path import join, dirname, realpath

import flask_login
# from flask_security import SQLAlchemyUserDatastore, login_required, Security
from flask import request, render_template, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_login import login_user, login_required, logout_user, current_user
# from  flask_admin import helpers

from todo import app, db, logger
from todo.models import User, Announcement, ImagesAnnouncement
from todo.utils.utils import avatar_img, answer_bal


# user_datastore = SQLAlchemyUserDatastore(db,  User,  RoleUser)
# security = Security(app, user_datastore)


# @security.context_processor
# def security_context_processor():
#     return dict(
#         admin_base_template=admin.base_template,
#         admin_view=admin.index_view,
#         h=helpers,
#         get_url=url_for
#     )


@app.route('/')
def index_page():
    app.logger.warning('info')
    if Announcement.query.all():
        try:
            image = ImagesAnnouncement.query.all()
            return render_template('index.html',
                                   announcement=Announcement.query.order_by(Announcement.date.desc()).all(),
                                   img=image)
        except Exception as e:
            logger.error(str(e))
        # return render_template('index.html', announcement=Announcement.query.order_by(Announcement.date.desc()).all(),
        #                        img=image)
    # logger.debug('info')
    return render_template('index.html')


@app.route('/<string:chapter>')
def announcement_chapter(chapter):
    logger.info('info')
    announcement = Announcement.query.filter_by(chapter=chapter).all()
    return render_template('index.html', announcement=announcement)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        password1 = request.form['password1']
        email = request.form['email']
        user_hash = generate_password_hash(password)
        if password == password1:
            # user_datastore.create_user(login=login, user_hash=user_hash, email=email)
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


@app.route('/login_user', methods=['GET', 'POST'])
def login_user_page():
    login_form = request.form.get('login')
    password_form = request.form.get('password')

    if login_form and password_form:
        # path = os.path.join(os.getcwd(), 'password_admin.txt')
        # with open(path, 'r') as file:
        #     file_list = list(file)
        #     login_adm = file_list[0]
        #     password_adm = file_list[1]

        user_new = User.query.filter_by(login=login_form).first()
        if user_new is not None:

            if check_password_hash(user_new.user_hash, password_form):
                login_user(user_new)
                # if request.args.get('next'):
                    # redirect_page = request.args.get('next')
                    # return redirect(url_for(redirect_page))
                return redirect(url_for('index_page'))
            else:
                flash('Password is incorrect')
        else:
            flash('Invalid login')
    else:
        flash('Enter login and password')

    return render_template('login.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def user_logout():
    logout_user()
    return redirect(url_for('index_page'))


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
        try:
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
                path = join(dirname(realpath(__file__)), 'static', secure_filename(file.filename))
                avatar_img(file, path)
                # file.save(path)
                user.add_avatar(file.filename)
        except Exception as e:
            db.session.rollback()

    return render_template('personal_area.html')


@app.route('/create_announcement', methods=['GET', 'POST'])
@login_required
def create_announcement():
    title = request.form.get('title')
    text = request.form.get('text')
    file = request.files.get('foto')
    chapter = request.form.get('chapter')

    if request.method == 'POST':
        new_announcement = Announcement(title=title, text=text, chapter=chapter, user_id=current_user.id)
        try:
            db.session.add(new_announcement)
            db.session.commit()
            if file is not None:
                path = join(dirname(realpath(__file__)), 'static', secure_filename(file.filename))
                images = ImagesAnnouncement(path_img=file.filename, id_announcement=new_announcement.id)
                db.session.add(images)
                db.session.commit()
                avatar_img(file, path)
            # db.session.commit()
            flash('Announcement created')
            return render_template('add_announcement.html', anonc=current_user.announcement_table,
                                   img=new_announcement.images_announcements)
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


@app.route('/<int:id_anons>/change_anons', methods=['GET', 'POST'])
@login_required
def change_anons(id_anons):
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

    return render_template('change_anons.html', chenge_anons=Announcement.query.filter_by(id=id_anons).first())


@app.route('/<int:id_anons>/announsement', methods=['GET', 'POST'])
@login_required
def announsement(id_anons):
    announcement = Announcement.query.filter_by(id=id_anons).first()
    img = ImagesAnnouncement.query.filter_by(id=announcement.id).first()
    if request.method == 'POST':
        answ = request.form.get('answ')
        if answ:
            answer = answer_bal()
            flash(answer)
    return render_template('anonsment.html', announcement=announcement, img=img)


@app.route('/admin/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_form = request.form.get('login')
        password_form = request.form.get('password')
        admin = User.query.filter_by(active=True, login=login_form).first()
        if admin:
            if check_password_hash(admin.user_hash, password_form):
                return redirect(url_for('admin_page'))
            else:
                flash('Invalid password')
        else:
            flash('Invalid login')
    return render_template('admin_login.html')


@app.get('/admin/admin_page')
def admin_page():
    return render_template('admin.html', users=User.query.all())

@app.route('/admin/change_anons/<int:id_user>', methods=['GET', 'POST'])
def data_user(id_user):
    user = User.query.filter_by(id=id_user).first()
    anons = Announcement.query.filter_by(user_id=id_user).all()
    if request.method == 'POST':
        del_user = request.form.get('del')
        change_pass = request.form.get('password')
        del_anons = request.form.get('del_an')
        flash(str(del_anons))
        try:
            if del_user:
                user.del_user()
                for anon in anons:
                    anon.del_announcement()
            if change_pass:
                user.change_password(generate_password_hash(change_pass))
            if del_anons:
                an = Announcement.query.filter_by(id=del_anons).first()
                an.del_announcement()
            # return render_template('data_user.html', user=user, anons=anons)
        except Exception as e:
            flash(str(e))
            db.session.rollback()
    return render_template('data_user.html', user=user, anons=anons)



# @app.after_request
# @login_required
# def redirect_page(response):
#     if response.status.code == 401:
#         return redirect(f'{url_for("login_user_page")}?next={request.url}')
#     return response

