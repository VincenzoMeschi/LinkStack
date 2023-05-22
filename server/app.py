from flask import Flask
from flask_graphql import GraphQLView
from flask_config import app, schema

app.add_url_rule(
    "/graphql",
    view_func=GraphQLView.as_view(
        "graphql",
        schema=schema,
        graphiql=True,
        get_context=lambda: {"session": app.db.session},
    ),
)

if __name__ == "__main__":
    app.run(debug=True)
