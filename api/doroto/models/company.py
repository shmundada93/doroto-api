from flask import url_for, current_app
from ..exceptions import ValidationError
from ..utils import split_url
from . import Base
from .. import db

class Company(Base):
    __tablename__ = "companies"
    name = db.Column(db.String(256))
    activation_status = db.Column(db.String(256))
    address = db.Column(db.Text)
    description = db.Column(db.Text)
    phone = db.Column(db.String(256))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    user = db.relationship('User', lazy=True)
    jobs = db.relationship('Job', backref='company', lazy='dynamic')

    def get_url(self):
        return url_for('api.get_company', id=self.id, _external=True)