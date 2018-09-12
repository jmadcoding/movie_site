from flask import render_template
from app import app


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
                    ' picks up a series of odd jobs to buy the perfect present for his Aunt Lucys 100th birthday, '
                    'only for the gift to be stolen.'

        },
        {
            'author': {'movie': 'Gone Girl'},
            'body': 'With his wifes disappearance having become the focus of an intense media circus, a man sees '
                    'the spotlight turned on him when its suspected that he may not be innocent.'
        },
        {
            'author': {'movie': 'Dr. Strangelove'},
            'body': 'An insane general triggers a path to nuclear holocaust that a War Room full of politicians and '
                    'generals frantically tries to stop.'
        }
    ]
    return render_template('movie-list.html', title='Movie List', movies=movies)

@app.route('/new-movie')
def newMovie():

    return render_template('new-movie.html', title='New Movie')

@app.route('/movie')
def movie():

    return render_template('movie.html', title='Movie')
