from flask import url_for, current_app
from ..exceptions import ValidationError
from ..utils import split_url
from . import Base
from .. import db

class Recruiter(Base):
    __tablename__ = "recruiters"
    name = db.Column(db.String(256))
    address = db.Column(db.Text)
    description = db.Column(db.Text)
    phone = db.Column(db.String(256))
    status = db.Column(db.String(256))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    user = db.relationship('User', lazy=True)
    job_recruiters = db.relationship('JobRecruiter', backref='recruiter', lazy='dynamic')