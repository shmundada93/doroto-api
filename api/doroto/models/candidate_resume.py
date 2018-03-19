from flask import url_for, current_app
from ..exceptions import ValidationError
from ..utils import split_url
from . import Base
from .. import db

class CandidateResume(Base):
    __tablename__ = "candidate_resumes"
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidates.id'), index=True)
    resume_name = db.Column(db.String(256))
    resume_url = db.Column(db.String(256))
    redacted_resume_url = db.Column(db.String(256))
    jobs = db.relationship('JobRecruiterCandidate', backref='candidate_resume', lazy='dynamic')