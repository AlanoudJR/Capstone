import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, abort, jsonify
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
        self.casting_assistant = os.getenv('CASTING_ASSISTANT')
        self.casting_director = os.getenv('CASTING_DIRECTOR')
        self.executive_producer = os.getenv('EXECUTIVE_PRODUCER')
        setup_db(self.app)

        
        self.new_movie= {
            'title': 'Me Before You',
            'release_date': '2020-06-27'
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
############################################################################################
#Testing Get /movies endpoint
    # Get movies 200
    def test_get_movies_casting_assistant(self):
        res = self.client().get('/movies',headers={ "Authorization": "Bearer {}".format(self.casting_assistant)})
        
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # 401 Error unauthorized (invalid token)
    def test_get_movies_casting_assistant_error(self):
        res = self.client().get('/movies',headers={ "Authorization": "Bearer Unauthorized.Token"})
        
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)


    #Testing getting 404 Error 
    def test_get_movies_error(self):
        res = self.client().get('/moviess')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'], False)
############################################################################################
#Testing Get /actors endpoint

    #Testing getting actors 200 casting_assistant
    def test_get_actors_casting_assistant(self):
        res = self.client().get('/actors', headers={ "Authorization": "Bearer {}".format(self.casting_assistant)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertTrue(data['actors'])
        self.assertTrue(data['success'])

    #Testing getting actors 200 casting_director
    def test_get_actors_casting_director(self):
        res = self.client().get('/actors', headers={ "Authorization": "Bearer {}".format(self.casting_director)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertTrue(data['actors'])
        self.assertTrue(data['success'])

    #Testing getting 404 Error 
    def test_get_actors_error(self):
        res = self.client().get('/actorss')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'], False)
    
############################################################################################
    #Test delete /movies/<int:movie_id> endpoint

    #Delete the Movie 200 Status code
    def test_delete_movie_executive_producer(self):
        res = self.client().delete('/movies/2', headers={ "Authorization": "Bearer {}".format(self.executive_producer)})
        data = json.loads(res.data)

        movie = Movie.query.filter(Movie.id == 2).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(movie, None)

    #To Get an Error on deleting a movie 422 Status code
    def test_422_delete_movie_does_not_exist(self):
        res = self.client().delete('/movies/1250', headers={ "Authorization": "Bearer {}".format(self.executive_producer)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    #To Get an Error on deleting a movie 401 Status code (Unauthorized by casting_director)
    def test_delete_movie_casting_director(self):
        res = self.client().delete('/movies/1', headers={ "Authorization": "Bearer {}".format(self.casting_director)})
        data = json.loads(res.data)
    
        movie = Movie.query.filter(Movie.id == 1).one_or_none()

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unauthorized')
############################################################################################
    #Test delete /actors/<int:actors_id> endpoint
        
    #Delete the Actor 200 Status code casting_director
    def test_delete_actor_casting_director(self):
        res = self.client().delete('/actors/4', headers={ "Authorization": "Bearer {}".format(self.casting_director)})
        data = json.loads(res.data)
        actor = Actor.query.filter(Actor.id == 4).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(actor, None)

    #Delete the Actor 200 Status code executive_producer
    def test_delete_actor_executive_producer(self):
        res = self.client().delete('/actors/2', headers={ "Authorization": "Bearer {}".format(self.executive_producer)})
        data = json.loads(res.data)
        actor = Actor.query.filter(Actor.id == 2).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(actor, None)
    
    #To Get an Error on deleting an actor 422 Status code
    def test_422_delete_actor_does_not_exist(self):
        res = self.client().delete('/actors/1250', headers={ "Authorization": "Bearer {}".format(self.casting_director)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
        
############################################################################################

    #Test Post /movies endpoint

    #Create a new movie 200 executive_producer
    def test_create_new_movie_executive_producer(self):
        res = self.client().post('/movies', headers={ "Authorization": "Bearer {}".format(self.executive_producer)}, json=self.new_movie)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created_movie_id'])

    def test_create_new_movie_unauthorized(self):
        res = self.client().post('/movies', json=self.new_movie)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
############################################################################################
    #Test Post /actors endpoint

    #Create a new actor 200 
    def test_create_new_actor(self):
        res = self.client().post('/actors', headers={ "Authorization": "Bearer {}".format(self.casting_director)}, json=self.new_actor)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created_actor_id'])

    #Create a new actor 401
    def test_create_new_actor_unauthorized(self):
        res = self.client().post('/actors', headers={ "Authorization": "Bearer {}".format(self.casting_assistant)}, json=self.new_actor)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
############################################################################################
    #Test Patch /movies endpoint
    
    #Update a movie 200 casting_director
    def test_update_movie_casting_director(self):
        res = self.client().patch('/movies/7', headers={"Authorization": "Bearer {}".format(self.casting_director)}, json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['updated_movie'])

    #Update a movie 200 executive_producer
    def test_update_movie_executive_producer(self):
        res = self.client().patch('/movies/6', headers={"Authorization": "Bearer {}".format(self.executive_producer)}, json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['updated_movie'])

    #Update a movie 400 executive_producer (sending an empty json)
    def test_update_movie_executive_producer_error(self):
        res = self.client().patch('/movies/1', headers={"Authorization": "Bearer {}".format(self.executive_producer)}, json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

############################################################################################
    #Test Patch /actors endpoint

    #Update an actor 200 casting_director

    def test_update_actor_casting_director(self):
        res = self.client().patch('/actors/7', headers={"Authorization": "Bearer {}".format(self.casting_director)}, json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['updated_actor'])

    #Update an actor 200 executive_producer
    def test_update_actor_casting_director(self):
        res = self.client().patch('/actors/6', headers={"Authorization": "Bearer {}".format(self.executive_producer)}, json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['updated_actor'])

    #Update an actor 400 executive_producer (sending an empty json)
    def test_update_movie_executive_producer_error(self):
        res = self.client().patch('/actors/6', headers={"Authorization": "Bearer {}".format(self.executive_producer)}, json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
