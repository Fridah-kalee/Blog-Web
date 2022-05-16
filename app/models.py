from .import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime

class Quotes:
    def __init__(self,id,quote,author):
        self.id=id
        self.quote=quote
        self.author=author


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
    author=db.Column(db.String)
    posted = db.Column(db.DateTime,default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    comment = db.relationship('Comment',backref = 'blog',lazy = "dynamic")

    def save_blog(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_user_blogs(cls,user):
        user_blogs = Blog.query.filter_by(user = user).all()
        return user_blogs

    @classmethod
    def viewblogs(cls):
        blogs = Blog.query.all()
        return blogs

    def delete_blog(self):
        db.session.delete(self)
        db.session.commit()
    

    def __repr__(self):
        return f'Blog {self.blog}'

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text(),nullable = False)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable = False)
    blog_id = db.Column(db.Integer,db.ForeignKey('blogs.id'),nullable = False)

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    def delete_comment(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def view_comments(cls,blog_id):
        comments = Comments.query.filter_by(blog_id = blog_id).all()
        return comments


    def __repr__(self):
        return f'comment:{self.comment}'        

    

    
        