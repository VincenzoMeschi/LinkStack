from sqlalchemy.ext.automap import automap_base
from utils.env import load_env_variables
from app import app
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_graphql_auth import GraphQLAuth

env_variables = load_env_variables()
USERNAME = env_variables["POSTGRE_USERNAME"]
PASSWORD = env_variables["POSTGRE_PASSWORD"]
HOST = env_variables["POSTGRE_HOST"]
PORT = env_variables["POSTGRE_PORT"]
DATABASE = env_variables["POSTGRE_DATABASE"]
SECRET = env_variables["JWT_SECRET"]

# Config the server with the env variables
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = f"{SECRET}"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)  # Expiration time is now 24 hours
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

# Connect the database to the Flask server
db = SQLAlchemy(app)

# Configure authorization
auth = GraphQLAuth(app)

Base = automap_base()

