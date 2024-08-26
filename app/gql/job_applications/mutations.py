from graphene import Boolean, Field, Int, Mutation

from app.db.database import Session
from app.db.models import JobApplication
from app.gql.types import JobApplicationObject

notFoundExceptionMessage = "job application not found"


class AddJobApplication(Mutation):
    class Arguments:
        user_id = Int(required=True)
        job_id = Int(required=True)

    job_application = Field(lambda: JobApplicationObject)

    @staticmethod
    def mutate(root, info, user_id, job_id):
        with Session() as session:
            job_application = JobApplication(user_id=user_id, job_id=job_id)

            session.add(job_application)
            session.commit()
            session.refresh(job_application)
            return AddJobApplication(job_application=job_application)


class DeleteJobApplication(Mutation):
    class Arguments:
        id = Int(required=True)

    success = Boolean()

    @staticmethod
    def mutate(root, info, user_id, job_id):
        with Session() as session:
            job_application = (
                session.query(JobApplication)
                .filter(
                    JobApplication.user_id == user_id, JobApplication.job_id == job_id
                )
                .first()
            )
            if not job_application:
                raise Exception(notFoundExceptionMessage)

            session.delete(job_application)
            session.commit()
            session.close()
            return DeleteJobApplication(success=True)
