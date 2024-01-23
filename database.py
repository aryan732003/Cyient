from sqlalchemy import create_engine, text

db_connection_string = "mysql+pymysql://79xtwlltb4x3wf7okeac:pscale_pw_HwJbP3Odm1W0Ae9LNZmgsfGuWbIpgGQCfxBlixHNHKz@aws.connect.psdb.cloud/website?charset=utf8mb4"

engine = create_engine(db_connection_string,
                       connect_args={"ssl": {
                           "ssl_ca": "/etc/ssl/cert.pem"
                       }})


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