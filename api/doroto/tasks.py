from . import create_app, make_celery, db
import os
import boto3
from botocore.exceptions import ClientError
from .constants import EmailType
from .email_templates import COMPANY_ONBOARDING_SUBJECT, COMPANY_ONBOARDING_BODY

celery, aws_client = make_celery(os.environ.get('FLASK_CONFIG', 'testing'))

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
def redactAndUploadResume(self, candidate_id, resume_name, resume_path):
    pass