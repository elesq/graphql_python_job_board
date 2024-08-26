# GraphQL API

A demo job board api using graphene, sqlalchemy and python. A GraphQL playground is bundled with the app and can be found at `//localhost:8000/gql`. The app uses uvicorn[standard] (ASGI web server implementation for Python) as the web server.

notes

-   In the app we use a global lazy load setting for sqlalchemy setting it to eager. This is not typically a solid option for all production apps, especailly larger apps where payload size and frequency may have considerable perf impacts. In this instance it's fine, but look at that as a convenience rather than a standard.
-   To approach a non-global control of lazy loading we could use something similar to the below is the applications functions/. Here a manual control is defined to use `joinedload` and perform the join action rather than the default option which is to skip.

```python
@staticmethod
    def mutate(root, info, id, title=None, description=None, employer_id=None):
        with Session() as session:
            # joinedload example
            job = (
                session.query(Job)
                .options(joinedload(Job.employer))
                .filter(Job.id == id)
                .first()
            )
            if not job:
                raise Exception("job not found")
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



@staticmethod
    def resolve_jobs(root, info):
        with Session() as session:
            # return session.query(Job).all() # non joined
            return session.query(Job).options(joinedload(Job.employer)).all()
```
