from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class MovieForm(FlaskForm):
    moviename = StringField('Movie', validators=[DataRequired()])
    releasedate = StringField('Release Date')
    director = StringField('Director')
    gross = StringField('Box Office')
    synopsis = TextAreaField('Synopsis')
    submit = SubmitField('Submit')