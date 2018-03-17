from flask import request, jsonify, g, abort
from . import api
from .. import db
from ..models import Company, Job, PositionType, JobRecruiter, Recruiter, Candidate, JobRecruiterCandidate, CandidateResume
from doroto.decorators.permission_evaluator import has_permissions
from ..constants import RoleType, JobStatus, RecruiterStatus, CandidateStatus, AccountStatus
from ..exceptions import ValidationError
from werkzeug.utils import secure_filename
import uuid

@api.route('/candidates/<int:id>/resumes/', methods=['POST'])
@has_permissions("candidate")
def upload_resume(id):
    data = request.json
    ## Validate input
    file = request.files['file']
    dir_path = os.path.dirname(os.path.realpath(__file__))
    outputfile = '' + str(project_id) + '.xlsx'
    outputfile_path = dir_path + "/../temp/" + outputfile
    file.save(outputfile_path)
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

@api.route('/candidate/<int:id>/job/<guid>/apply', methods=['POST'])
@has_permissions("candidate")
def apply_for_job(id, guid):
    job_recruiter = JobRecruiter.query.filter_by(guid=guid).first()
    data = request.json
    if job_recruiter.job.status != JobStatus.OPEN:
        raise ValidationError("Job application is closed now.")
    if job_recruiter.status != RecruiterStatus.ACCEPTED:
        raise ValidationError("Recruiter has not accepted the proposal yet.")
    if data.get("candidate_resume_id") is None:
        raise ValidationError("Please upload a resume.")
    candidate_resume_id = data["candidate_resume_id"]
    candidate_resume = CandidateResume.query.filter_by(id=candidate_resume_id).first()
    if candidate_resume is None:
        raise ValidationError("Resume for this id does not exist")
    applied_job = JobRecruiterCandidate.query.filter_by(job_recruiter_id=job_recruiter.id).filter_by(candidate_id=id).first()
    if applied_job is not None:
        raise ValidationError("Already applied for job.")
    job_recruiter_candidate = JobRecruiterCandidate(
        job_recruiter_id=job_recruiter.id,
        candidate_id=id,
        candidate_resume_id=candidate_resume_id,
        status=CandidateStatus.ACCEPTED
        )
    db.session.add(job_recruiter_candidate)
    db.session.commit()
    return jsonify({"status": "applied", "candidate_id": id}), 201
