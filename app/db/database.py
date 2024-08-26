from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.data import employers_data, job_applications_data, jobs_data, users_data
from app.db.models import Base, Employer, Job, JobApplication, User
from app.settings.config import database_url

engine = create_engine(database_url)
Session = sessionmaker(bind=engine)


def prepare_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    session = Session()

    for employer in employers_data:
        session.add(Employer(**employer))

    for job in jobs_data:
        session.add(Job(**job))

    for user in users_data:
        session.add(User(**user))

    for application in job_applications_data:
        session.add(JobApplication(**application))

    session.commit()
    session.close()
