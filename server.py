from flask import Flask
from flask_login import LoginManager
from userManager import UserManager
app = Flask(__name__)
app.config["SECRET_KEY"] = "Highly secret key"

userManager = UserManager()

login_manager = LoginManager()
login_manager.init_app(app)
