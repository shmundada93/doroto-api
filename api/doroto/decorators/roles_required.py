import functools
from time import time
from flask import current_app, request, g, jsonify
from ..errors import unauthorized

def roles_required(roles):
    def decorator(f):
        @functools.wraps(f)
        def decorated_function(*args, **kwargs):
            if not g.user.has(roles):
                return unauthorized('Insufficient permissions')
            return f(*args, **kwargs)
        return decorated_function
    return decorator