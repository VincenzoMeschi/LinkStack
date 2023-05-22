from graphene_sqlalchemy import SQLAlchemyObjectType
from database.model import Base

class LinkObject(SQLAlchemyObjectType):
    class Meta:
        model = Base.classes.link