from flask import Flask
from appconfig import AppConfig

app = Flask(__name__)
config = AppConfig(app)

config.init_cors()
db = config.init_db(app)
config.init_auth()
config.init_graphql(app, db)

if __name__ == '__main__':
  app.run(debug=True)
