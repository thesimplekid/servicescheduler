import logging

import config
import models
from flask import Flask
from routes import routes_for_flask

logging.basicConfig(filename='app.log',
                    format='[%(filename)s:%(lineno)d] %(message)s', level=logging.DEBUG)
logging.warning("New Run Starts Here")


def create_app():
    username = 'newuser'
    password = 'newpassword'
    location = 'mysql'
    dbname = 'test_db'
    app = Flask(__name__)
    app.register_blueprint(routes_for_flask)
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{username}:{password}@{location}:3306/{dbname}?charset=utf8mb4"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # Shows sql querys being made if having database issue set to true
    app.config['SQLALCHEMY_ECHO'] = True
    app.secret_key = 'dfghjfdfcghjk'
    models.db.init_app(app)
    return app


app = create_app()
app.app_context().push()
models.db.create_all()
# models.populate()
# app.run()
