from flask import url_for, current_app
from ..exceptions import ValidationError
from ..utils import split_url
from . import Base
from .. import db

class JobRecruiterCandidate(Base):
    __tablename__ = "job_recruiter_candidate"
    job_recruiter_id = db.Column(db.Integer, db.ForeignKey('job_recruiter.id'), index=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidates.id'), index=True)
    candidate_resume_id = db.Column(db.Integer, db.ForeignKey('candidate_resumes.id'), index=True)
    submitted = db.Column(db.Boolean)
    status = db.Column(db.String(256))