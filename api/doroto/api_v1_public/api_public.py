from flask import request
from . import api
from .. import db
from ..models import Company
from ..decorators import json, paginate


@api.route('/company/', methods=['POST'])
@json
def new_company():
    data = request.json
    email = data['email']
    password = data['password']
    user = User(email=email)
    user.set_password(password)	
    db.session.add(u)	
    company = Company(user=user)
    company.import_data(request.json)
    db.session.add(company)
    db.session.commit()
    response = {'name':company.name, "email": company.user.email, "token": company.user.generate_auth_token()}
    return response, 201, {'Location': company.get_url()}

@api.route('/status/', methods=['GET'])
@json
def pub_api_status():
    return {"status":"OK"}