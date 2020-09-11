import logging

from flask import Blueprint, render_template

routes_for_flask = Blueprint(
    'routes_for_flask', __name__, template_folder='templates')


@ routes_for_flask.route('/')
def main():
    logging.info('here')
    return render_template('index.html')
