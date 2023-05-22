import graphene
from database.models.user import UserObject
from database.models.link import LinkObject
from database.models.linkstack import LinkStackObject


class Query(graphene.ObjectType):
    users = graphene.List(UserObject)
    links = graphene.List(LinkObject)   
    link_stacks = graphene.List(LinkStackObject)
    view_link_stack = graphene.Field(LinkStackObject, stackid=graphene.String(required=True))
    view_user_link_stacks = graphene.List(LinkStackObject, useremail=graphene.String(required=True))

    def resolve_users(self, info):
        print("Resolving users...")
        query = UserObject.get_query(info)
        return query.all()
    
    def resolve_links(self, info):
        query = LinkObject.get_query(info)
        return query.all()
    
    def resolve_link_stacks(self, info):
        query = LinkStackObject.get_query(info)
        return query.all()
    
    def resolve_view_link_stack(self, info, stackid):
        print(f"Resolving viewLinkStack for stackid: {stackid}")

        query = LinkStackObject.get_query(info)
        linkstack = query.filter_by(stackid=stackid).first()

        if linkstack is None:
            raise Exception('Error: No linkstack found with the given id')

        link_query = LinkObject.get_query(info)
        links = link_query.filter_by(stackid=stackid).all()

        linkstack.links = links

        return linkstack

    
    def resolve_view_user_link_stacks(self, info, useremail):
        query = LinkStackObject.get_query(info)
        linkstacks = query.filter_by(useremail=useremail).all()

        if not linkstacks:
            print('Error: No linkstacks found with the given useremail')

        return linkstacks