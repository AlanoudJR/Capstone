import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from models import Movie, Actor, setup_db, db_drop_and_create_all
from auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)
'''
SQLALCHEMY_DATABASE_URI = 'postgres://alanoudjrayes@localhost:5432/capstone'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
'''

'''
https://test-alanoud.us.auth0.com/authorize?audience=capstone&response_type=token&client_id=mYDFGwfZsRg6NwjCPZdP7rj15hV8fUCa&redirect_uri=https://127.0.0.1:8080/movies
'''
db_drop_and_create_all()

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

@app.route('/movies')
@requires_auth('view:movies')
def get_movies():
    movies_query = Movie.query.all()
    if len(movies_query) == 0:
        abort(404)
    movies_list = [movie.formatted_json() for movie in movies_query]
    
    return jsonify({
                'success': True,
                'movies': movies_list,
            }), 200

@app.route('/actors')
@requires_auth('view:actors')
def get_actors():
    actors_query = Actor.query.all()
   
    if len(actors_query) == 0:
        abort(404)
    
    actors_list = [actor.formatted_json() for actor in actors_query]
    
    return jsonify({
                'success': True,
                'actors': actors_list,
            }), 200
          
###################### Delete ######################

@app.route('/movies/<int:movie_id>', methods=['DELETE'])
@requires_auth('delete:movies')
def delete_movie(self, movie_id):

    movie = Movie.query.filter(movie_id)

    if movie is None:
        abort(404)

    movie.delete()
    db.session.commit()
    db.session.close()

    return jsonify({
        'success': True,
        'Message': "deleted movie_id: " + movie_id,
    }), 200
  
@app.route('/actor/<int:actor_id>', methods=['DELETE'])
@requires_auth('delete:actors')
def delete_actor(self, actor_id):

    actor = Actor.query.filter(actor_id)

    if actor is None:
        abort(404)

    actor.delete()
    db.session.commit()
    db.session.close()

    return jsonify({
        'success': True,
        'Message': "deleted actor_id: " + actor_id,
    }), 200

###################### Create ######################
@app.route('/movies', methods=['POST'])
@requires_auth('create:movie')
def create_new_movie():
      body = request.get_json()
      
      if 'title' and 'release_date' not in body:
        abort(422)

      title = body['title']
      release_date = body['release_date']

      movie = Movie(title=title, release_date=release_date)
      try:
        movie.insert()
      except BaseException:
        abort(400)

      return jsonify({
        'success': True,
        'created_movie_id': movie.id,
        'created_movie_title': movie.title
      }),200
@app.route('/actors', methods=['POST'])
@requires_auth('create:actor')
def create_new_actor():
      body = request.get_json()
      
      if 'name' and 'age' and 'gender' not in body:
        abort(422)

      name = body['name']
      age = body['age']
      gender= body['gender']

      actor = Actor(name=name, age=age, gender=gender)
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

#PATCH /actors/ and /movies/
@app.route('/movies/<int:movie_id>', methods=['PATCH'])
@requires_auth('update:movie')
def update_movie(self, movie_id):

    movie = Movie.query.get(movie_id)

    if movie is None:
        abort(404)

    body = request.get_json()
    if body is None:
        abort(400)
    
    if 'title' in body:
        actor.title = body['title']
    if 'release_date' in body:
            actor.role = body['release_date']

    movie.update()

    return jsonify({
        'success': True,
        'updated_movie': movie,
    }), 200

@app.route('/actors/<int:actor_id>', methods=['PATCH'])
@requires_auth('update:actor')
def update_actor(self, actor_id):

    actor = Actor.query.get(actor_id)

    if actor is None:
        abort(404)

    body = request.get_json()
    if body is None:
        abort(400)
    
    if 'name' in body:
        actor.title = body['name']
    if 'age' in body:
            actor.role = body['age']
    if 'gender' in body:
            actor.gender = body['gender']

    actor.update()

    return jsonify({
        'success': True,
        'updated_actor': actor,
    }), 200
    #Abort 400 when there is an exception 
    except BaseException:
        abort(400)
    #RETRUN THE ID OF the deleted drink and return status code.
    return jsonify({
        'success': True, 
        'delete': id}
    ), 200


############# Error Handling #############

#return 400 for Bad Request
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'Bad Request'
            }), 400

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