from flask import render_template,request,redirect,url_for,abort
from . import main
from flask_login import login_required,current_user
from ..models import Blog,User,Comment
from .forms import BlogForm,CommentForm,UpdateProfile
from ..import db,photos
from ..requests import get_quotes
import datetime

@main.route('/')
def index():
    title='Fridah`s Blog Website'
    blog=Blog.query.all()
    random_quotes=get_quotes()

    return render_template('index.html',title = title,quotes=random_quotes, blog=blog)

@main.route('/blog/<int:blog_id>',methods=['GET'])
@login_required
def blog(blog_id):
    blog = Blog.query.get(blog_id)
    form=CommentForm()

    
    return render_template('blog.html',blog = blog,form=form)

@main.route('/blog/new',methods=['GET','POST'])
@login_required
def new_blog():
    form=BlogForm()
    if form.validate_on_submit():
        title = form.title.data
        blog = form.blog.data
        
        user_id=current_user
        
        new_blog= Blog(title = title,blog = blog,user_id=current_user._get_current_object().id)
        new_blog.save_blog()
        return redirect(url_for('main.index'))

    return render_template('new_blog.html',form=form)    


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

@main.route('/comment/<int:blog_id>', methods = ['POST','GET'])
@login_required
def comment(blog_id):
  comments = Comment.query.filter_by(blog_id=blog_id).all()
  form = CommentForm()
  if form.validate_on_submit():
    comment = form.comment.data

    new_comment_object= Comment(comment=comment, blog_id=blog_id, user_id = current_user._get_current_object().id)

    new_comment_object.save_comment()
    return redirect(url_for('main.comment', blog_id=blog_id))

  return render_template('comment.html', form=form, comments=comments)

@main.route('/<blog_id>/',methods=['GET','DELETE'])
@login_required
def delete_blog(blog_id):
    deleteBlog = Blog.query.filter_by(id=blog_id).first()
    if deleteBlog:
        db.session.delete(deleteBlog)
        db.session.commit()
        return redirect(url_for('main.index'))
    else:
        pass
    return redirect(url_for('main.index'))

    
@main.route('/blog/edit/<int:id>',methods = ['GET','POST'])
@login_required
def edit_blogs(id):
    if not current_user:
        abort(404)

    updateBlog= Blog.query.get(id)

    form = BlogForm()

    if form.validate_on_submit():
        updateBlog.title = form.title.data
        updateBlog.blog = form.blog.data

        db.session.add(updateBlog)
        db.session.commit()

        return redirect(url_for('main.index',id=updateBlog.id))
    

    return render_template('new_blog.html',form = form,action='Edit')              