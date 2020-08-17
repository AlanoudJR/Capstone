# Casting Agency Project

This is the final project for Udacity Full-Stack Web Developer Nanodegree Program "Capstone Project".

# Motivation for project
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.


The Flask app consists of an API with eight endpoints:

- GET /actors and /movies
- DELETE /actors/ and /movies/
- POST /actors and /movies and
- PATCH /actors/ and /movies/

It includes 3 main roles as well:
- Casting Assistant
  - view:actors
  - view:movies	
- Casting Director
  - create:actor / delete:actors
  - update:actor / update:movie	
  - view:actors	/ view:movies
- Executive Producer
  - create:actor / delete:actors
  - update:actor / update:movie	
  - view:actors	/ view:movies
  - create:movie / delete:movies

# Project dependencies, local development and hosting instructions,
- Flask is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- SQLAlchemy is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- Flask-CORS is the extension we'll use to handle cross origin requests from our frontend server.

- Auth0 is the authentication and authorization system we'll use to handle users with different roles with more secure and easy ways

- PostgreSQL this project is integrated with a popular relational database PostgreSQL, though other relational databases can be used with a little effort.
- Heroku is a platform as a service (PaaS) that enables developers to build, run, and operate applications entirely in the cloud.


## Database Setup
With Postgres running, restore a database using the capstone.psql file provided. From the backend folder in terminal run:
```
psql capstone < capstone.psql
```
For the testing run 
```
psql capstone_test < capstone_test.psql
```
## Initial setup

To start and run the local development server,

1. Initialize and activate a virtualenv:
  ```
  $ cd YOUR_PROJECT_DIRECTORY_PATH/
  $ virtualenv --no-site-packages env
  $ source env/bin/activate
  ```

2. Install the dependencies:
  ```
  $ pip install -r requirements.txt
  ```

3. Run the development server:
  ```
  $ export FLASK_APP=app
  $ export FLASK_ENV=development # enables debug mode
  $ python3 app.py
  ```


# Endpoints

#### GET '/movies'
- Returns: return a list of all movies (Title and release date)
- Request Arguments: None
- Example: http://127.0.0.1:5000/movies

Response:
```
{
    "movies": [
        {
            "id": 1,
            "release_date": "Fri, 22 Jun 2018 19:10:25 GMT",
            "title": "The Nightingale"
        },
        {
            "id": 2,
            "release_date": "Fri, 22 Jun 2018 00:00:00 GMT",
            "title": "The Ready Player One"
        },
        {
            "id": 3,
            "release_date": "Sat, 22 Jun 2019 00:00:00 GMT",
            "title": "The Lion King"
        }
    ],
    "success": true
}
```
#### GET '/actors'
- Returns: return a list of all actors (name, age and gender)
- Request Arguments: None
- Example: http://127.0.0.1:5000/actors

Response:
```
{
    "actors": [
        {
            "age": 56,
            "gender": "Male",
            "id": 1,
            "name": "Brad Pitt"
        },
        {
            "age": 57,
            "gender": "Male",
            "id": 2,
            "name": "Johnny Depp"
        },
        {
            "age": 45,
            "gender": "Female",
            "id": 3,
            "name": "Angelina Jolie"
        }
    ],
    "success": true
}
```
#### Post '/actors'
- Posts: an actor.
- Example: http://127.0.0.1:5000/actors

Request:
```
{
    "name": "Sarah",
    "age": "29",
    "gender": "female"
}
```
Response:
```
{
    "created_actor_id": 11,
    "created_actor_name": "Sarah",
    "success": true
}
```
#### Post '/movies'
- Posts: a movie.
- Example: http://127.0.0.1:5000/movies

Request:
```
{
    "title": "Avengers",
    "release_date": "2020-01-02"
}
```
Response:
```
{
    "created_movie_id": 8,
    "created_movie_title": "Avengers",
    "success": true
}
```

#### Patch '/movies/<int:movie_id>'
- Updates a movie.
- Example: http://127.0.0.1:5000/movies/7

Request:
```
{
    "title": "Avengers",
    "release_date": "2022-01-02"
}
```
Response:
```
{
    "success": true,
    "updated_movie_id": 7,
    "updated_movie_release_date": "Mon, 22 Jun 2020 00:00:00 GMT",
    "updated_movie_title": "Avengers"
}
```

#### Patch '/actors/<int:actor_id>'
- Updates an actor.
- Example: http://127.0.0.1:5000/actors/7

Request:
```
{
    "name":"Adam",
    "age":"27",
    "gender":"Male"
}

```
Response:
```
{
    "success": true,
    "updated_actor_age": 27,
    "updated_actor_gender": "Male",
    "updated_actor_id": 7,
    "updated_actor_name": "Adam"
}
```

#### Patch '/actors/<int:actor_id>'
- Updates an actor.
- Example: http://127.0.0.1:5000/actors/7
- Request: none.

Response:
```
{
    "success": true,
    "updated_actor_age": 27,
    "updated_actor_gender": "Male",
    "updated_actor_id": 7,
    "updated_actor_name": "Adam"
}
```
#### Delete '/actors/<int:actor_id>'
- Deletes an actor.
- Example: http://127.0.0.1:5000/actors/9
- Request: none.

Response:
```
{
    "Message": "deleted actor_id: 9",
    "success": true
}
```

#### Delete '/movies/<int:movie_id>'
- Deletes a movie.
- Example: http://127.0.0.1:5000/movies/5
- Request: none.

Response:
```
{
    "Message": "deleted movie_id: 5",
    "success": true
}
```

# Error Handling
Errors are returned as JSON objects in the following format:
```
{
    'success': False, 
    'error': 422,
    'message': 'unprocessable'
}
```
The API will return the following errors based on how the request fails:

- 400: Bad Request
- 401: Unauthorized
- 404: Resource Not Found
- 405: Method Not Allowed
- 422: Unprocessable Entity
- 500: Internal Server Error
