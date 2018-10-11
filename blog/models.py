from datetime import datetime
from blog import db,app, login_manager
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Post(db.Model):
    __tablename__ = 'post'   
    id = db.Column('post_id',db.Integer, primary_key=True)
    title = db.Column('title',db.String(100), nullable=False)
    date_posted = db.Column('date_posted',db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column('content',db.Text, nullable=False)
    user_id = db.Column('user_id',db.Integer, db.ForeignKey('user.user_id'), nullable=False)

    def __init__(self,title,content,user_id):
        self.title = title
        self.content = content
        self.user_id = user_id

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column('user_id',db.Integer, primary_key=True)
    username = db.Column('username',db.String(20), unique=True, nullable=False)
    email = db.Column('email',db.String(120), unique=True, nullable=False)
    img = db.Column('image',db.LargeBinary, default=None)
    password = db.Column('password',db.String(60), nullable=False)

    def __init__(self,username,email,password,img=None):
        self.username = username
        self.email = email
        self.password = password
        self.img = img
    posts = db.relationship('Post',backref='author',lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)
        