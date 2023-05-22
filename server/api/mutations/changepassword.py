import graphene
from database.models.password import PasswordObject
from app import db
from database.model import Base
import datetime


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