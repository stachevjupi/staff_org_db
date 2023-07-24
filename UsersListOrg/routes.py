from UsersListOrg import app, bcrypt, db, mail
from flask import render_template, request, redirect, url_for, flash, abort
from UsersListOrg.models import User
from UsersListOrg.forms import LoginForm, RegistrationForm, ResetPasswordForm, RequestResetForm
from flask_login import login_user, logout_user, login_required, current_user
import random
import string
from flask_mail import Message


@app.route("/", methods=(['POST', 'GET']))
def login():
    if current_user.is_authenticated and current_user.org_staff == 1:
        return redirect(url_for('rosters'))
    elif current_user.is_authenticated:
        return redirect(url_for('chptr'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, form.remember.data)
            next_page = request.args.get('next')
            if current_user.is_authenticated and current_user.org_staff == 1:
                return redirect(next_page) if next_page else redirect(url_for('rosters'))
            elif current_user.is_authenticated:
                return redirect(next_page) if next_page else redirect(url_for('chptr'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


def generate_random_password(length=10):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password


def send_reset_standard_email(user, password):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''You can leave your automatically given password: {password}
    To reset your password, visit the following link:
    
{url_for('reset_token', token=token, _external=True)}

If you or your employer did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:

{url_for('reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


@app.route("/register", methods=['GET', 'POST'])
@login_required
def register():
    # password = generate_random_password()
    # hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
    # print(password)
    # new_user = User(
    #     first_name="first_name",
    #     last_name="last_name",
    #     grade="grade",
    #     email="email@gmail.com",
    #     phone="+7894563214",
    #     password=hashed_pw,
    #     chapter="Not Specified",
    #     chapter_pres= 0,
    #     org_staff= 1,
    # )
    # db.session.add(new_user)
    # db.session.commit()
    users = User.query.all()
    chapters = []
    grades = []
    unique_chapters = []
    unique_grades = []
    for member in users:
        grades.append(member.grade)
        if member.chapter is not None:
            chapters.append(member.chapter)
        unique_grades = list(set(grades))
        unique_chapters = list(set(chapters))
    form = RegistrationForm()
    if form.validate_on_submit():
        password = generate_random_password()
        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        chapter_pres = 1 if form.chapter_pres.data else 0
        org_staff = 1 if form.org_staff.data else 0
        grade_sel = request.form.get('selectedGrade')
        if form.grade.data:
            grade = form.grade.data
        elif grade_sel:
            grade = grade_sel
        else:
            grade = "Not Specified"
        chapter_sel = request.form.get('selectedChapter')
        if form.chapter.data:
            chapter = form.chapter.data
        elif chapter_sel:
            chapter = chapter_sel
        elif current_user.chapter_pres == 1:
            chapter = current_user.chapter
        else:
            chapter = "Not Specified"
        user = User(first_name=form.first_name.data, last_name=form.last_name.data, grade=grade,
                    email=form.email.data, phone=form.phone.data, password=hashed_pw, chapter=chapter,
                    chapter_pres=chapter_pres, org_staff=org_staff)
        db.session.add(user)
        db.session.commit()
        flash('An email has been sent with instructions to reset new members password.', 'info')
        flash('Your new member created ! (Successfully added to the roster)', 'success')
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_standard_email(user, password)
        print(password)
        return redirect(url_for('login'))
    return render_template('register.html', title='Registration', form=form, chapters=unique_chapters,
                           grades=unique_grades, legend='Add a New Member')


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in.', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('rosters'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route("/rosters")
@login_required
def rosters():
    users = User.query.all()
    if current_user.org_staff == 1:
        return render_template('rosters.html', title='Rosters', users=users)


@app.route("/org_staff")
@login_required
def org_staff():
    users = User.query.filter_by(org_staff=1).all()
    if current_user.org_staff == 1:
        return render_template('roster_org.html', title='Organizational staff', users=users)


@app.route("/chapters")
@login_required
def chapters():
    unique_chapters = User.query.with_entities(User.chapter).distinct().all()
    if current_user.org_staff == 1:
        return render_template('chapters.html', title='Chapters', unique_chapters=unique_chapters)


@app.route("/chapters/<string:chapt>")
@login_required
def chapter(chapt):
    users = User.query.filter_by(chapter=chapt).all()
    return render_template('roster_chapt.html', users=users, chapt=chapt)


@app.route("/rosters/chapter")
@login_required
def chptr():
    users = User.query.filter_by(chapter=current_user.chapter).all()
    return render_template('rosters.html', users=users)


@app.route("/arrange/<string:variable>")
@login_required
def arrange(variable):
    print(variable)
    users = User.query.order_by(variable).all()
    if current_user.is_authenticated and current_user.org_staff == 1:
        return render_template('rosters.html', title='Rosters', users=users)
    elif current_user.is_authenticated and current_user.org_staff == 0:
        users = [user for user in users if user.chapter == current_user.chapter]
        return render_template('rosters.html', title='Rosters', users=users)


@app.route("/arrange_org/<string:variable>")
@login_required
def arrange_org(variable):
    users = User.query.order_by(variable).all()
    if current_user.is_authenticated and current_user.org_staff == 1:
        users = [user for user in users if user.org_staff == 1]
        return render_template('roster_org.html', title='Rosters', users=users)


@app.route("/<string:variable1>/<string:variable2>")
@login_required
def arrange_chapt(variable1, variable2):
    users = User.query.order_by(variable2).all()
    if current_user.is_authenticated and current_user.org_staff == 1:
        users = [user for user in users if user.chapter == variable1]
        return render_template('roster_chapt.html', title='Rosters', users=users, chapt=variable1)


@app.route("/roster/<int:user_id>/update", methods=['GET', 'POST'])
@login_required
def update_member(user_id):
    user = User.query.get_or_404(user_id)
    if current_user.id != user_id and (current_user.chapter == user.chapter and current_user.chapter_pres == 0) \
            and current_user.org_staff == 0:
        abort(403)
    users = User.query.all()
    chapters = []
    grades = []
    unique_chapters = []
    unique_grades = []
    for member in users:
        grades.append(member.grade)
        if member.chapter is not None:
            chapters.append(member.chapter)
        unique_grades = list(set(grades))
        unique_chapters = list(set(chapters))
    password = user.password
    grade_org = user.grade
    chapter_org = user.chapter
    chapter_pres_us = user.chapter_pres
    org_staff_us = user.org_staff
    db.session.delete(user)
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.chapter_pres.data:
            chapter_pres = 1
        elif chapter_pres_us == 1 and org_staff_us == 0 and current_user.org_staff == 0:
            chapter_pres = chapter_pres_us
        elif not form.chapter_pres.data:
            chapter_pres = 0
        if form.org_staff.data:
            org_staff = 1
        elif not form.org_staff.data:
            org_staff = 0
        grade_sel = request.form.get('selectedGrade')
        if form.grade.data:
            grade = form.grade.data
        elif grade_sel:
            grade = grade_sel
        elif grade_org:
            grade = grade_org
        else:
            grade = "Not Specified"
        chapter_sel = request.form.get('selectedChapter')
        if form.chapter.data:
            chapter = form.chapter.data
        elif chapter_sel:
            chapter = chapter_sel
        elif current_user.chapter_pres == 1:
            chapter = current_user.chapter
        elif chapter_org:
            chapter = chapter_org
        else:
            chapter = "Not Specified"
        user_updated = User(first_name=form.first_name.data, last_name=form.last_name.data, grade=grade,
                            email=form.email.data, phone=form.phone.data, password=password, chapter=chapter,
                            chapter_pres=chapter_pres, org_staff=org_staff)
        db.session.add(user_updated)
        db.session.commit()
        flash('Your member data has been updated!', 'success')
        if current_user.org_staff == 1:
            return redirect(url_for('rosters'))
        else:
            return redirect(url_for('chptr'))
    elif request.method == 'GET':
        form.first_name.data = user.first_name
        form.last_name.data = user.last_name
        form.grade.data = user.grade
        form.email.data = user.email
        form.phone.data = user.phone
        form.chapter.data = user.chapter
        form.chapter_pres.data = user.chapter_pres
        form.org_staff.data = user.org_staff
    return render_template('register.html', title='Update Post', form=form, legend='Update Member Data',
                           chapters=unique_chapters,
                           grades=unique_grades)


@app.route("/roster/<int:user_id>/delete", methods=['GET'])
@login_required
def delete_member(user_id):
    user = User.query.get_or_404(user_id)
    org_count = User.query.filter_by(org_staff=1).count()
    total_items = db.session.query(User).count()
    print(org_count)
    print(total_items)
    if current_user.id != user_id and (current_user.chapter == user.chapter and current_user.chapter_pres == 0)\
            and current_user.org_staff == 0:
        abort(403)
    elif current_user.org_staff == 0 and user.org_staff == 1:
        abort(403)
    elif org_count <= 1 and user.org_staff == 1:
        return render_template('last_org_staff.html', title='Error', username=current_user.first_name)
    else:
        db.session.delete(user)
        db.session.commit()
    flash('Your membership has been deleted!', 'success')
    if current_user.org_staff == 1:
        return redirect(url_for('rosters'))
    else:
        return redirect(url_for('chptr'))


@app.errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(403)
def error_403(error):
    return render_template('errors/403.html'), 403


@app.errorhandler(500)
def error_500(error):
    return render_template('errors/500.html'), 500
