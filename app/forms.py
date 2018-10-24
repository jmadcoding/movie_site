from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, BooleanField, IntegerField, SelectField, \
                    SelectMultipleField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from wtforms.fields.html5 import DateField
from app.models import User


class MovieForm(FlaskForm):
    title = StringField('Movie', validators=[DataRequired()])
    releasedate = DateField('Release Date', format='%Y-%m-%d')
    director = SelectField('Director', choices=[], coerce=int, validators=[DataRequired()])
    stars = SelectMultipleField('Stars', choices=[], coerce=int, validators=[DataRequired()])
    genre = StringField('Genre', validators=[DataRequired()])
    gross = IntegerField('Total Box Office', validators=[DataRequired()])
    synopsis = TextAreaField('Synopsis', validators=[DataRequired()])
    submit = SubmitField('Submit')

class DirectorForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired()])
    submit = SubmitField('Submit')

class StarForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired()])
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')