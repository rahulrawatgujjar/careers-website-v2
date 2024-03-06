from flask import Flask, render_template, jsonify, request, Blueprint
from database import load_jobs_from_db, load_job_from_db, add_application_to_db,applied_and_unapplied_jobs
from flask_login import login_required,current_user

core_routes= Blueprint("core",__name__)

@core_routes.route("/")
def hello_world():
  jobs=[]
  applied_jobs=[]
  if not current_user.is_authenticated:
    jobs = load_jobs_from_db()
  else:
    applied_jobs,jobs= applied_and_unapplied_jobs(current_user.id)
  return render_template("home.html", jobs=jobs,applied_jobs=applied_jobs, is_authenticated= current_user.is_authenticated)

@core_routes.route("/api/jobs")
def list_jobs():
  jobs = load_jobs_from_db()
  return jsonify(jobs)


@core_routes.route("/job/<id>")
@login_required
def show_job(id):
  job = load_job_from_db(id)
  if job:
    return render_template("jobpage.html", job=job)
  else:
    return "Not found", 404


@core_routes.route("/job/<id>/apply",methods=["post"])
@login_required
def apply_to_job(id):
  data=request.form
  job=load_job_from_db(id)
  add_application_to_db(id,data,current_user.id)
  return render_template("application_submitted.html", application=data, job=job)

