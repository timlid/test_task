from flask import Flask
import database
import routes 

import config

app = Flask(__name__)
app.config.from_object(config.app_config)
app.register_blueprint(routes.api)

database.db.init_app(app)
database.migrate.init_app(app, database.db)
