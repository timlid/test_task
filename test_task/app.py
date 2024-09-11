from flask import Flask
import database
import routes 
from dotenv import load_dotenv, find_dotenv

import config

load_dotenv(find_dotenv())

app = Flask(__name__)
app.config.from_object(config.AppConfig)
app.register_blueprint(routes.api)

database.db.init_app(app)
database.migrate.init_app(app, database.db)
