from flask import render_template, flash, redirect
from app import app, db
from app.form import MovieForm
from app.models import Director, Gross, Movie, MovieToStars, Stars


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Justin'}

    return render_template('index.html', title='home', user=user)

@app.route('/movie-list')
def movie_list():

    movies = Movie.query.all()
    return render_template('movie-list.html', title='Movie List', movies=movies)

@app.route('/movie/<title>', methods=['GET', 'POST'])
def movie(title):

    movie = Movie.query.filter_by(title=title).first()
    stars = []
    for m2s in movie.stars:
        stars.append(m2s.star)
    return render_template('movie.html', title='Movie', movie=movie, stars=stars)


@app.route('/new-movie', methods=['GET', 'POST'])
def new_movie():
    form = MovieForm()
    if form.validate_on_submit():
        y = Movie.query.filter_by(title = form.title.data).first()
        if y is not None:
            flash("This movie is already in the database. Submit a different movie!")
            return redirect("new-movie")
        flash('New Movie added: {}'.format(form.title.data))
        new = Movie(title=form.title.data, date=form.releasedate.data, genre=form.genre.data, synopsis=form.synopsis.data)
        """
        new = Movie(title=form.title.data, date=form.releasedate.data, director=form.director.data,
                    genre=form.genre.data, stars=form.stars.data, gross=form.gross.data,
                    synopsis=form.synopsis.data)
        """
        db.session.add(new)
        db.session.commit()
        return redirect('movie-list')
    return render_template('new-movie.html', title='New Movie', form=form)

@app.route('/reset_db')
def reset_db():
    flash("Resetting database: deleting old data and repopulating with dummy data")
    # clear all data from all tables
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print('Clear table {}'.format(table))
        db.session.execute(table.delete())
    db.session.commit()
#DirectorDummyData
    d = Director(name='Paul King')
    db.session.add(d)
    db.session.commit()
    d1 = Director(name='David Fincher')
    db.session.add(d1)
    db.session.commit()
    d2 = Director(name='Stanley Kubrick')
    db.session.add(d2)
    db.session.commit()
    d3 = Director(name='Julie Taymor')
    db.session.add(d3)
    db.session.commit()
    d4 = Director(name='Gareth Evans')
    db.session.add(d4)
    db.session.commit()
 #GrossDummyData
    g = Gross(total=227000000)
    db.session.add(g)
    db.session.commit()
    g1 = Gross(total=369000000)
    db.session.add(g1)
    db.session.commit()
    g2 = Gross(total=9400000)
    db.session.add(g2)
    db.session.commit()
    g3 = Gross(total=29000000)
    db.session.add(g3)
    db.session.commit()
    g4 = Gross(total=9000000)
    db.session.add(g4)
    db.session.commit()
#MovieDummyData
    m = Movie(title='Paddington 2', genre='comedy', date='12 January 2018', synopsis='Paddington, now happily settled '
                    'with the Brown family and a popular member of the local community,'
                    ' picks up a series of odd jobs to buy the perfect present for his Aunt Lucy\'s 100th birthday, '
                    'only for the gift to be stolen.', gross_id=1, director_id=1)
    db.session.add(m)
    db.session.commit()
    m1 = Movie(title='Gone Girl', genre='drama', date='3 October 2014', synopsis='With his wife\'s disappearance having'
                    ' become the focus of an intense media circus, a man sees the spotlight turned on him when its '
                    'suspected that he may not be innocent.', gross_id=2, director_id=2)
    db.session.add(m1)
    db.session.commit()
    m2 = Movie(title='Dr. Strangelove', genre='comedy', date='29 January 1964', synopsis='An insane general triggers a '
                    'path to nuclear holocaust that a War Room full of politicians and generals frantically tries to '
                    'stop.', gross_id=3, director_id=3)
    db.session.add(m2)
    db.session.commit()
    m3 = Movie(title='Across the Universe', genre='musical', date='12 October 2007', synopsis='The music of The Beatles'
                    ' and the Vietnam War form the backdrop for the romance between an upper-class American girl and a '
                    'poor Liverpudlian artist.', gross_id=4, director_id=4)
    db.session.add(m3)
    db.session.commit()
    m4 = Movie(title='The Raid', genre='action', date='13 April 2012', synopsis='A S.W.A.T. team becomes trapped in a '
                    'tenement run by a ruthless mobster and his army of killers and thugs.', gross_id=5, director_id=5)
    db.session.add(m4)
    db.session.commit()
# StarsDummyData
    s = Stars(name='Ben Whishaw')
    db.session.add(s)
    db.session.commit()
    s1 = Stars(name='Sally Hawkins')
    db.session.add(s1)
    db.session.commit()
    s2 = Stars(name='Ben Affleck')
    db.session.add(s2)
    db.session.commit()
    s3 = Stars(name='Rosamund Pike')
    db.session.add(s3)
    db.session.commit()
    s4 = Stars(name='Peter Sellers')
    db.session.add(s4)
    db.session.commit()
    s5 = Stars(name='Jim Sturgess')
    db.session.add(s5)
    db.session.commit()
    s6 = Stars(name='Evan Rachel Wood')
    db.session.add(s6)
    db.session.commit()
    s7 = Stars(name='Iko Uwais')
    db.session.add(s7)
    db.session.commit()
#MovieToStarsDummyData
    ms = MovieToStars(movieID=m.id, starsID=s.id)
    db.session.add(ms)
    db.session.commit()
    ms1 = MovieToStars(movieID=m.id, starsID=s1.id)
    db.session.add(ms1)
    db.session.commit()
    ms2 = MovieToStars(movieID=m1.id, starsID=s2.id)
    db.session.add(ms2)
    db.session.commit()
    ms3 = MovieToStars(movieID=m1.id, starsID=s3.id)
    db.session.add(ms3)
    db.session.commit()
    ms4 = MovieToStars(movieID=m2.id, starsID=s4.id)
    db.session.add(ms4)
    db.session.commit()
    ms5 = MovieToStars(movieID=m3.id, starsID=s5.id)
    db.session.add(ms5)
    db.session.commit()
    ms6 = MovieToStars(movieID=m3.id, starsID=s6.id)
    db.session.add(ms6)
    db.session.commit()
    ms7 = MovieToStars(movieID=m4.id, starsID=s7.id)
    db.session.add(ms7)
    db.session.commit()
    return redirect('index')
