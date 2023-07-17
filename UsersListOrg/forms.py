from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Email, Length, Regexp, EqualTo, ValidationError
from UsersListOrg.models import User
import re


# from flask_login import current_user
# from flask_wtf.file import FileField, FileAllowed, FileRequired


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    first_name = StringField('First Name',
                             validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last Name',
                            validators=[DataRequired(), Length(min=2, max=20)])
    grade = StringField('Grade')
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[DataRequired()])
    chapter = StringField('Chapter')
    chapter_pres = BooleanField('Chapter President Role')
    org_staff = BooleanField('Organizational Staff Role')
    submit = SubmitField('Add a New Member')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email already exist, please, take another one')

    def validate_phone(self, phone):
        user = User.query.filter_by(phone=phone.data).first()
        if user:
            raise ValidationError('This phone number already exist, please, take another one')
        pattern = r'^(\+)?[0-9]+$'
        is_valid = re.match(pattern, str(phone.data)) is not None
        if not is_valid or (len(phone.data) > 13) or (len(phone.data) < 10):
            raise ValidationError('This phone number is not correct ! '
                                  '(The number can\'t contain any of characters beside +'
                                  ' in the beginning and should be '
                                  'between 10 to 13 numeric characters)')


class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request to reset password')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no profile with this email. First you should sing up.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset password')
