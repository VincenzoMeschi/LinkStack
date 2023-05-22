import graphene
from database.models.link import LinkObject
from app import db
from flask_graphql_auth import mutation_header_jwt_required


class CreateLink(graphene.Mutation):
    class Arguments:
        linkhttp = graphene.String(required=True)
        linkplatform = graphene.String(required=True)
        linknickname = graphene.String(required=True)
        linktitle = graphene.String(required=True)
        linkdesc = graphene.String(required=True)
        stackid = graphene.String(required=True)

    ok = graphene.Boolean()
    link = graphene.Field(lambda: LinkObject)

    @mutation_header_jwt_required
    def mutate(root, info, linkhttp, linkplatform, linknickname, linktitle, linkdesc, stackid):
        link_model = LinkObject._meta.model
        link_instance = link_model(linkhttp=linkhttp, linkplatform=linkplatform, linknickname=linknickname, linktitle=linktitle, linkdesc=linkdesc, stackid=stackid)
        db.session.add(link_instance)
        db.session.commit()
        ok = True
        return CreateLink(link=link_instance, ok=ok)