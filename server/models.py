from flask_sqlalchemy import SQLAlchemy
from graphene_sqlalchemy import SQLAlchemyObjectType
import datetime

db = SQLAlchemy()

class LinkObject(SQLAlchemyObjectType):
    class Meta:
        model = Base.classes.link

class LinkStackObject(SQLAlchemyObjectType):
    links = graphene.List(LinkObject)

    class Meta:
        model = Base.classes.linkstack

    def resolve_links(self, info):
        link_query = LinkObject.get_query(info)
        return link_query.filter_by(stackid=self.stackid).all()

class UserObject(SQLAlchemyObjectType):
    linkstacks = graphene.List(LinkStackObject)

    class Meta:
        model = Base.classes.appuser

    def resolve_linkstacks(self, info):
        linkstack_query = LinkStackObject.get_query(info)
        return linkstack_query.filter_by(useremail=self.useremail).all()

class PasswordObject(SQLAlchemyObjectType):
    class Meta:
        model = Base.classes.password

def initialize_models(app):
    db.init_app(app)
    Base.prepare(db.engine, reflect=True)
