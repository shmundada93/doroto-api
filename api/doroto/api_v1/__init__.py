from flask import Blueprint
from ..auth import auth
from ..decorators import etag, rate_limit

api = Blueprint('api', __name__)

@api.after_request
@etag
def after_request(rv):
    """Generate an ETag header for all routes in this blueprint."""
    return rv

from . import company, errors, recruiter, candidate, admin
