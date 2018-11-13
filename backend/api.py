import responder
import graphene

api = responder.API()


@api.route("/")
async def hello(req, resp):
    resp.text = "hello, world!"


class Query(graphene.ObjectType):
    hello = graphene.String(name=graphene.String(default_value="stranger"))

    def resolve_hello(self, info, name):
        return f"Hello {name}"


schema = graphene.Schema(query=Query)
view = responder.ext.GraphQLView(api=api, schema=schema)

api.add_route("/graph", view)

if __name__ == "__main__":
    api.run()
