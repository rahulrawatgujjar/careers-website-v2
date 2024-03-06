from sqlalchemy import create_engine, text
import os
# from dotenv import load_dotenv

# load_dotenv()
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

def add_application_to_db(id, data,user_id):
  with engine.connect() as conn:
    query = text("INSERT INTO applications( job_id, full_name, email, linkedin_url, education, work_experience, resume_url, user_id) VALUES ( :job_id, :full_name, :email, :linkedin_url, :education, :work_experience, :resume_url, :user_id)")
    parameters = {
        'job_id': id,
        'full_name': data["full_name"],
        'email': data["email"],
        'linkedin_url': data["linkedin_url"],
        'education': data["education"],
        'work_experience': data["work_experience"],
        'resume_url': data["resume_url"],
        "user_id": user_id
    }
    conn.execute(query, parameters)
    conn.commit()


def run_sql_query(query,parameters=None):
  with engine.connect() as conn:
    result= conn.execute(query,parameters)
    conn.commit()
    return result
  

def applied_and_unapplied_jobs(user_id):
  with engine.connect() as conn:
    # query=text("SELECT job_id FROM applications WHERE user_id = :user_id")
    query_applied=text("SELECT jobs.id, jobs.title, jobs.location, jobs.salary FROM jobs LEFT JOIN applications ON jobs.id = applications.job_id AND applications.user_id = :user_id WHERE applications.job_id IS NOT NULL")
    query_unapplied=text("SELECT jobs.id, jobs.title, jobs.location, jobs.salary FROM jobs LEFT JOIN applications ON jobs.id = applications.job_id AND applications.user_id = :user_id WHERE applications.job_id IS NULL")
    parameters={
      "user_id": user_id
    }
    result1= conn.execute(query_applied,parameters).all()
    result2= conn.execute(query_unapplied,parameters).all()
    applied_jobs=[]
    for job in result1:
      applied_jobs.append(job._asdict())
    unapplied_jobs=[]
    for job in result2:
      unapplied_jobs.append(job._asdict())
    return applied_jobs,unapplied_jobs