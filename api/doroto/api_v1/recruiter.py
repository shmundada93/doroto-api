from flask import request, jsonify
from . import api
from .. import db
from ..models import Recruiter, JobRecruiter
from doroto.decorators.permission_evaluator import has_permissions
from ..constants import RoleType
from ..exceptions import ValidationError
from ..constants import RoleType, JobStatus, RecruiterStatus, CandidateStatus, AccountStatus

# To be written in comapny apis
@api.route('/recruiter/', methods=['GET'])
def get_recruiters():
    return jsonify({'recruiters': [recruiter.export_data() for recruiter in Recruiter.query.all()]})

@api.route('/recruiter/<id>', methods=['GET'])
@has_permissions("recruiter")
def get_recruiter(id):
    recruiter = Recruiter.query.get_or_404(id)
    response = {
        "id": recruiter.id,
        "name": recruiter.name,
        "address": recruiter.address,
        "description": recruiter.description,
        "phone": recruiter.phone,
        "status": recruiter.status
    }
    return jsonify(response)

@api.route('/recruiter/<id>/jobs', methods=['GET'])
@has_permissions("recruiter")
def get_jobs(id):
    jobs = JobRecruiter.query.filter_by(recruiter_id=id).all()
    temp_jobs = []
    for job in jobs:
        job_data = {
            'job_id': job.job_id,
            'recruiter_id': job.recruiter_id,
            'resume_limit': job.resume_limit,
            'status': job.status,
            'guid': job.guid,
            'job': {
                'title': job.job.title,
                'company_id': job.job.company_id,
                'job_description': job.job.job_description,
                'recruiter_description': job.job.recruiter_description,
                'questions': job.job.questions,
                'open_positions': job.job.open_positions,
                'status': job.job.status,
                'position_id': job.job.position_id
            }
        }
        temp_jobs.append(job_data)
    return jsonify({"jobs": temp_jobs})

@api.route('/recruiter/<id>/job/<job_id>/status', methods=['PUT'])
@has_permissions("recruiter")
def update_job_status(id, job_id):
    job = JobRecruiter.query.filter_by(job_id=job_id).filter_by(recruiter_id=id).first()
    data = request.json
    rec_status = RecruiterStatus()
    if not rec_status.checkIfStatusValid(data["status"]):
        raise ValidationError("Status not valid")
    job.status = data["status"]
    db.session.commit()
    return jsonify({
        "job_id": job.id,
        "status": data["status"]
    }), 201
