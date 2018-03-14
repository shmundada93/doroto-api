from flask import url_for, current_app
from ..exceptions import ValidationError
from ..utils import split_url
from . import Base
from .. import db

class DepartmentType(Base):
    __tablename__ = 'department_types'
    name = db.Column(db.String(64), index=True)
    positions = db.relationship('PositionType', backref='department_type', lazy='dynamic')