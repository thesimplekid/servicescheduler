
import logging

from flask import Flask
from routes import routes_for_flask

logging.basicConfig(filename='app.log',
                    format='[%(filename)s:%(lineno)d] %(message)s', level=logging.DEBUG)
logging.warning("New Run Starts Here")


def create_app():
    app = Flask(__name__)
    app.register_blueprint(routes_for_flask)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
