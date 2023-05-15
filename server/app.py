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
    query_jwt_required,
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

class LinkObject(SQLAlchemyObjectType):
    class Meta:
        model = Base.classes.link

class LinkStackObject(SQLAlchemyObjectType):
    links = graphene.List(LinkObject)

    class Meta:
        model = Base.classes.linkstack

    def resolve_links(self, info):
        link_query = LinkObject.get_query(info)
        return link_query.filter_by(linkstack_id=self.id).all()

class UserObject(SQLAlchemyObjectType):
    linkstacks = graphene.List(LinkStackObject)

    class Meta:
        model = Base.classes.appuser

    def resolve_linkstacks(self, info):
        linkstack_query = LinkStackObject.get_query(info)
        return linkstack_query.filter_by(userEmail=self.userEmail).all()


# Create PasswordObject model
class PasswordObject(SQLAlchemyObjectType):
    class Meta:
        model = Base.classes.password
    

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
    
class UserLogin(graphene.Mutation):
    class Arguments:
        useremail = graphene.String()
        password = graphene.String()

    access_token = graphene.String()
    refresh_token = graphene.String()

    def mutate(self, info, useremail, password):
        user_query = UserObject.get_query(info)
        user = user_query.filter_by(useremail=useremail).first()

        if not user:
            raise Exception('Authentication Failure: User is not registered')

        password_bytes = password.encode('utf-8')
        hashed_password = bcrypt.hashpw(password_bytes, user.passhash.encode('utf-8'))

        if hashed_password != user.passhash.encode('utf-8'):
            raise Exception('Authentication Failure: Invalid password')

        access_token = create_access_token(identity=useremail)
        refresh_token = create_refresh_token(identity=useremail)

        return UserLogin(access_token=access_token, refresh_token=refresh_token)


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

    @mutation_jwt_required
    def mutate(root, info, linkid, linkhttp, linkplatform, linknickname, linktitle, linkdesc, stackid):

        link_model = Base.classes.link
        link_instance = link_model(linkid=linkid, linkhttp=linkhttp, linkplatform=linkplatform, linknickname=linknickname, linktitle=linktitle, linkdesc=linkdesc, stackid=stackid)
        db.session.add(link_instance)
        db.session.commit()
        ok = True
        return CreateLink(link=link_instance, ok=ok)
    
class UpdateLink(graphene.Mutation):
    class Arguments:
        linkid = graphene.String(required=True)
        linkhttp = graphene.String()
        linkplatform = graphene.String()
        linknickname = graphene.String()
        linktitle = graphene.String()
        linkdesc = graphene.String()
        stackid = graphene.String()

    ok = graphene.Boolean()
    link = graphene.Field(lambda: LinkObject)

    @mutation_jwt_required
    def mutate(root, info, linkid, linkhttp=None, linkplatform=None, linknickname=None, linktitle=None, linkdesc=None, stackid=None):
        link_model = Base.classes.link
        link_instance = db.session.query(link_model).filter_by(linkid=linkid).first()

        if not link_instance:
            raise Exception('Error: No link found with the provided linkid')

        if linkhttp:
            link_instance.linkhttp = linkhttp
        if linkplatform:
            link_instance.linkplatform = linkplatform
        if linknickname:
            link_instance.linknickname = linknickname
        if linktitle:
            link_instance.linktitle = linktitle
        if linkdesc:
            link_instance.linkdesc = linkdesc
        if stackid:
            link_instance.stackid = stackid

        db.session.commit()
        ok = True
        return UpdateLink(link=link_instance, ok=ok)


class CreateLinkStack(graphene.Mutation):
    class Arguments:
        stacktitle = graphene.String()
        stackdesc = graphene.String()
        stacktheme = graphene.String()

    linkstack = graphene.Field(lambda: LinkStackObject)

    @mutation_jwt_required
    def mutate(self, info, stacktitle, stackdesc, stacktheme):
        useremail = get_jwt_identity()
        linkstack = LinkStackObject(stackTitle=stacktitle, stackDesc=stackdesc, stackTheme=stacktheme, userEmail=useremail)
        db.session.add(linkstack)
        db.session.commit()
        return CreateLinkStack(linkstack=linkstack)
    
class UpdateLinkStack(graphene.Mutation):
    class Arguments:
        stackid = graphene.String()
        stacktitle = graphene.String()
        stackdesc = graphene.String()
        stacktheme = graphene.String()

    linkstack = graphene.Field(lambda: LinkStackObject)

    @mutation_jwt_required
    def mutate(self, info, stackid, stacktitle=None, stackdesc=None, stacktheme=None):
        useremail = get_jwt_identity()
        linkstack = LinkStackObject.query.filter_by(stackId=stackid, userEmail=useremail).first()
        
        if linkstack is None:
            raise Exception('Error: No linkstack found with the given id for this user')

        if stacktitle is not None:
            linkstack.stackTitle = stacktitle

        if stackdesc is not None:
            linkstack.stackDesc = stackdesc

        if stacktheme is not None:
            linkstack.stackTheme = stacktheme

        db.session.commit()
        return UpdateLinkStack(linkstack=linkstack)

class ViewLinkStack(graphene.ObjectType):
    class Arguments:
        stackid = graphene.String()

    linkstack = graphene.Field(lambda: LinkStackObject)

    def resolve_linkstack(self, info, stackid):
        linkstack = LinkStackObject.query.filter_by(stackId=stackid).first()

        if linkstack is None:
            raise Exception('Error: No linkstack found with the given id')

        return linkstack

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
    
class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    user_login = UserLogin.Field()
    create_link = CreateLink.Field()
    update_link = UpdateLink.Field()
    create_link_stack = CreateLinkStack.Field()
    update_link_stack = UpdateLinkStack.Field()
    change_password = ChangePassword.Field()

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

    @query_jwt_required
    def resolve_protected(self, info):
        return 

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
