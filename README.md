# flask-tutorial
# Init db
flask --app flaskr init-db

# Start server
flask --app flaskr run --debug

# Test
pip3 install -e .
pytest
coverage run -m pytest

# Deploy to production
https://flask.palletsprojects.com/en/3.0.x/tutorial/deploy/