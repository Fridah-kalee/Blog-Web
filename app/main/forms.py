from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SelectField,SubmitField
from wtforms.validators import InputRequired

class BlogForm(FlaskForm):

    title = StringField('Blog title',validators=[InputRequired()])
    blog = TextAreaField('Blog content', validators=[InputRequired()])
    author=StringField('Author',validators=[InputRequired()])
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    comment = TextAreaField('Your comment' ,validators= [InputRequired()])
    submit = SubmitField('Submit')

class UpdateBlog(FlaskForm):
    title = StringField('Enter title',validators=[InputRequired()])
    blog = TextAreaField('Edit your blog',validators = [InputRequired()])
    submit = SubmitField('Submit')        

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [InputRequired()])
    submit = SubmitField('Submit')