from . import create_app, make_celery, db
import os
import boto3
from flask import current_app
from botocore.exceptions import ClientError
from .exceptions import ValidationError
from .constants import EmailType
from .models import CandidateResume
from .email_templates import COMPANY_ONBOARDING_SUBJECT, COMPANY_ONBOARDING_BODY
import uuid
from .redaction import redactPDF

app_config=os.environ.get('FLASK_CONFIG', 'testing')
celery, app, aws_client = make_celery(app_config)

@celery.task(bind=True)
def sendEmail(self, email_type, recipient_list, config):
    ses = aws_client.client("ses")
    if email_type== EmailType.COMPANY_ONBOARDING:
        EMAIL_SUBJECT = COMPANY_ONBOARDING_SUBJECT.format(**config)
        EMAIL_BODY = COMPANY_ONBOARDING_BODY.format(**config)
    else:
        return None
    try:
        #Provide the contents of the email.
        response = ses.send_email(
            Destination={
                'ToAddresses': recipient_list,
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': "UTF-8",
                        'Data': EMAIL_BODY,
                    }
                },
                'Subject': {
                    'Charset': "UTF-8",
                    'Data': EMAIL_SUBJECT,
                },
            },
            Source="Doroto Inc <doroto2018@gmail.com>"
        )
    # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['ResponseMetadata']['RequestId'])


@celery.task(bind=True)
def redactAndUploadResume(self, candidate_resume_id, s3_resume_name):
    candidateResume = CandidateResume.query.get(candidate_resume_id)
    if not candidateResume:
        raise ValidationError("Candidate resume not found for id: " + str(candidate_resume_id))
    filename = candidateResume.redacted_resume_url
    resume_url = candidateResume.resume_url
    resume_redacted_filename = "{}/resumes/candidate-{}/{}-redacted.pdf".format(app_config, candidateResume.candidate.id, filename)
    redacted_resume_url = "https://s3-{}.amazonaws.com/doroto/{}".format(app.config['AWS_REGION'], resume_redacted_filename)
    downloadFileFromS3(s3_resume_name, app.config['UPLOAD_FOLDER'] + filename + ".pdf")
    redactPDF(filename)
    uploadFileToS3(current_app.config['UPLOAD_FOLDER'] + filename + "-final.pdf", resume_redacted_filename)
    candidateResume.redacted_resume_url = redacted_resume_url
    db.session.add(candidateResume)
    db.session.commit()

def uploadFileToS3(filepath, dest_path):
    s3 = aws_client.resource("s3")
    s3.meta.client.upload_file(filepath, 'doroto', dest_path)

def downloadFileFromS3(filename, dest_path):
    s3 = aws_client.resource("s3")
    s3.meta.client.download_file('doroto',filename, dest_path)


    


 