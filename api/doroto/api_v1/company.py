from flask import request
from . import api
from .. import db
from ..models import Company
from ..decorators import json, paginate


@api.route('/company/', methods=['GET'])
@json
@paginate('company')
def get_companies():
    return Company.query

@api.route('/company/<int:id>', methods=['GET'])
@json
def get_company(id):
    return Company.query.get_or_404(id)

@api.route('/company/', methods=['POST'])
@json
def new_company():
    company = Company()
    company.import_data(request.json)
    db.session.add(company)
    db.session.commit()
    return {}, 201, {'Location': company.get_url()}

@api.route('/company/<int:id>', methods=['PUT'])
@json
def edit_company(id):
    company = Company.query.get_or_404(id)
    company.import_data(request.json)
    db.session.add(company)
    db.session.commit()
    return {}
