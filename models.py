import json
import logging
import time
from dataclasses import asdict, dataclass
from datetime import datetime

from pytz import timezone

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum

db = SQLAlchemy()

tz = timezone('EST')


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

    student_sessions = db.relationship(
        'Session', back_populates='student_in_session')


@dataclass
class Therapist(db.Model):
    therapist_id: int = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    therapist_ref_id: str = db.Column(db.String(80), nullable=False)
    first_name: str = db.Column(db.String(120), nullable=False)
    last_name: str = db.Column(db.String(120), nullable=False)

    therapist_rules = db.relationship('Rule', back_populates='therapist')


@dataclass
class Iepmandate(db.Model):

    iep_id: int = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    frequency: int = db.Column(db.Integer, nullable=False)
    duration: int = db.Column(db.Integer, nullable=False)
    group_size: int = db.Column(db.Integer, nullable=False)

    types = ('speech', 'OT', 'PT', 'Counseling')
    type_enum = Enum(*types, name="type")
    type: str = db.Column(type_enum, nullable=False)

    # TODO: figure out deletes

    student_id: int = db.Column(db.Integer, db.ForeignKey(
        'student.student_id'), nullable=False)
    student = db.relationship("Student", back_populates='student_iep_mandate')

    iep_rules = db.relationship('Rule', back_populates='ieps')


@dataclass
class Rule(db.Model):

    rule_id = db.Column(
        db.Integer, primary_key=True, autoincrement=True)

    locations = ('teletheraphy', 'in-person', 'in-classroom')
    location_enum = Enum(*locations, name='location')

    location: int = db.Column(location_enum, nullable=False)

    intervals = ('weekly', 'daily')
    interval_enum = Enum(*intervals, name='interval')
    interval: int = db.Column(interval_enum, nullable=False)

    days = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday')
    days_enum = Enum(*days, name='day')
    day: int = db.Column(days_enum, nullable=False)

    repeats: int = db.Column(db.Integer, nullable=False)

    start_date: datetime.date = db.Column(db.Date, nullable=False)
    end_date: datetime.date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)

    therapist_id: int = db.Column(db.Integer, db.ForeignKey(
        'therapist.therapist_id'), nullable=False)
    therapist = db.relationship("Therapist", back_populates='therapist_rules')

    iep_id: int = db.Column(db.Integer, db.ForeignKey(
        'iepmandate.iep_id'), nullable=False)
    ieps = db.relationship("Iepmandate", back_populates='iep_rules')

    student_id: int = db.Column(db.Integer, db.ForeignKey(
        'student.student_id'), nullable=False)
    student = db.relationship("Student", back_populates='student_rules')

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


def insert_student(osis_number_passed, first_name_passed, last_name_passed, grade_passed, schoolDBN_passed):
    new_student = Student(osis_number=osis_number_passed, first_name=first_name_passed,
                          last_name=last_name_passed, grade=grade_passed, schoolDBN=schoolDBN_passed)
    db.session.add(new_student)
    db.session.commit()


def insert_therapist(therapist_ref_id_passed, first_name_passed, last_name_passed):
    new_therapist = Therapist(therapist_ref_id=therapist_ref_id_passed,
                              first_name=first_name_passed, last_name=last_name_passed)
    db.session.add(new_therapist)
    db.session.commit()


def insert_iepmandate(frequency_passed, duration_passed, group_size_passed, type_passed, student_id_passed):
    new_iep = Iepmandate(frequency=frequency_passed, duration=duration_passed,
                         group_size=group_size_passed, type=type_passed, student_id=student_id_passed)
    db.session.add(new_iep)
    db.session.commit()


def insert_rule(location_passed, interval_passed, day_passed, repeats_passed, start_date_passed, end_date_passed, start_time_passed, therapist_id_passed, iep_id_passed, student_id_passed):
    new_rule = Rule(location=location_passed, interval=interval_passed, day=day_passed, repeats=repeats_passed, start_date=start_date_passed,
                    end_date=end_date_passed, start_time=start_time_passed, therapist_id=therapist_id_passed, iep_id=iep_id_passed, student_id=student_id_passed)
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


def get_iep_for_student(student_id_passed):
    result = []
    all = Iepmandate.query.filter_by(student_id=student_id_passed).all()
    [result.append(asdict(row)) for row in all]
    return result


def get_student_info(student_id_passed):
    result = []
    student = Student.query.filter_by(student_id=student_id_passed).first()
    return asdict(student)


def populate():
    insert_student(88, 'Jack', 'Murphy', 'pre-k', '127Q2')
    insert_student(99, 'Brendan', 'Murphy', '1', '9674q')

    insert_therapist(74783, 'Caroline', 'Murphy')
    insert_therapist(7646783, "tom", 'Murphy')

    insert_iepmandate(5, 65, 2, 'speech', 1)
    insert_iepmandate(2, 45, 1, 'PT', 2)
    currentDT = datetime.now()
    timers = currentDT.strftime("%H:%M")

    insert_rule('in-person', 'weekly', 'Monday', 2, datetime(2020,
                                                             5, 17), datetime(2020, 6, 17), timers, 1, 1, 1)

    insert_rule('teletheraphy', 'daily', 'Tuesday', 2, datetime(
        2020, 6, 18), datetime(2020, 7, 17), timers, 2, 2, 2)

    insert_session(datetime(2020, 7, 17), timers,
                   timers, 77, True, 'hi', 1, 1)
    insert_session(datetime(2020, 7, 18), timers,
                   timers, 77, False, 'hi', 2, 2)
