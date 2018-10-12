from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired


class MovieForm(FlaskForm):
    title = StringField('Movie', validators=[DataRequired()])
    releasedate = StringField('Release Date')
    director = StringField('Director')
    genre = StringField('Genre')
    stars = StringField('Lead Actor/Actress')
    gross = StringField('Total Box Office')
    synopsis = TextAreaField('Synopsis')
    submit = SubmitField('Submit')