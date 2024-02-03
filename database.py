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

def add_application_to_db(id, data):
  with engine.connect() as conn:
    query = text("INSERT INTO applications( job_id, full_name, email, linkedin_url, education, work_experience, resume_url) VALUES ( :job_id, :full_name, :email, :linkedin_url, :education, :work_experience, :resume_url)")
    parameters = {
        'job_id': id,
        'full_name': data["full_name"],
        'email': data["email"],
        'linkedin_url': data["linkedin_url"],
        'education': data["education"],
        'work_experience': data["work_experience"],
        'resume_url': data["resume_url"]
    }
    conn.execute(query, parameters)
    conn.commit()