import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from models import Movie, Actor, setup_db, db_drop_and_create_all
from auth.auth import AuthError, requires_auth
import json

app = Flask(__name__)
setup_db(app)
CORS(app)
db = SQLAlchemy(app)
'''
SQLALCHEMY_DATABASE_URI = 'postgres://alanoudjrayes@localhost:5432/capstone'
migrate = Migrate(app, db)
'''

#db_drop_and_create_all()

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)

  CORS(app, resources={'/': {'origins': '*'}})

  return app

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    return response

@app.route('/test')
def index():
    return jsonify({
        "success": True,
        "message": "Hello, World!"
    })

###################### Get/View ######################

'''
curl -d '{"name":"Sarah","age":"20"}' -H "Content-Type: application/json" -X POST http://localhost:5000/actors

curl -d '{"title":"Avengers","release_date":"2020-01-02"}' -H "Content-Type: application/json" -X POST http://localhost:5000/movies

FOR TESTING 
@app.route('/movies/<int:movie_id>')
#@requires_auth('view:movies')
def get_movie_by_id(movie_id):
    #movie = Movie.query.filter(movie_id)
    movie = Movie.query.filter_by(id=movie_id).first()
    if movie is None:
        abort(404)
    return jsonify({
                'success': True,
                'title': movie.title,
                'release_date': movie.release_date
            }), 200
'''
# /movies endpoint to get all movies by querying the DB, retrun json response
@app.route('/movies')
@requires_auth('view:movies')
def get_movies(payload):
    movies_query = Movie.query.all()
    if len(movies_query) == 0:
        abort(404)
    movies_list = [movie.formatted_json() for movie in movies_query]
    
    return jsonify({
                'success': True,
                'movies': movies_list,
            }), 200
##########

# /actors endpoint to get all actors by querying the DB, retrun json response 
@app.route('/actors')
@requires_auth('view:actors')
def get_actors(payload):
    actors_query = Actor.query.all()
   
    if len(actors_query) == 0:
        abort(404)
    
    actors_list = [actor.formatted_json() for actor in actors_query]
    return jsonify({
                'success': True,
                'actors': actors_list,
            }), 200
          
###################### Delete ######################

# /movies/<int:movie_id> endpoint to delete a movie
@app.route('/movies/<int:movie_id>', methods=['DELETE'])
@requires_auth('delete:movies')
def delete_movie(payload, movie_id):

    movie = Movie.query.get(movie_id)

    if movie is None:
        abort(404)

    movie.delete()
    db.session.commit()
    db.session.close()

    return jsonify({
        'success': True,
        'Message': "deleted movie_id: " + str(movie_id),
    }), 200

# /actors/<int:actor_id> endpoint to delete an actor
@app.route('/actors/<int:actor_id>', methods=['DELETE'])
#@requires_auth('delete:actors')
def delete_actor(payload, actor_id):

    actor = Actor.query.get(actor_id)

    if actor is None:
        abort(404)

    actor.delete()
    db.session.commit()
    db.session.close()

    return jsonify({
        'success': True,
        'Message': "deleted actor_id: " + str(actor_id),
    }), 200

###################### Create ######################

# /movies endpoint to create a new movie
@app.route('/movies', methods=['POST'])
@requires_auth('create:movie')
def create_new_movie(payload):
      body = request.get_json()
      
      if body is None:
        abort(422)

      new_title = body.get('title', None)
      new_release_date = body.get('release_date', None)

      movie = Movie(title=new_title, release_date=new_release_date)
      try:
        movie.insert()
      except BaseException:
        abort(400)

      return jsonify({
        'success': True,
        'created_movie_id': movie.id,
        'created_movie_title': movie.title
      }),200

# /actors endpoint to create a new actor
@app.route('/actors', methods=['POST'])
@requires_auth('create:actor')
def create_new_actor(payload):
      body = request.get_json()
      
      if body is None:
        abort(422)

      new_name = body.get('name', None)
      new_age = body.get('age', None)
      new_gender= body.get('gender', None)

      actor = Actor(name=new_name, age=new_age, gender=new_gender)

      try:
        actor.insert()
      except BaseException:
        abort(400)

      return jsonify({
        'success': True,
        'created_actor_id': actor.id,
        'created_actor_name': actor.name
      }),200

###################### Update ######################

# /movies/<int:movie_id> endpoint to update an existing movie

@app.route('/movies/<int:movie_id>', methods=['PATCH'])
@requires_auth('update:movie')
def update_movie(payload, movie_id):

    movie = Movie.query.get(movie_id)

    if movie is None:
        abort(404)

    body = request.get_json()
    if body is None:
        abort(422)
    
    if 'title' in body:
        movie.title = body.get('title')
    if 'release_date' in body:
            movie.role = body.get('release_date')

    movie.update()

    return jsonify({
        'success': True,
        'updated_movie_id': movie.id,
        'updated_movie_title': movie.title,
        'updated_movie_release_date': movie.release_date
    }), 200

# /actors endpoint to update an existing actor
@app.route('/actors/<int:actor_id>', methods=['PATCH'])
@requires_auth('update:actor')
def update_actor(payload, actor_id):

    actor = Actor.query.get(actor_id)

    if actor is None:
        abort(404)

    body = request.get_json()
    if body is None:
        abort(422)
    
    if 'name' in body:
        actor.name = body.get('name')
    if 'age' in body:
            actor.age = body.get('age')
    if 'gender' in body:
            actor.gender = body.get('gender')

    actor.update()

    return jsonify({
        'success': True,
        'updated_actor_id': actor.id,
        'updated_actor_name': actor.name,
        'updated_actor_age': actor.age,
        'updated_actor_gender': actor.gender,
    }), 200

############# Error Handling #############

#return 400 for Bad Request
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'Bad Request'
            }), 400

#return 401 for Unauthorized
@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        'success': False,
        'error': 401,
        'message': 'Unauthorized'
            }), 401

#return 422 for unprocessable entity
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
            'success': False, 
            'error': 422,
            'message': 'unprocessable'
            }), 422

#return 404 for resource not found
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message':'not found'
    }),404

#return 404 for resource not found
@app.errorhandler(405)
def Method_not_allowed(error):
    return jsonify({
        'success': False,
        'error': 405,
        'message':'Method not allowed'
    }),405

#return 500 for Internal Server Error
@app.errorhandler(500)
def server_error(error):
    return jsonify({
        'success': False,
        'error': 500,
        'message':'Internal Server Error'
    }),500

#retrun error for any authorization errors
@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error['description']
    }), error.status_code

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)