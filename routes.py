import logging

import models
from flask import Blueprint, jsonify, render_template, request

routes_for_flask = Blueprint(
    'routes_for_flask', __name__, template_folder='templates')


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


@routes_for_flask.route('/student/new', methods=['GET', 'POST'])
def new_student():
    logging.info('hi')


@routes_for_flask.route('/student/<int:id>')
def student_info(id):
    data = models.get_student_info(id)
    logging.info(data)
    return render_template('student/read.html', data=data)


@ routes_for_flask.route('/students/json')
def student_json():
    data = models.get_all_students()
    return jsonify(data)


@ routes_for_flask.route('/student/create')
def student_create():
    logging.info('in routes/student_create')
    return render_template('student/create.html')


@routes_for_flask.route('/providers')
def provider_view():
    return render_template('provider/view.html')


@routes_for_flask.route('/providers/json')
def provider_json():
    data = models.get_all_providers()
    return jsonify(data)


@routes_for_flask.route('/iep')
def iep_student():
    student_id = request.args.get('student_id')
    data = models.get_iep_for_student(student_id)
    return jsonify(data)


@routes_for_flask.app_errorhandler(404)
def handle_404(err):
    logging.info('in handle_404')
    return render_template('404.html'), 404
