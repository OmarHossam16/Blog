from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
app.config['SECRET_KEY'] = '713222ed02002a635f053d79a36d8ee5'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@localhost/blog'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app) 
login_manager.login_view = 'login'
login_manager.login_message_category = 'info' 

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'YOUR EMAIL'
app.config['MAIL_PASSWORD'] = 'YOUR PASSSWORD'
mail = Mail(app)
from blog import routes
