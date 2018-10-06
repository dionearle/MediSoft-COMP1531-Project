from flask import Flask
from flask_login import LoginManager
from userManager import UserManager
from centreManager import CentreManager
from appointmentManager import AppointmentManager
import pickle

app = Flask(__name__)
app.config["SECRET_KEY"] = "Highly secret key"

try:
	centreManager = pickle.load(open("pickleFiles/centreManager.p","rb"))
	userManager = pickle.load(open("pickleFiles/userManager.p", "rb"))
	appointmentManager = pickle.load(open("pickleFiles/appointmentManager.p", "rb"))
	print("used pickle!")
except FileNotFoundError:
	centreManager = CentreManager()
	userManager = UserManager(centreManager)
	appointmentManager = AppointmentManager()
	centreManager.addProviders(userManager)


login_manager = LoginManager()
login_manager.init_app(app)
