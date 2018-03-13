from flask import url_for, current_app
from ..exceptions import ValidationError
from ..utils import split_url
from . import Base
from .. import db

class PositionType(Base):
    __tablename__ = 'position_type'
    name = db.Column(db.String(64), index=True)
