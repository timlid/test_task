from flask import Flask
import database

import config

app = Flask(__name__)
app.config.from_object(config.app_config)

database.db.init_app(app)
database.migrate.init_app(app, database.db)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
