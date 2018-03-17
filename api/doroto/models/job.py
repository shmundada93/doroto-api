from flask import url_for, current_app
from ..exceptions import ValidationError
from ..utils import split_url
from . import Base
from .. import db

class Job(Base):
    __tablename__ = "jobs"
    title = db.Column(db.String(256))
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), index=True)
    job_description = db.Column(db.Text)
    recruiter_description = db.Column(db.Text)
    questions = db.Column(db.Text)
    open_positions = db.Column(db.Integer)
    status = db.Column(db.String(256))
    position_id = db.Column(db.Integer, db.ForeignKey('position_types.id'), index=True)
    job_recruiters = db.relationship('JobRecruiter', backref='job', lazy='dynamic')
