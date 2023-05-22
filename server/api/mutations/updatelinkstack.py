import graphene
from database.models.linkstack import LinkStackObject
from app import db
from flask_graphql_auth import mutation_header_jwt_required, get_jwt_identity


class UpdateLinkStack(graphene.Mutation):
    class Arguments:
        stackid = graphene.String()
        stacktitle = graphene.String()
        stackdesc = graphene.String()
        stacktheme = graphene.String()

    linkstack = graphene.Field(lambda: LinkStackObject)

    @mutation_header_jwt_required
    def mutate(self, info, stackid, stacktitle=None, stackdesc=None, stacktheme=None):
        useremail = get_jwt_identity()
        linkstack = LinkStackObject.query.filter_by(stackid=stackid, useremail=useremail).first()
        
        if linkstack is None:
            raise Exception('Error: No linkstack found with the given id for this user')

        if stacktitle is not None:
            linkstack.stacktitle = stacktitle

        if stackdesc is not None:
            linkstack.stackdesc = stackdesc

        if stacktheme is not None:
            linkstack.stacktheme = stacktheme

        db.session.commit()
        return UpdateLinkStack(linkstack=linkstack)