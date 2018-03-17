from functools import wraps
from time import time
from flask import current_app, request, g, jsonify, abort
from ..errors import unauthorized
from doroto.constants import RoleType
from doroto.models import Recruiter, Company

def roles_required(roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not g.user.has(roles):
                return unauthorized('Insufficient permissions')
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def has_permissions(type):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if g.user.role.name == RoleType.ADMIN:
                return func(*args, **kwargs)
            if type == "admin":
                if g.user.role.name == RoleType.ADMIN:
                    return func(*args, **kwargs)
                else:
                    abort(403)        
            if type == "recruiter":
                recruiter = Recruiter.query.get_or_404(kwargs['id'])
                if g.user.id != recruiter.user.id or g.user.role.name != RoleType.RECRUITER:
                    abort(403)
            return func(*args, **kwargs)
        return wrapper
    return decorator
