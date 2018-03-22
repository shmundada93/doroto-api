from flask import url_for, current_app
from ..exceptions import ValidationError
from ..utils import split_url
from . import Base, JobRecruiter, JobRecruiterCandidate
from doroto.constants import CandidateStatus
from .. import db
from sqlalchemy.sql import func

class Job(Base):
    __tablename__ = "jobs"
    title = db.Column(db.String(256))
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), index=True)
    job_description = db.Column(db.Text)
    recruiter_description = db.Column(db.Text)
    questions = db.Column(db.Text)
    open_positions = db.Column(db.Integer)
    status = db.Column(db.String(256))
    position_id = db.Column(db.Integer, db.ForeignKey('position_types.id'), index=True)
    job_recruiters = db.relationship('JobRecruiter', backref='job', lazy='dynamic')

    @property
    def resumes_requested(self):
        resumes_requested = db.session.query(func.sum(JobRecruiter.resume_limit).label('requested'))\
                            .filter(JobRecruiter.job_id==self.id).first().requested
        resumes_requested = int(resumes_requested) if resumes_requested else 0
        return resumes_requested

    @property
    def resumes_received(self):
        resumes_received = db.session.query(JobRecruiterCandidate).join(JobRecruiter).join(Job)\
                            .filter(JobRecruiterCandidate.job_recruiter_id == JobRecruiter.id)\
                            .filter(JobRecruiter.job_id == self.id)\
                            .filter(JobRecruiterCandidate.status != CandidateStatus.ACCEPTED)\
                            .count()
        return resumes_received

    @property
    def resumes_shortlisted(self):
        resumes_shortlisted = db.session.query(JobRecruiterCandidate).join(JobRecruiter).join(Job)\
                            .filter(JobRecruiterCandidate.job_recruiter_id == JobRecruiter.id)\
                            .filter(JobRecruiter.job_id == self.id)\
                            .filter(JobRecruiterCandidate.status != CandidateStatus.ACCEPTED)\
                            .filter(JobRecruiterCandidate.status != CandidateStatus.SUBMITTED)\
                            .count()
        return resumes_shortlisted
    

    
