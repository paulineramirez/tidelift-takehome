# Tidelift Hello Flask

This is a basic Flask app that you can use to plug in the routes
for the Tidelift coding exercise.

## Setup 
- Make a new python virtualenv `python -m venv`
- Activate it `source ENVNAMEHERE/bin/activate`
- Install dependencies `pip install -r requirements.txt`

## Running

The invoke tasks.py has a few useful tasks to be able to run and test
the application as you work.

- `invoke run` # Runs a dev server on port 5000
- `invoke test`  # Runs the tests
- `invoke lint` # Checks for linting errors
- `invoke fix` # Fixes linting errors


## Creating requests

You can call either of the endpoints through Terminal with either of the below:

`curl http://127.0.0.1:5000/package/releases/tiny-tarball`

`curl http://127.0.0.1:5000/package/health/dummy/0.8`
