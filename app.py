from flask import Flask, jsonify, render_template
from flask import request
from database import load_job_from_db, load_jobs_from_db, add_application_to_db

app = Flask(__name__)


@app.route("/")
def hello_jovian():
  return render_template('homepage.html')


@app.route("/api/jobs")
def list_jobs():
  jobs = load_jobs_from_db()
  return jsonify(jobs)


@app.route("/job")
def show_jobs():
  jobs = load_jobs_from_db()
  return render_template('job.html', jobs=jobs)


@app.route("/job/<id>")
def show_job(id):
  job = load_job_from_db(id)
  if not job:
    return "Not Found", 404

  return render_template('jobpage.html', job=job)


@app.route("/job/<int:job_id>/form")
def form(job_id):
  job = load_job_from_db(job_id)
  return render_template('application_form.html', job=job)


@app.route("/job/<int:job_id>/form/apply", methods=['post'])
def apply_to_job(job_id):
  data = request.form
  job = load_job_from_db(job_id)
  add_application_to_db(job_id, data)
  return render_template('submitted.html', job=job, application=data)


if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
