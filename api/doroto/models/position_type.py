from flask import url_for, current_app
from ..exceptions import ValidationError
from ..utils import split_url
from . import Base
from .. import db

class PositionType(Base):
    __tablename__ = 'position_types'
    name = db.Column(db.String(64), index=True)
    department_id = db.Column(db.Integer, db.ForeignKey('department_types.id'))
