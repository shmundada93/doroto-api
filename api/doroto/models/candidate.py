from flask import url_for, current_app
from ..exceptions import ValidationError
from ..utils import split_url
from . import Base
from .. import db

class Candidate(Base):
    __tablename__ = "candidates"
    name = db.Column(db.String(256))
    phone = db.Column(db.String(256))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    user = db.relationship('User', lazy=True)
    resumes = db.relationship('CandidateResume', backref='candidate', lazy='dynamic')
    jobs = db.relationship('JobRecruiterCandidate', backref='candidate', lazy='dynamic')
