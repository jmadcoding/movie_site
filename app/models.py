from app import db

class Director(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    movies = db.relationship('Movie', backref='director', lazy='dynamic')

    def __repr__(self):
        return '<Director {}>'.format(self.name)

class Gross(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total = db.Column(db.Integer, index=True)
    movies = db.relationship('Movie', backref='gross', lazy='dynamic')

    def __repr__(self):
        return '<Gross {}>'.format(self.total)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True)
    genre = db.Column(db.String(64), index=True)
    date = db.Column(db.String(64), index=True)
    synopsis = db.Column(db.String(500), index=True)
    director_id = db.Column(db.Integer, db.ForeignKey('director.id'))
    gross_id = db.Column(db.Integer, db.ForeignKey('gross.id'))

    def __repr__(self):
        return '<Movie {}>'.format(self.title, self.genre, self.date, self.synopsis)

class Stars(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)

    def __repr__(self):
        return '<Stars {}>'.format(self.name)

class MovieToStars(db.Model):
    movieID = db.Column(db.Integer, db.ForeignKey(Movie.id), primary_key=True)
    starsID = db.Column(db.Integer, db.ForeignKey(Stars.id), primary_key=True)
    movie = db.relationship('Movie', backref='stars')
    star = db.relationship('Stars', backref='movies')
