from flask import Flask
from flask_login import LoginManager
from userManager import UserManager
from centreManager import CentreManager
from appointmentManager import AppointmentManager

app = Flask(__name__)
app.config["SECRET_KEY"] = "Highly secret key"

centreManager = CentreManager()
userManager = UserManager(centreManager)
appointmentManager = AppointmentManager()

login_manager = LoginManager()
login_manager.init_app(app)
