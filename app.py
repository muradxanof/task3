from flask import Flask, render_template
from models import db, Movie

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql:///movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()
    if not Movie.query.first():
        populate_db()

def populate_db():
    movies = [
        Movie(title="Inception", released=2010, director="Christopher Nolan", genre="Sci-Fi"),
        Movie(title="The Matrix", released=1999, director="Lana Wachowski, Lilly Wachowski", genre="Sci-Fi"),
        Movie(title="Interstellar", released=2014, director="Christopher Nolan", genre="Sci-Fi"),
        Movie(title="The Godfather", released=1972, director="Francis Ford Coppola", genre="Crime"),
        Movie(title="Pulp Fiction", released=1994, director="Quentin Tarantino", genre="Crime"),
        Movie(title="The Dark Knight", released=2008, director="Christopher Nolan", genre="Action")
    ]
    db.session.bulk_save_objects(movies)
    db.session.commit()

@app.route('/movies/')
def movies():
    all_movies = Movie.query.all()
    return render_template('index.html', movies=all_movies)

@app.route('/movies/<int:movie_id>')
def movie_detail(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    return render_template('movie.html', movie=movie)

if __name__ == '__main__':
    app.run(debug=True)
