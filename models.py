from flask_login import UserMixin
from sqlalchemy import text
from database import run_sql_query

class User(UserMixin):
  def __init__(self,user_id,name,email):
    self.id=user_id
    self.name=name
    self.email=email

  @staticmethod
  def get(user_id):
    query=text("SELECT name,email FROM users where id=:user_id")
    parameters={"user_id":user_id}
    result=run_sql_query(query,parameters)
    result=result.first()._asdict()
    return User(user_id,result["name"],result["email"])