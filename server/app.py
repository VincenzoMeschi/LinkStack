from flask import Flask
from flask_cors import CORS
from flask_graphql import GraphQLView
from api.schema import schema
from database.model import db



app = Flask(__name__)

CORS(app, resources={r"/graphql": {"origins": ["http://localhost:3000", "https://studio.apollographql.com"]}}, supports_credentials=True, allow_headers=['Content-Type', 'Authorization'])

app.add_url_rule(
  "/graphql",
  view_func=GraphQLView.as_view(
      "graphql",
      schema=schema,
      graphiql=True,
      get_context=lambda: {'session': db},
  )
)

if __name__ == '__main__':
  app.run(debug=True)