from flask import request, jsonify, g, abort
from . import api
from .. import db
from ..models import Company, Job, PositionType, JobRecruiter, Recruiter, Candidate
from ..decorators import roles_required
from ..constants import RoleType, JobStatus, RecruiterStatus, CandidateStatus, AccountStatus
from ..exceptions import ValidationError
from werkzeug.utils import secure_filename
import uuid

def verify_permissions(candidate_id):
    candidate = Candidate.query.get_or_404(company_id)
    if g.user.id != candidate.user.id and g.user.role.name != RoleType.ADMIN:
        abort(403)
    else:
        return candidate


@api.route('/candidates/<int:id>/resumes/', methods=['POST'])
@roles_required([RoleType.CANDIDATE, RoleType.ADMIN])
def upload_resume(id):
    candidate = verify_permissions(id)
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


