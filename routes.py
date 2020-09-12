import logging

from flask import Blueprint, render_template

routes_for_flask = Blueprint(
    'routes_for_flask', __name__, template_folder='templates')

bp = Blueprint('errors', __name__)


@ routes_for_flask.route('/')
def main():
    logging.info('in routes main')
    return render_template('index.html')


@ routes_for_flask.route('/testcalendar')
def testcalendar():
    logging.info('in routes/testcalendar')
    return render_template('testcalendar.html')


@ routes_for_flask.route('/students')
def student_view():
    logging.info('in routes/student_view')
    return render_template('student/view.html')


@ routes_for_flask.route('/student/create')
def student_create():
    logging.info('in routes/student_create')
    return render_template('student/create.html')


@bp.app_errorhandler(404)
def handle_404(err):
    logging.info('in handle_404')
    return render_template('404.html'), 404
