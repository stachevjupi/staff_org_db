import flask_migrate
import flask_sqlalchemy
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13mbjhv887vge280ba245'

db_info = {'host': 'localhost',
           'database': 'UsersListOrg',
           'psw': 'Lena091165',
           'user': 'postgres',
           'port': '5432'}

app.config[
    'SQLALCHEMY_DATABASE_URI'] = f"postgresql://{db_info['user']}:{db_info['psw']}@{db_info['host']}/{db_info['database']}"

db = flask_sqlalchemy.SQLAlchemy(app)
migrate = flask_migrate.Migrate(app, db)

os.environ["EMAIL_USER"] = "staff.org@gmail.com"
os.environ["EMAIL_PASS"] = "tQc3RFfmhz4pCw0N"

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'danger'
app.config['MAIL_SERVER'] = 'smtp-relay.sendinblue.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
mail = Mail(app)

from UsersListOrg import routes, models
