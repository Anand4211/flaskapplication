import json

import datetime
from flask import Flask, Response, jsonify, request, flash, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy import Column, Integer, DateTime

from sqlalchemy.exc import DatabaseError


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@172.17.0.7/postgres'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'secret string'

# Initializing our database
db = SQLAlchemy(app)


class MissingColumnException:
    pass


def get_all_movies():
    """function to get all movies in our database"""
    return [Movie.json(movie) for movie in Movie.query.all()]


class Movie(db.Model):
    # creating a table name

    id = db.Column(db.Integer, primary_key=True)  # this is the primary key
    title = db.Column(db.String(20), unique=True, nullable=False)
    # nullable is false so the column can't be empty
    year = db.Column(db.INTEGER, nullable=False)
    genre = db.Column(db.String(40), nullable=False)

    def json(self):
        return {'id': self.id, 'title': self.title,
                'year': self.year, 'genre': self.genre}
        # this method we are defining will convert our output to json

    @staticmethod
    def add_movie( _title, _year, _genre):
        """function to add movie to database using _title, _year, _genre
        as parameters"""
        db_response = "Added Successfully"
        try:
            # creating an instance of our Movie constructor
            new_movie = Movie(title=_title, year=_year, genre=_genre)
            db.session.add(new_movie)
            db.session.commit()  # commit changes to session
        except IntegrityError:
            db_response = "This movie title is already present in database"
            db.session.rollback()
        except Exception as e:
            db_res = "fill value correctly"
        except MissingColumnException as e:
            abort(400, 'Excel File Missing Mandatory Column(s):', columns=str(e))
        except DatabaseError:
            db_response = "kindly fill "

        return db_response
    a=10

    def get_movie(_title):
        """function to get movie using the id of the movie as parameter"""
        return [Movie.json(Movie.query.filter_by(title=_title).first())]
        # Movie.json() coverts our output to json
        # the filter_by method filters the query by the id
        # the .first() method displays the first value

    def update_movie(_id, _title, _year, _genre):
        """function to update the details of a movie using the id, title,
        year and genre as parameters"""
        movie_to_update = Movie.query.filter_by(id=_id).first()
        movie_to_update.title = _title
        movie_to_update.year = _year
        movie_to_update.genre = _genre
        db.session.commit()

    def delete_movie(_id):
        """function to delete a movie from our database using
           the id of the movie as a parameter"""
        Movie.query.filter_by(id=_id).delete()
        # filter by id and delete
        db.session.commit()


@app.route('/movies', methods=['GET'])
def get_movies():
    """Function to get all the movies in the database"""
    return jsonify( {'movies': get_all_movies()})


# route to get movie by id
@app.route('/movies/<string:title>', methods=['GET'])
def get_movie_by_id(title):
    return_value = Movie.get_movie(title)
    return jsonify(return_value)


# route to add new movie

@app.route('/movies', methods=['POST'])
def add_movies():
    """Function to add new movie to our database"""
    request_data = request.get_json()  # getting data from client
    respons = Movie.add_movie(request_data["title"], request_data["year"], request_data["genre"])

    data = {
        'details': respons}

    json_data = json.dumps(data)
    return Response(json_data, status=201, content_type='application/json')


@app.route('/movies/<int:id>', methods=['PUT'])
def update_movie(id):
    """Function to edit movie in our database using movie id"""
    request_data = request.get_json()
    Movie.update_movie(id, request_data['title'], request_data['year'], request_data['genre'])

    data = {
        'details': 'movie updated'
    }
    json_data = json.dumps(data)
    return Response(json_data, status=200, content_type='application/json')


# route to delete movie using the DELETE method
@app.route('/movies/<int:id>', methods=['DELETE'])
def remove_movie(id):
    """Function to delete movie from our database"""
    Movie.delete_movie(id)
    data = {"details": "Movie Deleted"}
    json_d = json.dumps(data)
    return Response(json_d, status=203, content_type="application/json")


if __name__ == "__main__":
    db.create_all()
    app.run(port=5000, host='0.0.0.0', debug=True)
