from flask import request, jsonify, g, abort
from . import api
from .. import db
from ..models import Company, Job, PositionType, JobRecruiter, Recruiter, JobRecruiterCandidate
from ..decorators import roles_required
from ..constants import RoleType, JobStatus, RecruiterStatus, CandidateStatus, AccountStatus
from ..exceptions import ValidationError
from doroto.decorators.permission_evaluator import has_permissions
import uuid

@api.route('/company/<int:id>', methods=['GET'])
@has_permissions("company")
def get_company(id):
    company = Company.query.get_or_404(id)
    response = {
        "id": company.id,
        "name": company.name,
        "address": company.description,
        "description": company.description,
        "phone": company.phone,
        "job_count": company.jobs.count()
    }
    return jsonify(response)


@api.route('/company/<int:id>/jobs/', methods=['POST'])
@has_permissions("company")
def create_job(id):
    company = Company.query.get_or_404(id)
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
    job = Job(position_id=position_id, company_id=id, title=title, job_description=job_description, status=JobStatus.OPEN)
    job.recruiter_description = recruiter_description
    job.questions = questions
    db.session.add(job)
    db.session.commit()
    response = {
        "id": job.id,
        "title": job.title
    }
    return jsonify(response), 201


@api.route('/company/<id>/jobs/<int:job_id>/recruiters/', methods=['PUT'])
@has_permissions("company")
def select_job_recruiters(id, job_id):
    job = Job.query.get_or_404(job_id)
    company = Company.query.get_or_404(id)
    data = request.json
    ## Validate input
    try:
        selected_recruiters = data['selected_recruiters']
        for recruiter in selected_recruiters:
            recruiter_id = recruiter["id"]
            resume_limit = int(recruiter.get("resume_limit", 5))
            jobRecruiter = JobRecruiter(job_id=job_id, recruiter_id=recruiter_id, \
                        resume_limit= resume_limit, status= RecruiterStatus.REQUEST_SENT, guid=uuid.uuid4())
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


@api.route('/company/<id>/recruiters/suggestions/', methods=['GET'])
@has_permissions("company")
def get_suggested_recruiters(id):
    job_id = request.args.get('job_id')
    job = Job.query.get_or_404(job_id)
    company = Company.query.get_or_404(id)
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
    return jsonify(response), 201

@api.route('/company/<id>/job/<job_id>/candidates/', methods=['GET'])
@has_permissions("company")
def get_job_candidates(id, job_id):
    job_recruiters = JobRecruiter.query.filter_by(job_id=job_id).all()
    candidates = []
    candidateStatus = CandidateStatus()
    for job_rec in job_recruiters:
        ## ToDo check candidate status
        job_recruiter_candidates = JobRecruiterCandidate.query.filter_by(job_recruiter_id=job_rec.id)\
            .filter(~JobRecruiterCandidate.status.in_([CandidateStatus.ACCEPTED])).all()
        for job_recruiter_candidate in job_recruiter_candidates:
            if candidateStatus.checkHideCriteria(job_recruiter_candidate.status):
                name = job_recruiter_candidate.marvel_name
                phone = "****"
                email = "****"
                resume_url = job_recruiter_candidate.candidate_resume.redacted_resume_url
            else:
                name = job_recruiter_candidate.candidate.name
                phone = job_recruiter_candidate.candidate.phone
                email = job_recruiter_candidate.candidate.user.email
                resume_url = job_recruiter_candidate.candidate_resume.resume_url
            candidates.append({
                'candidate_id': job_recruiter_candidate.candidate_id,
                'status': job_recruiter_candidate.status,
                'name': name,
                'phone': phone,
                'email': email,
                'resume_url': resume_url,
                'recruiter_id': job_recruiter_candidate.candidate_recruiter.recruiter_id,
                'recruiter_name': job_recruiter_candidate.candidate_recruiter.recruiter.name,
                'recruiter_email': job_recruiter_candidate.candidate_recruiter.recruiter.user.email
            })
    return jsonify({"candidates": candidates}), 201

@api.route('/company/<id>/job/<job_id>/candidate/<candidate_id>', methods=['PUT'])
@has_permissions("company")
def update_candidate_status(id, job_id, candidate_id):
    data = request.json
    candidateStatus = CandidateStatus()
    if not candidateStatus.checkIfStatusValid(data["status"]):
        raise ValidationError('Invalid status')
    job_recruiters = JobRecruiter.query.filter_by(job_id=job_id).all()
    for job_rec in job_recruiters:
        job_recruiter_candidate = JobRecruiterCandidate.query\
            .filter_by(job_recruiter_id=job_rec.id)\
            .filter_by(candidate_id=candidate_id).first()
        if job_recruiter_candidate is not None:
            job_recruiter_candidate.status = data["status"]
            db.session.commit()
            return jsonify({"candidate_id": candidate_id}), 201
    raise ValidationError('Invalid candidate id ' + candidate_id + ' for this job')
    return jsonify({"status": "ok"}), 201
