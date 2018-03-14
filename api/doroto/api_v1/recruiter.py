from flask import request, jsonify
from . import api
from .. import db
from ..models import Recruiter
from ..decorators import roles_required
from ..constants import RoleType


@api.route('/recruiter/', methods=['GET'])
def get_recruiters():
    return jsonify({'recruiters': [recruiter.export_data() for recruiter in Recruiter.query.all()]})

@api.route('/recruiter/<int:id>', methods=['GET'])
@roles_required([RoleType.RECRUITER, RoleType.ADMIN])
def get_recruiter(id):
    return jsonify(Recruiter.query.get_or_404(id).export_data())

@api.route('/recruiter/<int:id>', methods=['PUT'])
def edit_recruiter(id):
    recruiter = Recruiter.query.get_or_404(id)
    recruiter.import_data(request.json)
    db.session.add(recruiter)
    db.session.commit()
    return jsonify({})
