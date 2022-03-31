from flask import Flask, render_template, Response,jsonify,request, flash
from flask_sqlalchemy import SQLAlchemy


import json
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://sql:anand4211@localhost/flasksql'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'secret string'

db = SQLAlchemy(app)


class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pname = db.Column(db.String(80), unique=True, nullable=False)
    color = db.Column(db.String(120), nullable=False)

    def __init__(self, pname, color):
        self.pname = pname
        self.color = color
    def json(self):
        return {'id': self.id, 'pname': self.pname,
                'color': self.year}
@app.route('/')
def home():
    return '<a href="/addperson"><button> Click here </button></a>'


@app.route("/addperson")
def addperson():
    return render_template("index.html")


@app.route("/personadd", methods=['POST'])
def personadd():
    pname = request.form["pname"]
    color = request.form["color"]
    entry = People(pname, color)
    db.session.add(entry)
    db.session.commit()

    return render_template("index.html")
@app.route('/get', methods=['GET'])
def datafetch():
     a=People.query.all()
     return (render_template('home.html', sock=a))














if __name__ == '__main__':
    db.create_all()
    app.run(port=7700)
