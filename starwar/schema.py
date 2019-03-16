import graphene
import graphql_jwt
import ingredients.relay
import recipes.relay

class Query(ingredients.relay.Query, recipes.relay.Query, graphene.ObjectType):
    pass

class Mutation(ingredients.relay.Mutation, graphene.ObjectType):
    pass

schema=graphene.Schema(query=Query,mutation=Mutation)