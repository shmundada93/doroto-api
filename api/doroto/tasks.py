from . import create_app, make_celery, db
import os

celery = make_celery(os.environ.get('FLASK_CONFIG', 'testing'))

@celery.task(bind=True)
def sendEmail(self, type, config):
    pass

@celery.task(bind=True)
def redactAndUploadResume(self, candidate_id, resume_name, resume_path):
    pass