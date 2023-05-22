import graphene
from api.queries.queries import Query
from api.mutations.mutation import Mutation

schema = graphene.Schema(query=Query, mutation=Mutation)