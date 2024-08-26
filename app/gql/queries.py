from graphene import Field, Int, List, ObjectType
from sqlalchemy.orm import joinedload

from app.db.database import Session
from app.db.models import Employer, Job, JobApplication, User
from app.gql.types import EmployerObject, JobApplicationObject, JobObject, UserObject


class Query(ObjectType):
    job = Field(JobObject, id=Int(required=True))
    employer = Field(EmployerObject, id=Int(required=True))
    jobs = List(JobObject)
    employers = List(EmployerObject)
    user = Field(UserObject, id=Int(required=True))
    users = List(UserObject)
    job_applications = List(JobApplicationObject)
    job_applications_by_user = List(JobApplicationObject, id=Int(required=True))
    job_applications_by_job = List(JobApplicationObject, id=Int(required=True))

    @staticmethod
    def resolve_job(root, info, id):
        with Session() as session:
            return (
                session.query(Job)
                .options(joinedload(Job.employer))
                .filter(Job.id == id)
                .first()
            )

    @staticmethod
    def resolve_employer(root, info, id):
        with Session() as session:
            return (
                session.query(Employer)
                .options(joinedload(Employer.jobs))
                .filter(Employer.id == id)
                .first()
            )

    @staticmethod
    def resolve_user(root, info, id):
        with Session() as session:
            return session.query(User).filter(User.id == id).first()

    @staticmethod
    def resolve_jobs(root, info):
        with Session() as session:
            return session.query(Job).all()

    @staticmethod
    def resolve_employers(root, info):
        with Session() as session:
            return session.query(Employer).all()

    @staticmethod
    def resolve_users(root, info):
        with Session() as session:
            return session.query(User).all()

    @staticmethod
    def resolve_job_applications(root, info):
        with Session() as session:
            return session.query(JobApplication).all()

    @staticmethod
    def resolve_job_applications_by_user(root, info, id):
        with Session() as session:
            return (
                session.query(JobApplication).filter(JobApplication.user_id == id).all()
            )

    @staticmethod
    def resolve_job_applications_by_job(root, info, id):
        with Session() as session:
            return (
                session.query(JobApplication).filter(JobApplication.job_id == id).all()
            )
