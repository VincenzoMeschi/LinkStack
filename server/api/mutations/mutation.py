import graphene

from api.mutations.createuser import CreateUser
from api.mutations.userlogin import UserLogin
from api.mutations.createlink import CreateLink
from api.mutations.updatelink import UpdateLink
from api.mutations.createlinkstack import CreateLinkStack
from api.mutations.updatelinkstack import UpdateLinkStack
from api.mutations.changepassword import ChangePassword
from api.mutations.deletelink import DeleteLink
from api.mutations.deletelinkstack import DeleteLinkStack


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    user_login = UserLogin.Field()
    create_link = CreateLink.Field()
    update_link = UpdateLink.Field()
    create_link_stack = CreateLinkStack.Field()
    update_link_stack = UpdateLinkStack.Field()
    change_password = ChangePassword.Field()
    delete_link = DeleteLink.Field()
    delete_link_stack = DeleteLinkStack.Field()