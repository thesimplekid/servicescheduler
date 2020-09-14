from flask_wtf import FlaskForm
from wtforms import (HiddenField, IntegerField, SelectField,
                     SelectMultipleField, StringField, SubmitField, validators,
                     widgets)
from wtforms.fields.html5 import DateField


class add_student(FlaskForm):
    osis_number = IntegerField('Enter Osis Number', [validators.Required()])
    first_name = StringField('Enter first name', [validators.Required()])
    last_name = StringField('Enter last name', [validators.Required()])
    grade = StringField('Enter grade', [validators.Required()])
    schoolDBN = StringField('Enter schoolDBN', [validators.Required()])
    submit = SubmitField('Submit')


class add_provider(FlaskForm):
    provider_ref_id = StringField('Enter ref id', [validators.Required()])
    first_name = StringField('Enter first name', [validators.Required()])
    last_name = StringField('Enter last name', [validators.Required()])
    provider_type = SelectField('Select a Provider type')
    submit = SubmitField('Submit')


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class add_rule(FlaskForm):
    iep_id = HiddenField('Iep ID')
    student_id = HiddenField('student_id')
    location = SelectField('Choose a location')
    frequency = SelectField('Enter a frequency(string)')
    interval = IntegerField('Enter a Interval (int)')
    start_date = DateField('Enter start date', [validators.Required()])
    start_time = StringField('Enter start field (str 00:00)')
    end_date = DateField('Enter end date', [validators.Required()])
    duration = IntegerField('Enter duration')
    provider = SelectField('Select a Provider')
    days = MultiCheckboxField('Select Days', choices=[
        ('monday', 'Monday'), ('tuesday', 'Tuesday'), ('wednesday', 'Wednesday'), ('thursday', 'Thursday'), ('friday', 'Friday')])

    submit = SubmitField('Submit')
