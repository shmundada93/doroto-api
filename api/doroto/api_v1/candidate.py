from flask import request, jsonify, g, abort, current_app
from . import api
from .. import db
from ..models import Company, Job, PositionType, JobRecruiter, Recruiter, Candidate, JobRecruiterCandidate, CandidateResume
from doroto.decorators.permission_evaluator import has_permissions
from ..constants import RoleType, JobStatus, RecruiterStatus, CandidateStatus, AccountStatus
from ..exceptions import ValidationError
from werkzeug.utils import secure_filename
from ..utils import allowed_file
from ..tasks import redactAndUploadResume, uploadFileToS3
import os
import uuid

@api.route('/candidates/<int:id>/resumes/', methods=['POST'])
@has_permissions("candidate")
def upload_resume(id):
    ## Validate input
    try:
        file = request.files['resume_file']
        resume_name = request.form['resume_name']
    except KeyError as e:
        raise ValidationError('Invalid resume: missing ' + e.args[0])
    if file.filename == '':
        raise ValidationError('No selected file')
    if file and allowed_file(file.filename):
        extension = file.filename.split(".")[-1]
        filename = str(uuid.uuid4())
        filename_with_extension = filename + "." + extension
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename_with_extension)
        file.save(filepath)
    candidate = Candidate.query.get_or_404(id)
    resume_filename = "{}/resumes/candidate-{}/{}.pdf".format(current_app.config['FLASK_CONFIG'], id, filename)
    resume_url = "https://s3-{}.amazonaws.com/doroto/{}".format(current_app.config['AWS_REGION'], resume_filename)
    uploadFileToS3(filepath, resume_filename)
    candidateResume = CandidateResume(candidate=candidate, resume_name=resume_name, resume_url=resume_url, redacted_resume_url=filename)
    db.session.add(candidateResume)
    db.session.commit()
    redactAndUploadResume.delay(candidateResume.id, resume_filename)
    response = {
        "id": candidateResume.id,
        "resume_name": candidateResume.resume_name
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
