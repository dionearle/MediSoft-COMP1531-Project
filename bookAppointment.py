from server import userManager, centreManager
from appointment import Appointment

# 	def __init__(self, provider, patient, date, time)
def addAppointment(provider_email, patient_email, date, time):
	appointment = Appointment(provider_email, patient_email, date, time)
	users = userManager.getUsers()
	for user in users:
		if user.isPatient() == True and user.get_id() == patient_email:
			user.addAppointment(appointment)
		if user.isPatient() == False and user.get_id() == provider_email:
			user.addAppointment(appointment)
	