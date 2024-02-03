from sqlalchemy import create_engine, text
import os

db_string = os.environ['DB_STRING']

engine = create_engine(db_string)


def load_jobs_from_db():
  with engine.connect() as conn:
    result = conn.execute(text("select * from jobs"))
    jobs = []
    for job in result.all():
      jobs.append(job._asdict())
    return jobs



def load_job_from_db(id):
  with engine.connect() as conn:
    result=conn.execute(text(
      f"SELECT * FROM jobs WHERE id = {id}"
    ))
    jobs=result.all()
    if len(jobs)==0:
      return None
    else:
      return jobs[0]._asdict()