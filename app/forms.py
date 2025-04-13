from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length

class MovieForm(FlaskForm):
    title = StringField('Movie Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=10, max=500, message='Description must be between 10 and 500 characters')])
    poster = FileField('Movie Poster', validators=[DataRequired(), FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])