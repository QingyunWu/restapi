from app import app
from db import db

db.init_app(app)

# create tables for db in the very first place, if it can see the tabls in models
@app.before_first_request
def create_tables():
    db.create_all()
