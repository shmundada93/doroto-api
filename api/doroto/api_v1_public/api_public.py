from flask import request, jsonify
from . import api
from .. import db
from ..models import Company, User, Role, Recruiter
from ..constants import RoleType


@api.route('/company/', methods=['POST'])
def new_company():
    data = request.json
    email = data['email']
    password = data['password']
    role = Role.query.filter_by(name=RoleType.COMPANY).first()
    user = User(email=email, role=role)
    user.set_password(password)	
    db.session.add(user)	
    company = Company(user=user)
    company.import_data(request.json)
    db.session.add(company)
    db.session.commit()
    response = {'name':company.name, "email": company.user.email, "token": company.user.generate_auth_token()}
    return jsonify(response), 201, {'Location': company.get_url()}


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