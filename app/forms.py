from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField
from wtforms.validators import DataRequired

class VideoForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    file = FileField('Video File', validators=[DataRequired()])

class CommentForm(FlaskForm):
    body = TextAreaField('Comment', validators=[DataRequired()])
