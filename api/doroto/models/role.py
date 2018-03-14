from flask import url_for, current_app
from ..exceptions import ValidationError
from ..utils import split_url
from . import Base
from .. import db

class Role(Base):
    __tablename__ = 'roles'
    name = db.Column(db.String(64), index=True)
    users = db.relationship('User', backref='role', lazy='dynamic')
