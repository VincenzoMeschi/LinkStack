import graphene
from app import db
from database.models.link import LinkObject
from flask_graphql_auth import mutation_header_jwt_required


class UpdateLink(graphene.Mutation):
    class Arguments:
        linkid = graphene.String(required=True)
        linkhttp = graphene.String()
        linkplatform = graphene.String()
        linknickname = graphene.String()
        linktitle = graphene.String()
        linkdesc = graphene.String()
        stackid = graphene.String()

    ok = graphene.Boolean()
    link = graphene.Field(lambda: LinkObject)

    @mutation_header_jwt_required
    def mutate(root, info, linkid, linkhttp=None, linkplatform=None, linknickname=None, linktitle=None, linkdesc=None, stackid=None):
        link_model = LinkObject._meta.model
        link_instance = db.session.query(link_model).filter_by(linkid=linkid).first()

        if not link_instance:
            print('Error: No link found with the provided linkid')

        if linkhttp:
            link_instance.linkhttp = linkhttp
        if linkplatform:
            link_instance.linkplatform = linkplatform
        if linknickname:
            link_instance.linknickname = linknickname
        if linktitle:
            link_instance.linktitle = linktitle
        if linkdesc:
            link_instance.linkdesc = linkdesc
        if stackid:
            link_instance.stackid = stackid

        db.session.commit()
        ok = True
        return UpdateLink(link=link_instance, ok=ok)