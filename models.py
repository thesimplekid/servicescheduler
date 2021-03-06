import json
import logging
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta

from pytz import timezone

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum

db = SQLAlchemy()

tz = timezone('EST')

frequency = ('weekly', 'daily')
frequency_enum = Enum(*frequency, name='frequency')

locations = ('teletheraphy', 'in-person', 'in-classroom')
location_enum = Enum(*locations, name='location')

types = ('speech', 'OT', 'PT', 'Counseling')
type_enum = Enum(*types, name="type")


@dataclass
class Student(db.Model):
    student_id: int = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    osis_number: int = db.Column(db.Integer, nullable=False, unique=True)
    first_name: str = db.Column(db.String(120), nullable=False)
    last_name: str = db.Column(db.String(120), nullable=False)
    grade: str = db.Column(db.String(80), nullable=False)
    schoolDBN: str = db.Column(db.String(80), nullable=False)

    student_iep_mandate = db.relationship(
        'Iepmandate', back_populates='student')

    student_rules = db.relationship('Rule', back_populates='student')


'''
    student_sessions = db.relationship(
        'Session', back_populates='student_in_session')
'''


@dataclass
class Provider(db.Model):
    provider_id: int = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    provider_ref_id: str = db.Column(
        db.String(80), nullable=False, unique=True)
    first_name: str = db.Column(db.String(120), nullable=False)
    last_name: str = db.Column(db.String(120), nullable=False)

    provider_type: str = db.Column(type_enum, nullable=False)

    provider_rules = db.relationship('Rule', back_populates='provider')


@dataclass
class Iepmandate(db.Model):

    iep_id: int = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    frequency: int = db.Column(db.Integer, nullable=False)
    duration: int = db.Column(db.Integer, nullable=False)
    group_size: int = db.Column(db.Integer, nullable=False)

    type: str = db.Column(type_enum, nullable=False)

    # TODO: figure out deletes

    student_id: int = db.Column(db.Integer, db.ForeignKey(
        'student.student_id'), nullable=False)
    student = db.relationship("Student", back_populates='student_iep_mandate')

    iep_rules = db.relationship('Rule', back_populates='ieps')


@dataclass
class Rule(db.Model):

    rule_id: int = db.Column(
        db.Integer, primary_key=True, autoincrement=True)

    location: int = db.Column(location_enum, nullable=False)

    frequency: str = db.Column(frequency_enum, nullable=False)

    monday: bool = db.Column(db.Boolean, default=False, nullable=False)
    tuesday: bool = db.Column(db.Boolean, default=False, nullable=False)
    wednesday: bool = db.Column(db.Boolean, default=False, nullable=False)
    thursday: bool = db.Column(db.Boolean, default=False, nullable=False)
    friday: bool = db.Column(db.Boolean, default=False, nullable=False)

    interval: int = db.Column(db.Integer, nullable=False)

    start_date: datetime.date = db.Column(db.DateTime, nullable=False)
    end_date: datetime.date = db.Column(db.Date, nullable=False)

    duration: int = db.Column(db.Integer, nullable=False)

    provider_id: int = db.Column(db.Integer, db.ForeignKey(
        'provider.provider_id'), nullable=False)
    provider = db.relationship("Provider", back_populates='provider_rules')

    iep_id: int = db.Column(db.Integer, db.ForeignKey(
        'iepmandate.iep_id'), nullable=False)
    ieps = db.relationship("Iepmandate", back_populates='iep_rules')

    student_id: int = db.Column(db.Integer, db.ForeignKey(
        'student.student_id'), nullable=False)
    student = db.relationship("Student", back_populates='student_rules')


'''
    rule_sessions = db.relationship('Session', back_populates='rule')


@ dataclass
class Session(db.Model):
    session_id = db.Column(
        db.Integer, primary_key=True, autoincrement=True)

    date: datetime.date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)

    duration: int = db.Column(db.Integer, nullable=False)

    attended: bool = db.Column(db.Boolean, nullable=False)
    notes: str = db.Column(db.String(500), nullable=True)

    student_id: int = db.Column(db.Integer, db.ForeignKey(
        'student.student_id'), nullable=False)
    student_in_session = db.relationship(
        "Student", back_populates='student_sessions')

    rule_id: int = db.Column(db.Integer, db.ForeignKey(
        'rule.rule_id'), nullable=False)
    rule = db.relationship("Rule", back_populates='rule_sessions')
'''


def tup_to_choices(tup_name):
    result = []
    [result.append((i, i)) for i in tup_name]
    return result


def provider_choices():
    result = []
    all = Provider.query.with_entities(
        Provider.provider_id, Provider.first_name, Provider.last_name).all()
    [result.append((i[0], i[1] + " " + i[2])) for i in all]
    return result


def insert_student(osis_number_passed, first_name_passed, last_name_passed, grade_passed, schoolDBN_passed):
    if(db.session.query(Student.osis_number).filter_by(osis_number=osis_number_passed).scalar() is None):

        new_student = Student(osis_number=osis_number_passed, first_name=first_name_passed,
                              last_name=last_name_passed, grade=grade_passed, schoolDBN=schoolDBN_passed)
        db.session.add(new_student)
        db.session.commit()
    else:
        logging.info('Student already exisits')


def insert_provider(provider_ref_id_passed, first_name_passed, last_name_passed, provider_type_passed):
    if (db.session.query(Provider.provider_ref_id).filter_by(provider_ref_id=provider_ref_id_passed).scalar() is None):

        new_provider = Provider(provider_ref_id=provider_ref_id_passed,
                                first_name=first_name_passed, last_name=last_name_passed, provider_type=provider_type_passed)
        db.session.add(new_provider)
        db.session.commit()
    else:
        logging.info('Provider already exists')


def insert_iepmandate(frequency_passed, duration_passed, group_size_passed, type_passed, student_id_passed):
    new_iep = Iepmandate(frequency=frequency_passed, duration=duration_passed,
                         group_size=group_size_passed, type=type_passed, student_id=student_id_passed)
    db.session.add(new_iep)
    db.session.commit()


def insert_rule(location_passed, interval_passed, frequency_passed, start_date_passed, end_date_passed, provider_id_passed, iep_id_passed, student_id_passed, duration_passed, monday_passed, tuesday_passed, wednesday_passed, thursday_passed, friday_passed):
    new_rule = Rule(location=location_passed, interval=interval_passed, frequency=frequency_passed, start_date=start_date_passed,
                    end_date=end_date_passed, provider_id=provider_id_passed, iep_id=iep_id_passed, student_id=student_id_passed, duration=duration_passed, monday=monday_passed, tuesday=tuesday_passed, wednesday=wednesday_passed, thursday=thursday_passed, friday=friday_passed)
    db.session.add(new_rule)
    db.session.commit()


def insert_session(date_passed, start_time_passed, end_time_passed, duration_passed, attended_passed, notes_passed, student_id_passed, rule_id_passed):
    new_session = Session(date=date_passed, start_time=start_time_passed, end_time=end_time_passed, duration=duration_passed,
                          attended=attended_passed, notes=notes_passed, student_id=student_id_passed, rule_id=rule_id_passed)
    db.session.add(new_session)
    db.session.commit()


def get_all_students():
    result = []
    all = db.session.query(Student).all()
    [result.append(asdict(row)) for row in all]
    return result


def get_student_by_id(student_id_passed):
    student = Student.query.filter_by(student_id=student_id_passed).first()
    return student


def get_iep_by_id(iep_id_passed):
    iep = Iepmandate.query.filter_by(iep_id=iep_id_passed).first()
    return iep


def get_rule_by_id(rule_id_passed):
    rule = Rule.query.filter_by(rule_id=rule_id_passed).first()
    return rule


def get_provider_by_id(provider_id_passed):
    provider = Provider.query.filter_by(provider_id=provider_id_passed).first()
    return provider


def get_student_id_from_iep(iep_id_passed):
    logging.info(iep_id_passed)
    iep = get_iep_by_id(iep_id_passed)
    logging.info(iep)
    return iep.student_id


def get_all_providers():
    result = []
    all = db.session.query(Provider).all()
    [result.append(asdict(row)) for row in all]
    return result


def get_iep_for_student(student_id_passed):
    result = []
    all = Iepmandate.query.filter_by(student_id=student_id_passed).all()
    [result.append(asdict(row)) for row in all]
    return result


def get_student_info(student_id_passed):
    student = Student.query.filter_by(student_id=student_id_passed).first()
    return asdict(student)


def get_provider_info(provider_id_passed):
    provider = Provider.query.filter_by(provider_id=provider_id_passed).first()
    return asdict(provider)


def get_rules_for_iep(mandate_id_passed):
    result = []
    rules = Rule.query.filter_by(iep_id=mandate_id_passed).all()
    [result.append(asdict(row)) for row in rules]
    return result


def get_rules_for_student(student_id):
    result = []
    student = get_student_by_id(student_id)
    rules = student.student_rules
    [result.append(asdict(row)) for row in rules]
    return result


def get_rules_for_provider(provider_id):
    result = []
    provider = get_provider_by_id(provider_id)
    rules = provider.provider_rules
    [result.append(asdict(row)) for row in rules]
    return result


def get_rules_by_type(type_passed):
    result = []
    rules = Rule.query.filter(Rule.ieps.has(type=type_passed)).all()
    [result.append(asdict(row)) for row in rules]
    return result


def get_event_titile(iep_id):
    result = []
    iep = get_iep_by_id(iep_id)
    type = iep.type
    freq = iep.frequency
    dur = iep.duration
    group_size = iep.group_size

    return type + " " + str(freq) + "x" + str(dur) + "x" + str(group_size)


def update_rule(rule_id, start_time, end_day):
    start_time = start_time.replace(
        " GMT-0400 (Eastern Daylight Time)", "")[:-3]

    start_datetime = datetime.strptime(start_time, "%a %b %d %Y %H:%M")

    end_day = end_day.replace(
        " GMT-0400 (Eastern Daylight Time)", "")[:-9]
    end_date = datetime.strptime(end_day, "%a %b %d %Y")
    logging.info(end_date)

    rule = get_rule_by_id(rule_id)
    logging.info(rule)
    rule.start_date = start_datetime
    #rule.end_date = end_date
    db.session.commit()


def rules_to_json(li_dics):
    # return json for the calander view
    result = []

    for dic in li_dics:
        event_dic = {}
        rrule_dic = {}
        extendedProps_dic = {}
        day_li = []

        if dic['monday'] == True:
            day_li.append('mo')
        if dic['tuesday'] == True:
            day_li.append('tu')
        if dic['wednesday'] == True:
            day_li.append('we')
        if dic['thursday'] == True:
            day_li.append('th')
        if dic['friday'] == True:
            day_li.append('fr')

        rrule_dic['dtstart'] = dic['start_date'].strftime("%Y-%m-%dT%H:%M:%S")
        rrule_dic['until'] = dic['end_date'].strftime("%Y-%m-%d")
        rrule_dic['byweekday'] = day_li
        rrule_dic['interval'] = dic['interval']
        rrule_dic['freq'] = dic['frequency']

        extendedProps_dic['location'] = dic['location']
        extendedProps_dic['iep_id'] = dic['iep_id']
        extendedProps_dic['student_id'] = dic['student_id']

        event_dic['title'] = get_event_titile(dic['iep_id'])

        duration_string = str(timedelta(minutes=dic['duration']))[:-3]
        duration = datetime.strptime(
            duration_string, "%H:%M").strftime('%H:%M')
        event_dic['duration'] = duration
        event_dic['editable'] = True

        event_dic['id'] = dic['rule_id']
        event_dic['groupId'] = dic['rule_id']
        event_dic['rrule'] = rrule_dic
        event_dic['extendedProps'] = extendedProps_dic

        result.append(event_dic)
    return (result)


def rules_for_student_to_json(student_id):
    li_dics = get_rules_for_student(student_id)
    return rules_to_json(li_dics)


def rules_for_provider_to_json(provider_id):

    li_dics = get_rules_for_provider(provider_id)

    return rules_to_json(li_dics)


def rules_by_type_to_json(type_passed):
    li_dic = get_rules_by_type(type_passed)
    return rules_to_json(li_dic)


def populate():
    insert_student(88, 'Jack', 'Murphy', 'pre-k', '127Q2')
    insert_student(99, 'Brendan', 'Murphy', '1', '9674q')

    insert_provider(74783, 'Caroline', 'Murphy', 'speech')
    insert_provider(7646783, "tom", 'Murphy', 'ot')

    insert_iepmandate(5, 65, 2, 'speech', 1)
    insert_iepmandate(2, 45, 1, 'PT', 2)

    insert_rule('in-person', 2, 'weekly', datetime(2020, 5, 17, 8,
                                                   15), datetime(2021, 6, 17), 1, 1, 1, 45, True, True, False, False, False)

    insert_rule('teletheraphy', 1, 'daily', datetime(
        2020, 6, 18, 13, 00), datetime(2021, 7, 17), 2, 2, 2, 45, True, False, False, True, False)


'''
    insert_session(datetime(2020, 7, 17), timers,
                   timers, 77, True, 'hi', 1, 1)
    insert_session(datetime(2020, 7, 18), timers,
                   timers, 77, False, 'hi', 2, 2)

'''
