from flask import render_template,request,redirect,url_for,abort
from . import main
from flask_login import login_required,current_user
from ..models import Blog,User
from .forms import BlogForm,UpdateProfile
from ..import db,photos
from ..requests import get_quotes

@main.route('/')
def index():
    title='Fridah`s Blog Website'
    blogs=Blog.query.all()
    random_quotes=get_quotes()

    return render_template('index.html',title = title,quotes=random_quotes, blog=blogs)

@main.route('/blog/new',methods=['GET','POST'])
@login_required
def new_blog():
    form=BlogForm()
    if form.validate_on_submit():
        title = form.title.data
        blog = form.blog.data
        author = form.author.data
        
        new_blog_= Blog(title = title,blog = blog,author = author,user_id=current_user._get_current_object().id)
        new_blog_.save_blog()
        return redirect(url_for('main.index'))

    return render_template('new_blog.html',BlogForm=form)

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))            