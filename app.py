import logging

import models
from flask import Flask
from routes import routes_for_flask

logging.basicConfig(filename='app.log',
                    format='[%(filename)s:%(lineno)d] %(message)s', level=logging.DEBUG)
logging.warning("New Run Starts Here")


def create_app():
    app = Flask(__name__)
    app.register_blueprint(routes_for_flask)
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://user:pavgncbrs1wvrd0r@db-mysql-nyc1-43883-do-user-7668124-0.b.db.ondigitalocean.com:25060/defaultdb?"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # Shows sql querys being made if having database issue set to true
    app.config['SQLALCHEMY_ECHO'] = True
    models.db.init_app(app)
    return app


if __name__ == "__main__":
    app = create_app()
    app.app_context().push()
    models.db.create_all()
    app.run()
