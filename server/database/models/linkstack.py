from graphene_sqlalchemy import SQLAlchemyObjectType
from database.model import Base
from database.models.link import LinkObject
import graphene

class LinkStackObject(SQLAlchemyObjectType):
    links = graphene.List(LinkObject)

    class Meta:
        model = Base.classes.linkstack

    def resolve_links(self, info):
        link_query = LinkObject.get_query(info)
        return link_query.filter_by(stackid=self.stackid).all()