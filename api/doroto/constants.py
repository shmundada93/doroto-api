class RoleType:
    ADMIN = 'ADMIN'
    COMPANY = 'COMPANY'
    RECRUITER = 'RECRUITER'
    CANDIDATE = 'CANDIDATE'

class AccountStatus:
    PENDING = 'PENDING'
    ACTIVE = 'ACTIVE'
    INACTIVE = 'INACTIVE'

class JobStatus:
    OPEN = 'OPEN'
    CLOSE = 'CLOSE'

class RecruiterStatus:
    REQUEST_SENT = 'REQUEST_SENT' # Request sent for resumes by company
    ACCEPTED = 'ACCEPTED'
    DECLINED = 'DECLINED'
    TERMINATED = 'TERMINATED' # Request for resumes terminated by company

class CandidateStatus:
    ACCEPTED = 'ACCEPTED' # Application received by recruiter
    SUBMITTED = 'SUBMITTED'  # Application sent to company
    SHORTLISTED = 'SHORTLISTED'
    OFFERED = 'OFFERED' 
    JOINED = 'JOINED'