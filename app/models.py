from .import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index = True)
    blogs = db.relationship('Blog',backref='user',lazy='dynamic')
    pass_secure =db.Column(db.String(255))
    email=db.Column(db.String,unique=True)
    bio=db.Column(db.String(255))
    profile_pic_path=db.Column(db.String())

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    
    def __repr__(self):
        return f'User {self.username}'

class Blog(db.Model):
    __tablename__ = 'blogs'
    id = db.Column(db.Integer,primary_key = True)
    title=db.Column(db.String(255))
    blog = db.Column(db.String)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))

    def __repr__(self):
        return f'Blog {self.blog}'