from graphene import Boolean, Field, Int, Mutation, String

from app.db.database import Session
from app.db.models import Job
from app.gql.types import JobObject

notFoundExceptionMessage = "job not found"


class AddJob(Mutation):
    class Arguments:
        title = String(required=True)
        description = String(required=True)
        employer_id = Int(required=True)

    job = Field(lambda: JobObject)

    @staticmethod
    def mutate(root, info, title, description, employer_id):
        job = Job(title=title, description=description, employer_id=employer_id)
        with Session() as session:
            session.add(job)
            session.commit()
            session.refresh(job)
            return AddJob(job)


class UpdateJob(Mutation):
    class Arguments:
        id = Int(required=True)
        title = String()
        description = String()
        employer_id = Int()

    job = Field(lambda: JobObject)

    @staticmethod
    def mutate(root, info, id, title=None, description=None, employer_id=None):
        with Session() as session:
            job = session.query(Job).filter(Job.id == id).first()

            if not job:
                raise Exception(notFoundExceptionMessage)

            if title is not None:
                job.title = title
            if description is not None:
                job.description = description
            if employer_id is not None:
                job.employer_id = employer_id
            session.commit()
            session.refresh(job)
            session.close()
            return UpdateJob(job=job)


class DeleteJob(Mutation):
    class Arguments:
        id = Int(required=True)

    success = Boolean()

    @staticmethod
    def mutate(root, info, id):
        with Session() as session:
            job = session.query(Job).filter(Job.id == id).first()
            if not job:
                raise Exception(notFoundExceptionMessage)

            session.delete(job)
            session.commit()
            session.close()
            return DeleteJob(success=True)
