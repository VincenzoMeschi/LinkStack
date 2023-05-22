from graphene_sqlalchemy import SQLAlchemyObjectType
from database.model import Base

class PasswordObject(SQLAlchemyObjectType):
    class Meta:
        model = Base.classes.password