import logging
from datetime import datetime

import forms
import models
import json
from flask import Blueprint, jsonify, redirect, render_template, request

routes_for_flask = Blueprint(
    'routes_for_flask', __name__, template_folder='templates')


@ routes_for_flask.route('/')
def main():
    logging.info('in routes main')
    logging.info(models.get_iep_by_id(1))
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
    form = forms.add_student()

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('student/create.html', form=form)
        else:
            models.insert_student(
                form.osis_number.data, form.first_name.data, form.last_name.data, form.grade.data, form.schoolDBN.data)
            return redirect('/students')
    else:
        return render_template('student/create.html', form=form)


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


@routes_for_flask.route('/provider/new', methods=['GET', 'POST'])
def new_provider():
    form = forms.add_provider()

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('provider/create.html', form=form)
        else:
            models.insert_provider(
                form.provider_ref_id.data, form.first_name.data, form.last_name.data)
            return redirect('/providers')

    else:
        return render_template('provider/create.html', form=form)


@routes_for_flask.route('/iep')
def iep_student():
    student_id = request.args.get('student_id')
    data = models.get_iep_for_student(student_id)
    return jsonify(data)


@routes_for_flask.route('/rules')
def rules_for_iep():
    mandate_id = request.args.get('mandate_id')
    data = models.get_rules_for_iep(mandate_id)
    return jsonify(data)


@routes_for_flask.route('/rule/new', methods=['GET', 'POST'])
def add_rule():
    iep_id = request.args.get('iep_id')

    form = forms.add_rule()
    if request.method == 'POST':
        iep_id = form.iep_id.data
        student_id = models.get_student_id_from_iep(iep_id)
        monday_b = True if 'monday' in form.days.data else False
        tuesday_b = True if 'tuesday' in form.days.data else False
        wednesday_b = True if 'wednesday' in form.days.data else False
        thursday_b = True if 'thursday' in form.days.data else False
        friday_b = True if 'friday' in form.days.data else False

        start_date = form.start_date.data
        start_time = form.start_time.data

        time = start_time.split(':')

        start_datetime = datetime(
            start_date.year, start_date.month, start_date.day, int(time[0]), int(time[1]))
        logging.info(start_datetime)

        models.insert_rule(form.location.data, form.interval.data, form.frequency.data, start_datetime, form.end_date.data,
                           form.provider.data, form.iep_id.data, student_id, form.duration.data, monday_b, tuesday_b, wednesday_b, thursday_b, friday_b)

        return redirect('/students')
    else:
        form.iep_id.data = iep_id
        form.location.choices = models.tup_to_choices(models.locations)
        form.frequency.choices = models.tup_to_choices(models.frequency)
        form.provider.choices = models.provider_choices()
        return render_template('rule/create.html', form=form)


@routes_for_flask.route('/rule/move', methods=['POST'])
def move_rule():
    logging.info(request.values.get('id'))
    logging.info(type(request.values.get('start')))
    logging.info(request.values.get('end'))


@routes_for_flask.route('/rules/student')
def rules_for_student():
    student_id = request.args.get('student_id')
    result = models.rules_for_student_tojson(student_id)
    string = result
    return jsonify(string)


@routes_for_flask.app_errorhandler(404)
def handle_404(err):
    logging.info('in handle_404')
    return render_template('404.html'), 404
