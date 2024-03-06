from flask import Flask
from app import core_routes
import os 
# from dotenv import load_dotenv
from app import core_routes
from auth_routes import auth_routes
from flask_login import LoginManager
from models import User

app= Flask(__name__)

# load_dotenv()
app.config["SECRET_KEY"]=os.environ["SECRET_KEY"]

login_manager = LoginManager(app)
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


app.register_blueprint(core_routes)
app.register_blueprint(auth_routes)

if __name__=="__main__":
  app.run(host="0.0.0.0",debug=True)