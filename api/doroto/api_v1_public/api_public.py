from flask import request, jsonify
from . import api
from .. import db
from ..models import Company, User, Role, Recruiter
from ..constants import RoleType
from ..exceptions import ValidationError


@api.route('/company/', methods=['POST'])
def new_company():
    data = request.json
    ## Validate input
    try:
        name = data['name']
        email = data['email']
        password = data['password']
    except KeyError as e:
        raise ValidationError('Invalid company: missing ' + e.args[0])
    user = User.query.filter_by(email=email).first()
    if user:
        print("HERE")
        raise ValidationError('Invalid company: duplicate email')
    ## Fetch role object
    role = Role.query.filter_by(name=RoleType.COMPANY).first()
    ## Create user
    user = User(email=email, role=role)
    user.set_password(password)	
    db.session.add(user)
    ## Create company
    address = data.get("address", None)
    description = data.get("description", None)
    phone = data.get("phone", None)
    company = Company(user=user, name=name, address=address, description=description, phone=phone, activation_status="INPROGRESS")
    db.session.add(company)
    db.session.commit()
    ## Generate response
    response = {'id':company.id, 'name':company.name, "email": company.user.email, "token": company.user.generate_auth_token()}
    return jsonify(response), 201


@api.route('/recruiter/', methods=['POST'])
def new_recruiter():
    data = request.json
    email = data['email']
    password = data['password']
    role = Role.query.filter_by(name=RoleType.RECRUITER).first()
    user = User(email=email, role=role)
    user.set_password(password)	
    db.session.add(user)	
    recruiter = Recruiter(user=user)
    recruiter.import_data(request.json)
    db.session.add(recruiter)
    db.session.commit()
    response = {'name':recruiter.name, "email": recruiter.user.email, "token": recruiter.user.generate_auth_token()}
    return jsonify(response), 201, {'Location': recruiter.get_url()}


@api.route('/status/', methods=['GET'])
def pub_api_status():
    return jsonify({"status":"OK"})