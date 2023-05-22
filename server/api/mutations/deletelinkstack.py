import graphene
from database.models.linkstack import LinkStackObject
from app import db
from flask_graphql_auth import mutation_header_jwt_required


class DeleteLinkStack(graphene.Mutation):
    class Arguments:
        stackid = graphene.String(required=True)

    ok = graphene.Boolean()

    @mutation_header_jwt_required
    def mutate(root, info, stackid):
        linkstack_model = LinkStackObject._meta.model
        linkstack_instance = db.session.query(linkstack_model).filter_by(stackid=stackid).first()

        if not linkstack_instance:
            raise Exception('Error: No linkstack found with the provided stackid')

        db.session.delete(linkstack_instance)
        db.session.commit()
        ok = True
        return DeleteLinkStack(ok=ok)