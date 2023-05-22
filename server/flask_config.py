# Flask Imports
from flask import Flask, g
import datetime
from flask_cors import CORS

# SQL Alchemy Imports
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base

# Graph QL Imports
from flask_graphql import GraphQLView
import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType

# ENV Imports
from dotenv import load_dotenv
import os

# Auth Imports
from flask_graphql_auth import (
    AuthInfoField,
    GraphQLAuth,
    get_jwt_identity,
    create_access_token,
    create_refresh_token,
    query_jwt_required,
    mutation_jwt_refresh_token_required,
    mutation_header_jwt_required
)
import bcrypt
from datetime import timedelta

# Create Flask app
app = Flask(__name__)
CORS(app, resources={r"/graphql": {"origins": ["http://localhost:3000", "https://studio.apollographql.com"]}}, supports_credentials=True, allow_headers=['Content-Type', 'Authorization'])

# Load environment variables
load_dotenv()
PASSWORD = os.getenv("POSTGRE_PASSWORD") 
USERNAME = os.getenv("POSTGRE_USERNAME")
HOST = os.getenv("POSTGRE_HOST")
PORT = os.getenv("POSTGRE_PORT")
DATABASE = os.getenv("POSTGRE_DATABASE")
SECRET = os.getenv("JWT_SECRET")

# Config the server with the environment variables
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = f"{SECRET}"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)  # Expiration time is now 24 hours
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

# Connect the database to the Flask server
db = SQLAlchemy(app)

# Configure authorization
auth = GraphQLAuth(app)

# Map existing relationships and data to SQLAlchemy models
Base = automap_base()
with app.app_context():
    Base.prepare(db.engine, reflect=True)

# Add the database to a Flask global variable
@app.before_request
def before_request():
    g.db = db.session
