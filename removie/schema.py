import graphene
import app.schema


class Mutation(app.schema.Mutation, graphene.ObjectType):
    pass


class Query(app.schema.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query,mutation=Mutation)
