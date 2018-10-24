from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import MovieForm, RegistrationForm, LoginForm, DirectorForm, StarForm
from app.models import Director, Movie, MovieToStar, Star, User
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from datetime import datetime


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='home')

@app.route('/movie-list')
@login_required
def movie_list():

    movies = Movie.query.all()
    return render_template('movie-list.html', title='Movie List', movies=movies)

@app.route('/movie/<title>', methods=['GET', 'POST'])
@login_required
def movie(title):

    movie = Movie.query.filter_by(title=title).first()
    director = movie.director.name

    stars = []
    for m2s in movie.stars:
        stars.append(m2s.star.name)

    return render_template('movie.html', title='Movie', movie=movie, stars=stars, director=director)

@app.route('/new-movie', methods=['GET', 'POST'])
@login_required
def new_movie():
    form = MovieForm()

    director = Director.query.all()
    stars = Star.query.all()

    form.director.choices = [(d.id, d.name) for d in director]
    form.stars.choices = [(s.id, s.name) for s in stars]
    if form.validate_on_submit():
        y = Movie.query.filter_by(title = form.title.data).first()
        if y is not None:
            flash("This movie is already in the database. Submit a different movie!")
            return redirect("new-movie")
        flash('New Movie added: {}'.format(form.title.data))
        new = Movie(title=form.title.data, date=form.releasedate.data, gross=form.gross.data, genre=form.genre.data,
                    synopsis=form.synopsis.data, director_id=form.director.data)
        db.session.add(new)
        db.session.commit()

        for sid in form.stars.data:
            new_movie_to_stars = MovieToStar(movieID=new.id, starID=sid)
            db.session.add(new_movie_to_stars)

        db.session.commit()
        return redirect('movie-list')
    return render_template('new-movie.html', title='New Movie', form=form, director=director, stars=stars)

@app.route('/new-director', methods=['GET', 'POST'])
@login_required
def new_director():
    form = DirectorForm()
    if form.validate_on_submit():
        y = Director.query.filter_by(name = form.name.data).first()
        if y is not None:
            flash("This director is already in the database. Submit a different director!")
            return redirect("new-director")
        flash('New Director added: {}'.format(form.name.data))
        new = Director(name=form.name.data, age=form.age.data, country=form.country.data)
        db.session.add(new)
        db.session.commit()
        return redirect('new-director')
    return render_template('new-director.html', title='New Director', form=form)

@app.route('/new-star', methods=['GET', 'POST'])
@login_required
def new_star():
    form = StarForm()
    if form.validate_on_submit():
        y = Star.query.filter_by(name = form.name.data).first()
        if y is not None:
            flash("This star is already in the database. Submit a different star!")
            return redirect("new-star")
        flash('New Star added: {}'.format(form.name.data))
        new = Star(name=form.name.data, age=form.age.data, country=form.country.data)
        db.session.add(new)
        db.session.commit()
        return redirect('new-star')
    return render_template('new-star.html', title='New Star', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/reset_db')
@login_required
def reset_db():
    flash("Resetting database: deleting old data and repopulating with dummy data")
    # clear all data from all tables
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print('Clear table {}'.format(table))
        db.session.execute(table.delete())
    db.session.commit()
#UserDummyData
    u = User(username='Justin', email='jtmhms@gmail.com')
    u.set_password('dog')
    db.session.add(u)
    db.session.commit()
#DirectorDummyData
    d = Director(name='Paul King', age='40', country='United Kingdom')
    db.session.add(d)
    db.session.commit()
    d1 = Director(name='David Fincher', age='56', country='United States')
    db.session.add(d1)
    db.session.commit()
    d2 = Director(name='Stanley Kubrick', age='70', country='United States')
    db.session.add(d2)
    db.session.commit()
    d3 = Director(name='Julie Taymor', age='65', country='United States')
    db.session.add(d3)
    db.session.commit()
    d4 = Director(name='Gareth Evans', age='38', country='United Kingdom')
    db.session.add(d4)
    db.session.commit()
#MovieDummyData
    m = Movie(title='Paddington 2', genre='comedy', date=datetime(2018, 1, 12), synopsis='Paddington, now happily '
                    'settled with the Brown family and a popular member of the local community,'
                    ' picks up a series of odd jobs to buy the perfect present for his Aunt Lucy\'s 100th birthday, '
                    'only for the gift to be stolen.', gross='227000000', director_id=1)
    db.session.add(m)
    db.session.commit()
    m1 = Movie(title='Gone Girl', genre='drama', date=datetime(2014, 10, 3), synopsis='With his wife\'s '
                    'disappearance having become the focus of an intense media circus, a man sees the spotlight turned '
                    'on him when its suspected that he may not be innocent.', gross='369000000', director_id=2)
    db.session.add(m1)
    db.session.commit()
    m2 = Movie(title='Dr. Strangelove', genre='comedy', date=datetime(1964, 1, 29), synopsis='An insane general '
                    'triggers a path to nuclear holocaust that a War Room full of politicians and generals frantically '
                    'tries to stop.', gross='9400000', director_id=3)
    db.session.add(m2)
    db.session.commit()
    m3 = Movie(title='Across the Universe', genre='musical', date=datetime(2007, 10, 12), synopsis='The music of '
                    'The Beatles and the Vietnam War form the backdrop for the romance between an upper-class American '
                    'girl and a poor Liverpudlian artist.', gross='29000000', director_id=4)
    db.session.add(m3)
    db.session.commit()
    m4 = Movie(title='The Raid', genre='action', date=datetime(2012, 4, 13), synopsis='A S.W.A.T. team becomes '
                    'trapped in a tenement run by a ruthless mobster and his army of killers and thugs.',
                    gross='9000000', director_id=5)
    db.session.add(m4)
    db.session.commit()
# StarsDummyData
    s = Star(name='Ben Whishaw', age='38', country='United Kingdom')
    db.session.add(s)
    db.session.commit()
    s1 = Star(name='Sally Hawkins', age='42', country='United Kingdom')
    db.session.add(s1)
    db.session.commit()
    s2 = Star(name='Ben Affleck', age='46', country='United States')
    db.session.add(s2)
    db.session.commit()
    s3 = Star(name='Rosamund Pike', age='39', country='United Kingdom')
    db.session.add(s3)
    db.session.commit()
    s4 = Star(name='Peter Sellers', age='54', country='United Kingdom')
    db.session.add(s4)
    db.session.commit()
    s5 = Star(name='Jim Sturgess', age='40', country='United Kingdom')
    db.session.add(s5)
    db.session.commit()
    s6 = Star(name='Evan Rachel Wood', age='31', country='United States')
    db.session.add(s6)
    db.session.commit()
    s7 = Star(name='Iko Uwais', age='35', country='Indonesia')
    db.session.add(s7)
    db.session.commit()
#MovieToStarsDummyData
    ms = MovieToStar(movieID=m.id, starID=s.id)
    db.session.add(ms)
    db.session.commit()
    ms1 = MovieToStar(movieID=m.id, starID=s1.id)
    db.session.add(ms1)
    db.session.commit()
    ms2 = MovieToStar(movieID=m1.id, starID=s2.id)
    db.session.add(ms2)
    db.session.commit()
    ms3 = MovieToStar(movieID=m1.id, starID=s3.id)
    db.session.add(ms3)
    db.session.commit()
    ms4 = MovieToStar(movieID=m2.id, starID=s4.id)
    db.session.add(ms4)
    db.session.commit()
    ms5 = MovieToStar(movieID=m3.id, starID=s5.id)
    db.session.add(ms5)
    db.session.commit()
    ms6 = MovieToStar(movieID=m3.id, starID=s6.id)
    db.session.add(ms6)
    db.session.commit()
    ms7 = MovieToStar(movieID=m4.id, starID=s7.id)
    db.session.add(ms7)
    db.session.commit()
    return redirect('index')
