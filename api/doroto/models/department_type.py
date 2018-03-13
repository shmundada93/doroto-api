from . import Base

class DepartmentType(Base):
    __tablename__ = 'department_type'
    name = db.Column(db.String(64), index=True)

