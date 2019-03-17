from graphene import Schema,ObjectType
import graphql_jwt
from graphene_django_extras import all_directives
import ingredients.extras,ingredients.relay
import recipes.relay
from .relay import Query as user_query,Mutation as user_mutation

class Query(ingredients.extras.Query,ingredients.relay.Query, recipes.relay.Query, user_query, ObjectType):
   pass

class Mutation(user_mutation,ingredients.relay.Mutation,ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

schema=Schema(query=Query,mutation=Mutation,directives=all_directives)