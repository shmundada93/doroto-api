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

@api.route('/company/<int:id>', methods=['GET'])
@roles_required([RoleType.COMPANY, RoleType.ADMIN])
def get_company(id):
    return jsonify(Company.query.get_or_404(id).export_data())

@api.route('/company/<int:id>', methods=['PUT'])
@roles_required([RoleType.COMPANY, RoleType.ADMIN])
def edit_company(id):
    company = Company.query.get_or_404(id)
    company.import_data(request.json)
    db.session.add(company)
    db.session.commit()
    return jsonify(company.export_data())
