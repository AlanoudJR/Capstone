import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import json

'''
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://alanoudjrayes@localhost:5432/capstone'

migrate = Migrate(app, db)
'''
database_name = "capstone"
database_path = "postgres://{}/{}".format('localhost:5432', database_name)

db = SQLAlchemy()

def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

def db_drop_and_create_all():
    db.drop_all()
    db.create_all()



class Movie(db.Model):

    __tablename__ = 'movie'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime)
    #actors = db.relationship('Actor', backref="movie", lazy=True)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def formatted_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
            #'actors': list(map(lambda actor: actor.format(), self.actors))
        }


class Actor(db.Model):

    __tablename__ = 'actor'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    age = db.Column(db.Integer)
    gender = db.Column(db.String)
   # movie_id = Column(Integer, ForeignKey('movies.id'), nullable=True)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender
        #self.movie_id = movie_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def formatted_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
           # "movie_id": self.movie_id
        }