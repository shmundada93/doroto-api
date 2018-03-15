from flask import request, jsonify, g, abort
from . import api
from .. import db
from ..models import Company, Job, PositionType, JobRecruiter, Recruiter
from ..decorators import roles_required
from ..constants import RoleType
from ..exceptions import ValidationError
import uuid

def verify_permissions(company_id):
    company = Company.query.get_or_404(company_id)
    if g.user.id != company.user.id and g.user.role.name != RoleType.ADMIN:
        abort(403)
    ## ToDo: Check activation status
    else:
        return company

@api.route('/companies/<int:id>', methods=['GET'])
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


@api.route('/companies/<int:id>/jobs/', methods=['POST'])
@roles_required([RoleType.COMPANY, RoleType.ADMIN])
def create_job(id):
    company = verify_permissions(id)
    data = request.json
    ## Validate input
    try:
        title = data['title']
        job_description = data['job_description']
        open_positions = data['open_positions']
        position_id = data['position_id']
    except KeyError as e:
        raise ValidationError('Invalid job: missing ' + e.args[0])
    ## Create Job
    recruiter_description = data.get('recruiter_description', None)
    questions = data.get('questions', None)
    job = Job(position_id=position_id, company_id=id, title=title, job_description=job_description)
    job.recruiter_description = recruiter_description
    job.questions = questions
    db.session.add(job)
    db.session.commit()
    response = {
        "id": job.id,
        "title": job.title
    }
    return jsonify(response), 201


@api.route('/jobs/<int:job_id>/recruiters/', methods=['PUT'])
@roles_required([RoleType.COMPANY, RoleType.ADMIN])
def select_job_recruiters(job_id):
    job = Job.query.get_or_404(job_id)
    company_id = job.company.id
    company = verify_permissions(company_id)
    data = request.json
    ## Validate input
    try:
        selected_recruiters = data['selected_recruiters']
        for recruiter in selected_recruiters:
            recruiter_id = recruiter["id"]
            resume_limit = int(recruiter.get("resume_limit", 5))
            jobRecruiter = JobRecruiter(job_id=job_id, recruiter_id=recruiter_id, \
                        resume_limit= resume_limit, action_status= "REQUESTED", guid=uuid.uuid4())
            ## Check if jobReruiter already added
            tempJobRecruiter = JobRecruiter.query.filter_by(job_id=job_id).filter_by(recruiter_id=recruiter_id).first()
            if not tempJobRecruiter:
                db.session.add(jobRecruiter)
    except KeyError as e:
        raise ValidationError('Invalid selected recruiters list: missing ' + e.args[0])
    db.session.commit()
    recruiters = JobRecruiter.query.filter_by(job_id=job_id).all()
    recruiters_json = []
    for jobRecruiter in recruiters:
        recruiter = {
                "id": jobRecruiter.id,
                "name": jobRecruiter.recruiter.name,
                "resume_upload_url" : jobRecruiter.guid
            }
        recruiters_json.append(recruiter)
    response = {
        "job_id": job.id,
        "title": job.title,
        "recruiters": recruiters_json
    }
    return jsonify(response), 201


@api.route('/recruiters/suggestions/', methods=['GET'])
@roles_required([RoleType.COMPANY, RoleType.ADMIN])
def get_suggested_recruiters():
    job_id = request.args.get('job_id')
    job = Job.query.get_or_404(job_id)
    company_id = job.company.id
    company = verify_permissions(company_id)
    recruiters = Recruiter.query.all()
    recruiters_json = []
    for recruiter in recruiters:
        recruiter_json = {
            'id': recruiter.id,
            'name': recruiter.name,
            'description': recruiter.description
        }
        recruiters_json.append(recruiter_json)

    response = {
        "job_id":job_id,
        "title":job.title,
        "suggested_recruiters": recruiters_json
    }
    return jsonify(response)
