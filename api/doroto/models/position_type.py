from . import Base

class PositionType(Base):
    __tablename__ = 'position_type'
    name = db.Column(db.String(64), index=True)