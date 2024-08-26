from graphene import Boolean, Field, Int, Mutation, String

from app.db.database import Session
from app.db.models import Employer
from app.gql.types import EmployerObject

notFoundExceptionMessage = "employer not found"


class AddEmployer(Mutation):
    class Arguments:
        name = String(required=True)
        contact_email = String(required=True)
        industry = String(required=True)

    employer = Field(lambda: EmployerObject)

    @staticmethod
    def mutate(root, info, name, contact_email, industry):
        with Session() as session:
            employer = Employer(
                name=name, contact_email=contact_email, industry=industry
            )
            session.add(employer)
            session.commit()
            session.refresh(employer)
            return AddEmployer(employer=employer)


class UpdateEmployer(Mutation):
    class Arguments:
        id = Int(required=True)
        name = String()
        contact_email = String()
        industry = String()

    employer = Field(lambda: EmployerObject)

    @staticmethod
    def mutate(root, info, id, name=None, contact_email=None, industry=None):
        with Session() as session:
            employer = session.query(Employer).filter(Employer.id == id).first()

            if not employer:
                raise Exception(notFoundExceptionMessage)

            if name is not None:
                employer.name = name
            if contact_email is not None:
                employer.contact_email = contact_email
            if industry is not None:
                employer.industry = industry
            session.commit()
            session.refresh(employer)
            session.close()
            return UpdateEmployer(employer=employer)


class DeleteEmployer(Mutation):
    class Arguments:
        id = Int(required=True)

    success = Boolean()

    @staticmethod
    def mutate(root, info, id):
        with Session() as session:
            employer = session.query(Employer).filter(Employer.id == id).first()
            if not employer:
                raise Exception(notFoundExceptionMessage)

            session.delete(employer)
            session.commit()
            session.close()
            return DeleteEmployer(success=True)
