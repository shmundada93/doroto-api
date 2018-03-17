class RoleType:
    ADMIN = 'ADMIN'
    COMPANY = 'COMPANY'
    RECRUITER = 'RECRUITER'
    CANDIDATE = 'CANDIDATE'

class AccountStatus:
    PENDING = 'PENDING'
    ACTIVE = 'ACTIVE'
    INACTIVE = 'INACTIVE'

    def __init__(self):
        pass

    def checkIfStatusValid(self, status):
        if status not in [AccountStatus.PENDING, AccountStatus.ACTIVE, AccountStatus.INACTIVE]:
            return False
        return True

class JobStatus:
    OPEN = 'OPEN'
    CLOSE = 'CLOSE'

    def __init__(self):
        pass

    def checkIfStatusValid(self, status):
        if status not in [JobStatus.OPEN, JobStatus.CLOSE]:
            return False
        return True

class RecruiterStatus:
    REQUEST_SENT = 'REQUEST_SENT' # Request sent for resumes by company
    ACCEPTED = 'ACCEPTED'
    DECLINED = 'DECLINED'
    TERMINATED = 'TERMINATED' # Request for resumes terminated by company

    def __init__(self):
        pass

    def checkIfStatusValid(self, status):
        if status not in [RecruiterStatus.REQUEST_SENT, RecruiterStatus.ACCEPTED, RecruiterStatus.DECLINED, RecruiterStatus.TERMINATED]:
            return False
        return True

class CandidateStatus:
    ACCEPTED = 'ACCEPTED' # Application received by recruiter
    SUBMITTED = 'SUBMITTED'  # Application sent to company
    SHORTLISTED = 'SHORTLISTED'
    OFFERED = 'OFFERED'
    JOINED = 'JOINED'
