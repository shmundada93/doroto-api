from flask import request, jsonify, g, abort
from . import api
from .. import db
from ..models import Company
from ..decorators import roles_required
from ..constants import RoleType


def verify_permissions(company_id):
    company = Company.query.get_or_404(company_id)
    if g.user.id != company.user.id and g.user.role.name != RoleType.ADMIN:
        abort(403)
    else:
        return company

@api.route('/company/<int:id>', methods=['GET'])
@roles_required([RoleType.COMPANY, RoleType.ADMIN])
def get_company(id):
    company = verify_permissions(id)
    response = {
        "id": company.id,
        "name": company.name,
        "address": company.description,
        "description": company.description,
        "phone": company.phone,
        "job_count": company.jobs.count()
    }
    return jsonify(response)
