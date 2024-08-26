from contextlib import asynccontextmanager

from fastapi import FastAPI
from graphene import Schema
from starlette_graphene3 import GraphQLApp, make_playground_handler

from app.db.database import Session, prepare_database
from app.db.models import Employer, Job
from app.gql.mutations import Mutation
from app.gql.queries import Query

schema = Schema(query=Query, mutation=Mutation)


@asynccontextmanager
async def lifespan(app: FastAPI):
    prepare_database()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/employers")
def get_all_employers():
    with Session() as session:
        return session.query(Employer).all()


@app.get("/jobs")
def get_all_jobs():
    with Session() as session:
        return session.query(Job).all()


app.mount(
    "/gql",
    GraphQLApp(
        schema=schema,
        on_get=make_playground_handler(),
    ),
)
