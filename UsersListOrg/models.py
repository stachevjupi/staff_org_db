from UsersListOrg import db, app
from flask_login import UserMixin
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    grade = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    chapter = db.Column(db.String(40))
    chapter_pres = db.Column(db.Integer, nullable=True, default=0)
    org_staff = db.Column(db.Integer, nullable=True, default=0)
