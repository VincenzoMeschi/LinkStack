import graphene
from datetime import datetime
from flask_graphql_auth import (
    mutation_header_jwt_required,
    get_jwt_identity,
    create_access_token,
    create_refresh_token
)
import bcrypt

from models import UserObject, LinkObject, LinkStackObject

class CreateUser(graphene.Mutation):
    class Arguments:
        useremail = graphene.String(required=True)
        password = graphene.String(required=True)

    user = graphene.Field(UserObject)

    def mutate(self, info, useremail, password):
        # Check if user already exists
        existing_user = UserObject.get_query(info).filter_by(useremail=useremail).first()
        if existing_user:
            raise Exception("User already exists!")

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        # Create a new user object
        new_user = UserObject(useremail=useremail, password=hashed_password)

        # Add the user to the session and commit changes to the database
        info.context["session"].add(new_user)
        info.context["session"].commit()

        return CreateUser(user=new_user)

class CreateLink(graphene.Mutation):
    class Arguments:
        stackid = graphene.String(required=True)
        url = graphene.String(required=True)
        description = graphene.String(required=True)

    link = graphene.Field(LinkObject)

    def mutate(self, info, stackid, url, description):
        # Create a new link object
        new_link = LinkObject(stackid=stackid, url=url, description=description)

        # Add the link to the session and commit changes to the database
        info.context["session"].add(new_link)
        info.context["session"].commit()

        return CreateLink(link=new_link)

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    create_link = CreateLink.Field()
