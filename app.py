import logging

import config
import models
from flask import Flask
from routes import routes_for_flask

logging.basicConfig(filename='app.log',
                    format='[%(filename)s:%(lineno)d] %(message)s', level=logging.DEBUG)
logging.warning("New Run Starts Here")


def create_app():
    app = Flask(__name__)
    app.register_blueprint(routes_for_flask)
    app.config['SQLALCHEMY_DATABASE_URI'] = config.database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # Shows sql querys being made if having database issue set to true
    app.config['SQLALCHEMY_ECHO'] = True
    models.db.init_app(app)
    return app


if __name__ == "__main__":
    app = create_app()
    app.app_context().push()
    models.db.create_all()
    # models.populate()
    app.run()
