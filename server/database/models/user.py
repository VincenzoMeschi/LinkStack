from graphene_sqlalchemy import SQLAlchemyObjectType
from database.model import Base
from database.models.linkstack import LinkStackObject
import graphene

class UserObject(SQLAlchemyObjectType):
    linkstacks = graphene.List(LinkStackObject)

    class Meta:
        model = Base.classes.appuser

    def resolve_linkstacks(self, info):
        linkstack_query = LinkStackObject.get_query(info)
        return linkstack_query.filter_by(useremail=self.useremail).all()