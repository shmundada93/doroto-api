from . import Base

class UserType(Base):
    __tablename__ = 'user_type'
    name = db.Column(db.String(64), index=True)