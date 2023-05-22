import graphene
from flask_graphql_auth import create_access_token, create_refresh_token
from database.models.user import UserObject
import bcrypt


class UserLogin(graphene.Mutation):
    class Arguments:
        useremail = graphene.String()
        password = graphene.String()
        
    access_token = graphene.String()
    refresh_token = graphene.String()
    useremail = graphene.String()

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

        return UserLogin(access_token=access_token, refresh_token=refresh_token, useremail=useremail)