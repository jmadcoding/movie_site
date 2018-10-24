from app import db, login
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5

class Director(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    age = db.Column(db.String(64), index=True)
    country = db.Column(db.String(120), index=True)
    movies = db.relationship('Movie', backref='director', lazy='dynamic')

    def __repr__(self):
        return '{}'.format(self.name)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True)
    genre = db.Column(db.String(64), index=True)
    date = db.Column(db.DateTime, index=True)
    synopsis = db.Column(db.String(500), index=True)
    gross = db.Column(db.String(64), index=True)
    director_id = db.Column(db.Integer, db.ForeignKey('director.id'))

    def __repr__(self):
        return '{}'.format(self.title, self.genre, self.date, self.synopsis)

class Star(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    age = db.Column(db.String(64), index=True)
    country = db.Column(db.String(120), index=True)

    def __repr__(self):
        return '{}'.format(self.name)

class MovieToStar(db.Model):
    movieID = db.Column(db.Integer, db.ForeignKey(Movie.id), primary_key=True)
    starID = db.Column(db.Integer, db.ForeignKey(Star.id), primary_key=True)
    movie = db.relationship('Movie', backref='stars')
    star = db.relationship('Star', backref='movies')

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))