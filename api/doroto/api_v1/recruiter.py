from flask import request, jsonify
from . import api
from .. import db
from ..models import Recruiter, JobRecruiter, JobRecruiterCandidate
from doroto.decorators.permission_evaluator import has_permissions
from ..constants import RoleType
from ..auth import auth
from ..exceptions import ValidationError
from ..constants import RoleType, JobStatus, RecruiterStatus, CandidateStatus, AccountStatus


@api.route('/recruiter/<id>', methods=['GET'])
@auth.login_required
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
@auth.login_required
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
@auth.login_required
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

@api.route('/recruiter/<id>/job/<job_id>/applicants', methods=['GET'])
@auth.login_required
@has_permissions("recruiter")
def get_job_applicants(id, job_id):
       job_recruiter = JobRecruiter.query.filter_by(job_id=job_id).filter_by(recruiter_id=id).first()
       candidates = JobRecruiterCandidate.query.filter_by(job_recruiter_id=job_recruiter.id).all()
       temp = []
       for candidate in candidates:
           temp_candidate = {
            "candidate_id": candidate.candidate_id,
            "candidate_resume_id": candidate.candidate_resume_id,
            "candidate_status": candidate.status,
            "candidate_name": candidate.candidate.name,
            "candidate_phone": candidate.candidate.phone,
            "candidate_email": candidate.candidate.user.email
           }
           temp.append(temp_candidate)
       return jsonify({"candidates": temp}), 201

@api.route('/recruiter/<id>/job/<job_id>/submit_applicants', methods=['PUT'])
@auth.login_required
@has_permissions("recruiter")
def submit_candidates(id, job_id):
    job_recruiter = JobRecruiter.query.filter_by(job_id=job_id).filter_by(recruiter_id=id).first()
    data = request.json
    submitted_candidates = data["submitted_candidates"]
    for temp in submitted_candidates:
        candidate = JobRecruiterCandidate.query\
            .filter_by(job_recruiter_id=job_recruiter.id)\
            .filter_by(candidate_id=temp).first()
        if candidate is not None:
            if candidate.status == CandidateStatus.ACCEPTED:
                candidate.status = CandidateStatus.SUBMITTED
            else:
                raise ValidationError("Invalid status transition.")
        else:
            raise ValidationError("Candidate with id "  + temp + "not found")
        db.session.commit()
    return jsonify({"status": "success"})
