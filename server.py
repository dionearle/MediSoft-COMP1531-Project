from flask import Flask
from flask_login import LoginManager
from userManager import UserManager
from centreManager import CentreManager
from appointmentManager import AppointmentManager
from addProviders import addProviders
app = Flask(__name__)
app.config["SECRET_KEY"] = "Highly secret key"

centreInitialManager = CentreManager()
userManager = UserManager(centreInitialManager)
centreManager = addProviders(centreInitialManager, userManager)

print(str(centreManager.getHealthCentres[0].getName()))
test = centreManager.getHealthCentres()[0].getProviders()
for i in test:
	print(str(i.get_id()))

login_manager = LoginManager()
login_manager.init_app(app)
