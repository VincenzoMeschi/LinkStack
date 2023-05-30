from flask_cors import CORS
from flask_graphql import GraphQLView
from api.schema import schema
from utils.env import load_env_variables
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_graphql_auth import GraphQLAuth
from sqlalchemy.ext.automap import automap_base

class AppConfig:
  def __init__(self, app):
    self.app = app
  
  def init_cors(self):
    CORS(self.app, resources={r"/graphql": {"origins": ["http://localhost:3000", "https://studio.apollographql.com"]}}, supports_credentials=True, allow_headers=['Content-Type', 'Authorization'])

  def init_db(self):
    env_variables = load_env_variables()
    USERNAME = env_variables["POSTGRE_USERNAME"]
    PASSWORD = env_variables["POSTGRE_PASSWORD"]
    HOST = env_variables["POSTGRE_HOST"]
    PORT = env_variables["POSTGRE_PORT"]
    DATABASE = env_variables["POSTGRE_DATABASE"]
    SECRET = env_variables["JWT_SECRET"]

    # Config the server with the env variables
    self.app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
    self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    self.app.config["JWT_SECRET_KEY"] = f"{SECRET}"
    self.app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)  # Expiration time is now 24 hours
    self.app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

    # Connect the database to the Flask server
    db = SQLAlchemy(self.app)

  def init_auth(self):
    # Configure authorization
    auth = GraphQLAuth(self.app)

  def init_automap(self):
    Base = automap_base()
    Base.prepare(db.engine, reflect=True)
    return Base

  def init_graphql(self):
    self.app.add_url_rule(
      "/graphql",
      view_func=GraphQLView.as_view(
          "graphql",
          schema=schema,
          graphiql=True,
          get_context=lambda: {'session': db},
      )
    )
