import graphene
from app import db
from database.models.link import LinkObject
from flask_graphql_auth import mutation_header_jwt_required


class DeleteLink(graphene.Mutation):
    class Arguments:
        linkid = graphene.String(required=True)

    ok = graphene.Boolean()

    @mutation_header_jwt_required
    def mutate(root, info, linkid):
        link_model = LinkObject._meta.model
        link_instance = db.session.query(link_model).filter_by(linkid=linkid).first()

        if not link_instance:
            raise Exception('Error: No link found with the provided linkid')

        db.session.delete(link_instance)
        db.session.commit()
        ok = True
        return DeleteLink(ok=ok)