from flask import request, jsonify
from . import api
from .. import db
from ..models import Company
from ..decorators import roles_required
from ..constants import RoleType


@api.route('/company/', methods=['GET'])
@roles_required([RoleType.ADMIN])
def get_companies():
    return jsonify({'companies': [company.export_data() for company in Company.query.all()]})