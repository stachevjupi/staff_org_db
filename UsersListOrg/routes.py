from UsersListOrg import app, bcrypt, db, mail
from flask import render_template, request, redirect, url_for, flash
from UsersListOrg.models import User
from UsersListOrg.forms import LoginForm, RegistrationForm, ResetPasswordForm, RequestResetForm
from flask_login import login_user, logout_user, login_required, current_user
import random
import string
from flask_mail import Message


@app.route("/", methods=(['POST', 'GET']))
def login():
    if current_user.is_authenticated:
        return redirect(url_for('rosters'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('register'))
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
    # if current_user.is_authenticated:
    #     return redirect(url_for('posts'))
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
        return redirect(url_for('login'))
    return render_template('register.html', title='Registration', form=form, chapters=unique_chapters,
                           grades=unique_grades)


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
        return render_template('org_staff.html', title='Organizational staff', users=users)


@app.route("/chapters")
@login_required
def chapters():
    unique_chapters = User.query.with_entities(User.chapter).distinct().all()
    if current_user.org_staff == 1:
        return render_template('chapters.html', title='Chapters', unique_chapters=unique_chapters)


@app.route("/chapters/<string:chapt>")
@login_required
def chapter(chapt):
    print(chapt)
    users = User.query.filter_by(chapter=chapt).first_or_404()
    print(users)
    return render_template('rosters.html', users=users)
