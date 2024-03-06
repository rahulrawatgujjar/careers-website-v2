from flask import Flask, render_template, request, jsonify,redirect,url_for,flash, Blueprint
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from database import run_sql_query
from sqlalchemy import text
from models import User

auth_routes= Blueprint("auth",__name__)


@auth_routes.route("/login",methods=["GET","POST"])
def login():
  if request.method=="POST":
    data=request.get_json()
    email,password=data.get("email"),data.get("password")
    query=text("SELECT id,name,email,password FROM users WHERE email=:email")
    parameters={
      "email":email
    }
    result=run_sql_query(query,parameters).first()
    if result:
      result=result._asdict()
      if check_password_hash(result["password"],password):
        user=User(user_id=result["id"],name=result["name"],email=result["email"])
        login_user(user)
        return jsonify({"valid":True, "redirectUrl":"/"})
      else:
        return jsonify({"valid":False, "error":"Invalid Password"})
    else:
      return jsonify({"valid":False,"error":"Invalid Username"})
  return render_template("login.html")


@auth_routes.route("/register",methods=["GET","POST"])
def register():
  if request.method=="POST":
    data=request.get_json()
    name,email,password=data["name"],data["email"],data["password"]
    hashed_password=generate_password_hash(password)

    # checking that user already exist or not
    query=text("SELECT id,name,email,password FROM users WHERE email=:email")
    parameters={
      "email":email
    }
    result= run_sql_query(query,parameters).first()
    if result:
      return jsonify({"valid":False, "error":"Email alrgeady exists"})
    else:
      query=text("INSERT INTO users(name,email,password) VALUES(:name,:email,:password)")
      parameters={
        "name":name,
        "email":email,
        "password":hashed_password
      }
      run_sql_query(query,parameters)
      flash("Registration successfull. Please login.","success")
      return jsonify({"valid":True, "redirectUrl":"/login"})
  return render_template("register.html")



@auth_routes.route("/logout")
@login_required
def logout():
  logout_user()
  return redirect(url_for("auth.login"))


@auth_routes.route("/check_login")
def check_login():
  if current_user.is_authenticated:
    return jsonify({"logged_in":True})
  else:
    return jsonify({"logged_in":False})
  