from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base

from flask_graphql import GraphQLView
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

# ENV IMPORTS
from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv()
PASSWORD = os.getenv("POSTGRE_PASSWORD") 
USERNAME = os.getenv("POSTGRE_USERNAME")
HOST = os.getenv("POSTGRE_HOST")
PORT = os.getenv("POSTGRE_PORT")
DATABASE = os.getenv("POSTGRE_DATABASE")

app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"

db = SQLAlchemy(app)

Base = automap_base()
with app.app_context():
    Base.prepare(db.engine, reflect=True)

class UserObject(SQLAlchemyObjectType):
    class Meta:
        model = Base.classes.appuser

class LinkObject(SQLAlchemyObjectType):
    class Meta:
        model = Base.classes.link

class LinkStackObject(SQLAlchemyObjectType):
    class Meta:
        model = Base.classes.linkstack

class PasswordObject(SQLAlchemyObjectType):
    class Meta:
        model = Base.classes.password


class Query(graphene.ObjectType):
    users = graphene.List(UserObject)
    links = graphene.List(LinkObject)   
    link_stacks = graphene.List(LinkStackObject)        
    passwords = graphene.List(PasswordObject) 

    def resolve_users(self, info):
        query = UserObject.get_query(info)
        return query.all()
    
    def resolve_links(self, info):
        query = LinkObject.get_query(info)
        return query.all()
    
    def resolve_link_stacks(self, info):
        query = LinkStackObject.get_query(info)
        return query.all()
    
    def resolve_passwords(self, info):
        query = PasswordObject.get_query(info)
        return query.all()
    
schema = graphene.Schema(query=Query)
# Add the GraphQL endpoint
app.add_url_rule(
    "/graphql",
    view_func=GraphQLView.as_view(
        "graphql",
        schema=schema,
        graphiql=True,
    )
)

