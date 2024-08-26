from graphene import ObjectType

from app.gql.employer.mutations import AddEmployer, DeleteEmployer, UpdateEmployer
from app.gql.job.mutations import AddJob, DeleteJob, UpdateJob
from app.gql.job_applications.mutations import AddJobApplication, DeleteJobApplication


class Mutation(ObjectType):
    add_job = AddJob.Field()
    update_job = UpdateJob.Field()
    delete_job = DeleteJob.Field()
    add_employer = AddEmployer.Field()
    update_employer = UpdateEmployer.Field()
    delete_employer = DeleteEmployer.Field()
    add_job_application = AddJobApplication.Field()
    delete_job_application = DeleteJobApplication.Field()
