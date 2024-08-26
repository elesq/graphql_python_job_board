from graphene import Boolean, Field, Int, Mutation, String

from app.db.database import Session
from app.db.models import User
from app.gql.types import UserObject

notFoundExceptionMessage = "user not found"


class AddUser(Mutation):
    class Arguments:
        username = String(required=True)
        email = String(required=True)
        password = String(required=True)
        role = String(required=True)

    user = Field(lambda: UserObject)

    @staticmethod
    def mutate(root, info, username, email, password, role):
        user = User(username=username, email=email, password=password, role=role)
        with Session() as session:
            session.add(user)
            session.commit()
            session.refresh(user)
            return AddUser(user)


class UpdateUser(Mutation):
    class Arguments:
        id = Int(required=True)
        username = String()
        email = String()
        password = String()
        role = String()

    user = Field(lambda: UserObject)

    @staticmethod
    def mutate(root, info, id, username=None, email=None, password=None, role=None):
        with Session() as session:
            user = session.query(User).filter(User.id == id).first()

            if not user:
                raise Exception(notFoundExceptionMessage)

            if username is not None:
                user.username = username
            if email is not None:
                user.email = email
            if password is not None:
                user.password = password
            if role is not None:
                user.role = role

            session.commit()
            session.refresh(user)
            session.close()
            return UpdateUser(user=user)


class DeleteUser(Mutation):
    class Arguments:
        id = Int(required=True)

    success = Boolean()

    @staticmethod
    def mutate(root, info, id):
        with Session() as session:
            user = session.query(User).filter(User.id == id).first()
            if not user:
                raise Exception(notFoundExceptionMessage)

            session.delete(user)
            session.commit()
            session.close()
            return DeleteUser(success=True)
