from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed

class VideoForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    file = FileField('Video File', validators=[DataRequired(), FileAllowed(['mp4', 'avi', 'mov', 'mkv'], 'Video files only!')])
    submit = SubmitField('Upload')

class CommentForm(FlaskForm):
    body = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Post Comment')
