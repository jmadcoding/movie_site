from flask import render_template, flash, redirect
from app import app
from app.form import MovieForm


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Justin'}

    return render_template('index.html', title='home', user=user)

@app.route('/movie-list')
def movieList():
    movies = [
        {
            'author': {'movie': 'Paddington 2'},
            'body': 'Paddington, now happily settled with the Brown family and a popular member of the local community,'
                    ' picks up a series of odd jobs to buy the perfect present for his Aunt Lucy\'s 100th birthday, '
                    'only for the gift to be stolen.'

        },
        {
            'author': {'movie': 'Gone Girl'},
            'body': 'With his wife\'s disappearance having become the focus of an intense media circus, a man sees '
                    'the spotlight turned on him when its suspected that he may not be innocent.'
        },
        {
            'author': {'movie': 'Dr. Strangelove'},
            'body': 'An insane general triggers a path to nuclear holocaust that a War Room full of politicians and '
                    'generals frantically tries to stop.'
        }
    ]
    return render_template('movie-list.html', title='Movie List', movies=movies)

@app.route('/movie')
def movie():
    info = {'Movie': 'Paddington 2'}
    info['ReleaseDate'] = 'November 10, 2017'
    info['Director'] = 'Paul King'
    info['Synopsis'] = 'Paddington, now happily settled with the Brown family and a popular member of the local ' \
                      'community, picks up a series of odd jobs to buy the perfect present for his Aunt Lucy\'s 100th ' \
                      'birthday, only for the gift to be stolen.'
    info['Gross'] = '$200,000,000'
    return render_template('movie.html', title='Movie', info=info)


@app.route('/new-movie', methods=['GET', 'POST'])
def newMovie():
    form = MovieForm()
    if form.validate_on_submit():
        flash('New Movie added: {}'.format(form.moviename.data))
        info = {'Movie': form.moviename.data}
        info['ReleaseDate'] = form.releasedate.data
        info['Director'] = form.director.data
        info['Synopsis'] = form.synopsis.data
        info['Gross'] = form.gross.data
        return render_template('movie.html', title='Movie Page', info=info)
    return render_template('new-movie.html', title='New Movie', form=form)