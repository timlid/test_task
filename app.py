from flask import Flask

import config

app = Flask(__name__)
app.config.from_object(config.app_config)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
