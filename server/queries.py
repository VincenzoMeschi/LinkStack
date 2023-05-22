import graphene
from models import UserObject, LinkObject, LinkStackObject

class Query(graphene.ObjectType):
    users = graphene.List(UserObject)
    links = graphene.List(LinkObject)
    linkstacks = graphene.List(LinkStackObject)

    def resolve_users(self, info):
        return UserObject.get_query(info).all()

    def resolve_links(self, info):
        return LinkObject.get_query(info).all()

    def resolve_linkstacks(self, info):
        return LinkStackObject.get_query(info).all()
