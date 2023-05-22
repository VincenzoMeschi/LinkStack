import graphene
import bcrypt
import datetime
from database.model import Base
from app import db
from database.models.user import UserObject

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

        db.session.add(password_instance)
        db.session.add(user_instance)
        db.session.commit()

        ok = True
        return CreateUser(user=user_instance, ok=ok)