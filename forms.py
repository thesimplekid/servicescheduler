from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField, validators


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
    submit = SubmitField('Submit')
