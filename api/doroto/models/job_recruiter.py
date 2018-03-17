from flask import url_for, current_app
from ..exceptions import ValidationError
from ..utils import split_url
from . import Base
from .. import db

class JobRecruiter(Base):
    __tablename__ = "job_recruiter"
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), index=True)
    recruiter_id = db.Column(db.Integer, db.ForeignKey('recruiters.id'), index=True)
    resume_limit = db.Column(db.Integer)
    status = db.Column(db.String(256))
    guid = db.Column(db.String(256), index=True)
