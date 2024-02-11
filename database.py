import os
import sqlalchemy as sa

from sqlalchemy import create_engine, text

DB_CONNECTION_STRING = "postgresql+psycopg2://aryan732003:BWArQI0Oi4TE@ep-sparkling-glade-a50wr0c5.us-east-2.aws.neon.tech/neondb?sslmode=require"
os.environ['DB_CONNECTION_STRING'] = DB_CONNECTION_STRING

# Modify the connection string to include SSL-related parameters
engine = sa.create_engine(os.environ['DB_CONNECTION_STRING'],
                          connect_args={"sslmode": "require"})


def load_jobs_from_db():
  with engine.connect() as conn:
    result = conn.execute(text("select * from jobs"))
    jobs = []
    for row in result:
      jobs_dict = (row._mapping)
      jobs.append(dict(jobs_dict))
    return jobs


def load_job_from_db(id):
  with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM jobs WHERE id = :val"),
                          {'val': id})
    rows = result.all()
    if len(rows) == 0:
      return None
    else:
      return dict(rows[0]._mapping)


def add_application_to_db(job_id, data):
  with engine.connect() as conn:
    query = text(
        f"INSERT INTO applications (job_id, full_name, email, linkedin_url, education, work_experience, resume_url) VALUES (:job_id, :full_name, :email, :linkedin_url, :education, :work_experience, :resume_url)"
    ).bindparams(job_id=job_id,
                 full_name=data['full_name'],
                 email=data['email'],
                 linkedin_url=data['linkedin_url'],
                 education=data['education'],
                 work_experience=data['work_experience'],
                 resume_url=data['resume_url'])
    conn.execute(query)
