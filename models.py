import logging
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
        'IEP_Mandate', back_populates='student')
    rules = db.relationship('Rule', back_populates='student')
    sessions = db.relationship('Session', back_populates='student')


@dataclass
class Therapist(db.Model):
    therapist_id: int = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    therapist_ref_id: str = db.Column(db.String(80), nullable=False)
    first_name: str = db.Column(db.String(120), nullable=False)
    last_name: str = db.Column(db.String(120), nullable=False)

    rules = db.relationship('Rule', back_populates='therapist')


@dataclass
class IepMandate(db.Model):

    iep_id: int = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    frequency: int = db.Column(db.Integer, nullable=False)
    duration: int = db.Column(db.Integer, nullable=False)
    group_size: int = db.Column(db.Integer, nullable=False)

    types = ('speech', 'OT', 'PT', 'Counseling')
    type_enum = Enum(*types, name="type")
    type: int = db.Column(type_enum, nullable=False)

    # TODO: figure out deletes

    student_id: int = db.Column(db.Integer, db.ForeignKey(
        'student.student_id'), nullable=False)
    student = db.relationship("Student", back_populates='student_iep_mandate')

    rules = db.relationship('Rule', back_populates='iep_mandate')


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
    therapist = db.relationship("Therapist", back_populates='rules')

    iep_id: int = db.Column(db.Integer, db.ForeignKey(
        'iep_mandate.iep_id'), nullable=False)
    ieps = db.relationship("IEP_Mandate", back_populates='rules')

    student_id: int = db.Column(db.Integer, db.ForeignKey(
        'student.student_id'), nullable=False)
    student = db.relationship("Student", back_populates='rules')

    sessions = db.relationship('session', back_populates='student')


@dataclass
class Session(db.Model):
    session_id = db.Column(
        db.Integer, primary_key=True, autoincrement=True)

    date: datetime.date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)

    duration: int = db.Column(db.Integer, nullable=False)

    attended: bool = db.Column(db.Boolean, nullable=False)
    notes: str = db.Column(db.String(500), nullable=True)

    # TODO: student id
    student_id: int = db.Column(db.Integer, db.ForeignKey(
        'student.student_id'), nullable=False)
    student = db.relationship("Student", back_populates='sessions')
    # TODO: rule id

    rule_id: int = db.Column(db.Integer, db.ForeignKey(
        'rule.rule_id'), nullable=False)
    rule = db.relationship("Rule", back_populates='sessions')
