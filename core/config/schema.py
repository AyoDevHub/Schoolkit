import strawberry 

from accounts.graphql.queries import UserQuery
from accounts.graphql.mutations import UserMutation


@strawberry.type
class Query(UserQuery):
    pass


@strawberry.type
class Mutation(UserMutation):
    pass


schema = strawberry.Schema(
    query=Query, 
    mutation=Mutation
    )