from flask import request, render_template, flash
from flask_login import login_required, current_user

from todo.models import Announcement
from todo import db
from todo.anons import announcement


@announcement.route('/create_announcement', methods=['GET', 'POST'])
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


@announcement.route('/editing_announcement', methods=['GET', 'POST'])
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


@announcement.route('/<int:id_anons>/change_anons', methods=['GET', 'POST'])
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