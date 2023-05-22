import graphene
from database.model import Base
from app import db
from database.models.linkstack import LinkStackObject
from flask_graphql_auth import mutation_header_jwt_required, get_jwt_identity



class CreateLinkStack(graphene.Mutation):
    class Arguments:
        stacktitle = graphene.String()
        stackdesc = graphene.String()
        stacktheme = graphene.String()

    linkstack = graphene.Field(lambda: LinkStackObject)

    @mutation_header_jwt_required
    def mutate(self, info, stacktitle, stackdesc, stacktheme):
        try:
            useremail = get_jwt_identity()
        except Exception as e:
            raise Exception('Error: Unable to fetch token identity: {}'.format(e))

        linkstack_model = Base.classes.linkstack
        linkstack = linkstack_model(stacktitle=stacktitle, stackdesc=stackdesc, stacktheme=stacktheme, useremail=useremail)
        db.session.add(linkstack)
        db.session.commit()
        return CreateLinkStack(linkstack=linkstack)