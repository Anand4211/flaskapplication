import json
from dotenv import load_dotenv

load_dotenv()

from os import environ
from flask import Flask, Response, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import os

app = Flask(__name__)
app.config.from_pyfile('config.py')

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = 'secreat key'

# Initializing our database
db = SQLAlchemy(app)


class Movie(db.Model):
    # creating a table name

    id = db.Column(db.Integer, primary_key=True)  # this is the primary key
    title = db.Column(db.String(20), unique=True, nullable=False)
    # nullable is false so the column can't be empty
    year = db.Column(db.Integer, nullable=False)
    genre = db.Column(db.String(40), nullable=False)

    def json(self):
        return {
            "id": self.id,
            "title": self.title,
            "year": self.year,
            "genre": self.genre,
        }
        # this method we are defining will convert our output to json


@app.route("/movies", methods=["GET"])
def get_movie():
    """Function to get all the movies in the database"""
    return_value = [Movie.json(movie) for movie in Movie.query.all()]
    return jsonify({"movies": return_value})


# route to get movie by id
@app.route("/movies/<int:id>", methods=["GET"])
def get_movie_by_id(id):
    return_value = Movie.json(Movie.query.filter_by(id=id).first())

    return jsonify(return_value)


# route to add new movie


@app.route("/movies", methods=["POST"])
def add_movie():
    request_data = request.get_json()
    db_response = "Added Successfully"
    try:
        # creating an instance of our Movie constructor
        new_movie = Movie(
            title=request_data["title"],
            year=request_data["year"],
            genre=request_data["genre"],
        )
        db.session.add(new_movie)
        db.session.commit()  # commit changes to session
    except IntegrityError:
        db_response = "This movie title is already present in database"
        db.session.rollback()
    except Exception:
        db_response = "fill value correctly"

    data = {"details": db_response}
    json_data = json.dumps(data)
    return Response(json_data, status=201, content_type="application/json")


@app.route("/movies/<int:id>", methods=["PUT"])
def update_movie(id):
    """Function to edit movie in our database using movie id"""
    request_data = request.get_json()

    movie_to_update = Movie.query.filter_by(id=id).first()
    movie_to_update.title = request_data["title"]
    movie_to_update.year = request_data["year"]
    movie_to_update.genre = request_data["genre"]
    db.session.commit()

    data = {"details": "movie updated"}
    json_data = json.dumps(data)
    return Response(json_data, status=200, content_type="application/json")


# route to delete movie using the DELETE method
@app.route("/movies/<int:id>", methods=["DELETE"])
def remove_movie(id):
    """Function to delete movie from our database"""
    Movie.query.filter_by(id=id).delete()
    db.session.commit()

    data = {"details": "Movie Deleted"}
    json_d = json.dumps(data)
    return Response(json_d, status=203, content_type="application/json")


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True, port=5000)
