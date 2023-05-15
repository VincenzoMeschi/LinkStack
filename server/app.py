# Flask Imports
from flask import Flask, g
import datetime

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
    query_header_jwt_required,
    mutation_jwt_refresh_token_required,
    mutation_jwt_required
)
import bcrypt

# Create Flask app
app = Flask(__name__)

# Load enviroment variables
load_dotenv()
PASSWORD = os.getenv("POSTGRE_PASSWORD") 
USERNAME = os.getenv("POSTGRE_USERNAME")
HOST = os.getenv("POSTGRE_HOST")
PORT = os.getenv("POSTGRE_PORT")
DATABASE = os.getenv("POSTGRE_DATABASE")
SECRET = os.getenv("JWT_SECRET")

# Config the server with the env variables
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
app.config["JWT_SECRET_KEY"] = f"{SECRET}"

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

# Create UserObject model
class UserObject(SQLAlchemyObjectType):
    class Meta:
        model = Base.classes.appuser

# Create LinkObject model
class LinkObject(SQLAlchemyObjectType):
    class Meta:
        model = Base.classes.link

# Create LinkStackObject model
class LinkStackObject(SQLAlchemyObjectType):
    class Meta:
        model = Base.classes.linkstack

# Create PasswordObject model
class PasswordObject(SQLAlchemyObjectType):
    class Meta:
        model = Base.classes.password

# Create Query class and its resolvers
class Query(graphene.ObjectType):
    users = graphene.List(UserObject)
    links = graphene.List(LinkObject)   
    link_stacks = graphene.List(LinkStackObject)

    # Resolve user request
    def resolve_users(self, info):
        print("Resolving users...")
        query = UserObject.get_query(info)
        return query.all()
    
    # Resolve links request
    def resolve_links(self, info):
        query = LinkObject.get_query(info)
        return query.all()
    
    # Resolve LinkStack request
    def resolve_link_stacks(self, info):
        query = LinkStackObject.get_query(info)
        return query.all()
    

# Handle user mutations (create new user)
class CreateUser(graphene.Mutation):
    class Arguments:
        useremail = graphene.String(required=True)
        userfirst = graphene.String(required=True)
        userlast = graphene.String(required=True)
        userimg = graphene.String()
        password = graphene.String(required=True)

    ok = graphene.Boolean()
    user = graphene.Field(lambda: UserObject)

    def mutate(root, info, useremail, userfirst, userlast, password, userimg=None):
        user_model = Base.classes.appuser
        password_model = Base.classes.password

        # Convert user password into encrypted hash+salt to send to DB
        password_bytes = password.encode('utf-8')
        hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
        passhash = hashed.decode('utf-8')

        # Create password instance to prepare to send to DB
        password_instance = password_model(
            passhash=passhash,
            passdate=datetime.datetime.utcnow()
        )

        # Create user instance to prepare to send to DB
        user_instance = user_model(
            useremail=useremail,
            userfirst=userfirst,
            userlast=userlast,
            userimg=userimg,
            usercreated=datetime.datetime.utcnow(),
            passhash=passhash,
        )

        # Send instances to the DB & commit the changes
        db.session.add(password_instance)
        db.session.add(user_instance)
        db.session.commit()

        ok = True
        return CreateUser(user=user_instance, ok=ok)


class CreateLink(graphene.Mutation):
    class Arguments:
        linkid = graphene.String(required=True)
        linkhttp = graphene.String(required=True)
        linkplatform = graphene.String(required=True)
        linknickname = graphene.String(required=True)
        linktitle = graphene.String(required=True)
        linkdesc = graphene.String(required=True)
        stackid = graphene.String(required=True)

    ok = graphene.Boolean()
    link = graphene.Field(lambda: LinkObject)

    def mutate(root, info, linkid, linkhttp, linkplatform, linknickname, linktitle, linkdesc, stackid):
        link_model = Base.classes.link
        link_instance = link_model(linkid=linkid, linkhttp=linkhttp, linkplatform=linkplatform, linknickname=linknickname, linktitle=linktitle, linkdesc=linkdesc, stackid=stackid)
        db.session.add(link_instance)
        db.session.commit()
        ok = True
        return CreateLink(link=link_instance, ok=ok)


class CreateLinkStack(graphene.Mutation):
    class Arguments:
        stackid = graphene.String(required=True)
        stacktitle = graphene.String(required=True)
        stackdesc = graphene.String(required=True)
        stacktheme = graphene.String(default_value="default")
        useremail = graphene.String(required=True)

    ok = graphene.Boolean()
    linkstack = graphene.Field(lambda: LinkStackObject)

    def mutate(root, info, stackid, stacktitle, stackdesc, useremail, stacktheme=None):
        linkstack_model = Base.classes.linkstack
        linkstack_instance = linkstack_model(stackId=stackid, stackTitle=stacktitle, stackDesc=stackdesc, stackTheme=stacktheme, userEmail=useremail)
        db.session.add(linkstack_instance)
        db.session.commit()
        ok = True
        return CreateLinkStack(linkstack=linkstack_instance, ok=ok)
    
class CreatePassword(graphene.Mutation):
    class Arguments:
        passhash = graphene.String(required=True)

    ok = graphene.Boolean()
    password = graphene.Field(lambda: PasswordObject)

    def mutate(root, info, passhash):
        password_model = Base.classes.password
        password_instance = password_model(
            passHash=passhash, 
            passDate=datetime.datetime.utcnow()
        )
        db.session.add(password_instance)
        db.session.commit()
        ok = True
        return CreatePassword(password=password_instance, ok=ok)

class ChangePassword(graphene.Mutation):
    class Arguments:
        useremail = graphene.String(required=True)
        oldpasshash = graphene.String(required=True)
        newpasshash = graphene.String(required=True)
        newpasssalt = graphene.String(required=True)

    ok = graphene.Boolean()
    password = graphene.Field(lambda: PasswordObject)

    def mutate(root, info, useremail, oldpasshash, newpasshash, newpasssalt):
        user_model = Base.classes.appuser
        password_model = Base.classes.password
        
        user_instance = db.session.query(user_model).get(useremail)
        password_instance = db.session.query(password_model).get((user_instance.passhash, user_instance.passsalt))

        if user_instance.passhash != oldpasshash:
            raise Exception('Invalid password')

        new_password_instance = password_model(
            passhash=newpasshash, 
            passsalt=newpasssalt, 
            passdate=datetime.datetime.utcnow()
        )

        user_instance.passhash = newpasshash
        user_instance.passsalt = newpasssalt

        db.session.add(new_password_instance)
        db.session.delete(password_instance)

        db.session.commit()

        ok = True
        return ChangePassword(password=new_password_instance, ok=ok)
    
class AuthMutation(graphene.Mutation):
    access_token = graphene.String()
    refresh_token = graphene.String()

    class Arguments:
        useremail = graphene.String()
        password = graphene.String()
    
    def mutate(self, info, useremail, password):
        user_query = UserObject.get_query(info)
        user = user_query.filter_by(useremail=useremail).first()

        if not user:
            raise Exception('Authentication Failure: User is not registered')

        password_bytes = password.encode('utf-8')
        hashed_password = bcrypt.hashpw(password_bytes, user.passhash.encode('utf-8'))

        if hashed_password != user.passhash.encode('utf-8'):
            raise Exception('Authentication Failure: Invalid password')

        return AuthMutation(
            access_token=create_access_token(useremail),
            refresh_token=create_refresh_token(useremail)
        )
    
class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    create_link = CreateLink.Field()
    create_link_stack = CreateLinkStack.Field()
    auth = AuthMutation.Field()

# Create schema from Query and Mutation classes
schema = graphene.Schema(query=Query, mutation=Mutation)

# Add the GraphQL endpoint
app.add_url_rule(
    "/graphql",
    view_func=GraphQLView.as_view(
        "graphql",
        schema=schema,
        graphiql=True,
        get_context=lambda: {'session': g.db},
    )
)

# Run app when __name__ == __main__
if __name__ == '__main__':
    app.run(debug=True)
