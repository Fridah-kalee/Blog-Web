from flask import render_template,request,redirect,url_for,abort
from . import main
from flask_login import login_required,current_user
from ..models import Blog,User,Comment
from .forms import BlogForm,CommentForm,UpdateBlog,UpdateProfile
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

@main.route('/blog,<id>')
@login_required
def blog(id):
    blog = Blog.query.filter_by(id = id).first()

    # comment = Comments.view_comments()
    return render_template('index.html',blog = blog)    

# @main.route('/comment/<int:id>' , methods = ['GET' , 'POST'])
# def comment(id):
#     # blog = Blogs.query.filter_by(id = id).first()
#     form = CommentForm()
    
#     if form.validate_on_submit():
#         comment = form.comment.data

#         new_comment = Comment(comment = comment,user = current_user.username,blog_id = id)
#         new_comment.save_comments()
#         return redirect(url_for('.comment',id = id ))

#     return render_template('comment.html',commentForm = form,comment = comment)
@main.route('/comment/<int:BLOG_id>', methods = ['GET','POST'])
@login_required
def comment(blog_id):
    form = CommentForm()
    blog = Blog.query.get(blog_id)
    all_comments = Comment.query.filter_by(blog_id = blog_id).all()
    if form.validate_on_submit():
        comment = form.comment.data 
        blog_id = blog_id
        user_id = current_user._get_current_object().id
        new_comment = Comment(comment = comment,user_id = user_id,blog_id = blog_id)
        new_comment.save_comment()
        return redirect(url_for('.comment', blog_id = blog_id))
    return render_template('comment.html', form =form, blog = blog,all_comments=all_comments)


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