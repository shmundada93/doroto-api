from flask import request, jsonify
from . import api
from .. import db
from ..models import Company, Recruiter
from ..exceptions import ValidationError
from ..constants import RoleType
from doroto.decorators.permission_evaluator import roles_required, has_permissions
from ..constants import RoleType, JobStatus, RecruiterStatus, CandidateStatus, AccountStatus


@api.route('/company/', methods=['GET'])
@roles_required([RoleType.ADMIN])
def get_companies():
    return jsonify({'companies': [company.export_data() for company in Company.query.all()]})

@api.route('/recruiter/<int:id>/account_activation', methods=['PUT'])
@has_permissions("admin")
def update_recruiter_account(id):
    recruiter = Recruiter.query.get_or_404(id)
    data = request.json
    account_status = AccountStatus()
    if not account_status.checkIfStatusValid(data["status"]):
        raise ValidationError("Status not valid")
    recruiter.status = data["status"]
    db.session.commit()
    return jsonify({
        "status": "ok"
    })

@api.route('/company/<int:id>/account_activation', methods=['PUT'])
@has_permissions("admin")
def update_company_account(id):
    company = Company.query.get_or_404(id)
    data = request.json
    account_status = AccountStatus()
    if not account_status.checkIfStatusValid(data["status"]):
        raise ValidationError("Status not valid")
    company.status = data["status"]
    db.session.commit()
    return jsonify({
        "status": "ok"
    })
