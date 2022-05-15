from flask import render_template
from . import main
from flask_login import login_required

@main.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''

    title = 'Fridah`s Blog Website'
    return render_template('index.html',title = title)

@main.route('/blog/new',methods=['GET','POST'])
@login_required
def new_blog():

    return render_template('new_blog.html') 