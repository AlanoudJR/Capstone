import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie


class CapstoneTestCase(unittest.TestCase):
    """This class represents the capstone test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        
        self.new_movie= {
            'title': 'Me Before You',
            'release_date': '2020-06-27',
        }
        self.new_actor= {
            'name': 'Sarah',
            'age': 22,
            'gender': 'Female'
        }
        

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

############################################## 

    #Testing getting movies 200
    def test_get_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertTrue(data['movies'])
        self.assertTrue(data['success'])

    #Testing getting actors 200
    def test_get_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertTrue(data['actors'])
        self.assertTrue(data['success'])

##############################################

    #Delete the Movie 200 Status code (deleting an exsiting movie)    
    def test_delete_movie(self):
        res = self.client().delete('/movies/12')
        data = json.loads(res.data)

        movie = Movie.query.filter(Movie.id == 12).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(movie, None)

    #To Get an Error on deleting a movie 422 Status code
    def test_422_delete_movie_does_not_exist(self):
        res = self.client().delete('/movies/1250')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
        
    #Delete the Actor 200 Status code (deleting an exsiting movie)    
    def test_delete_actor(self):
        res = self.client().delete('/actors/4')
        data = json.loads(res.data)

        actor = Actor.query.filter(Actor.id == 12).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(actor, None)

    
    #To Get an Error on deleting an actor 422 Status code
    def test_422_delete_actor_does_not_exist(self):
        res = self.client().delete('/actors/1250')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
        
##############################################

    #Create a new movie 200 
    def test_create_new_movie(self):
        res = self.client().post('/movies', json=self.new_movie)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created_movie_id'])

    #Create a new actor 200 
    def test_create_new_actor(self):
        res = self.client().post('/actors', json=self.new_actor)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created_actor_id'])

##############################################        
 

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
