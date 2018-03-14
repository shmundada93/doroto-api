from doroto.models import Role, PositionType, DepartmentType
from doroto.constants import RoleType

def seed_roles(db):
    roles = [attr for attr in dir(RoleType) if not callable(getattr(RoleType, attr)) and not attr.startswith("__")]
    for r in roles:
        role = Role.query.filter_by(name=r).first()
        if role is None:
            role = Role(name=r)
            db.session.add(role)
    db.session.commit()

def seed_departments_and_positions(db):
    departments = ['SALES', 'MARKETING', 'TECHNOLOGY', 'HR']
    positions = ['JUNIOR', 'SENIOR', 'MANAGER']
    for d in departments:
        department = DepartmentType.query.filter_by(name=d).first()
        if department is None:
            department = DepartmentType(name=d)
            db.session.add(department)
            for p in positions:
                position = PositionType(department_type=department, name=p)
                db.session.add(position)
    db.session.commit()
    
    
