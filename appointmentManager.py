from appointment import Appointment
from datetime import datetime, timedelta
# 	def __init__(self, provider, patient, date, time)
class AppointmentManager():
	def checkPreviousAppointment(self, user, appointment, patient_email, provider_email):
		if user.isPatient() == True: # if user is patient
			for userAppointment in user.getListOfAppointments():
				if patient_email == user.get_id() and userAppointment.date == appointment.date\
					and userAppointment.time == appointment.time:

					return True
		else: # user is provider
			for userAppointment in user.getListOfAppointments():
				if provider_email == user.get_id() and userAppointment.date == appointment.date\
					and userAppointment.time == appointment.time:

					return True
		return False


	def addAppointment(self, userManager, provider_email, patient_email, time, date, reason):
		# check that date isn't in the past
		datetime_object = datetime.strptime(date, "%m/%d/%Y")
		if (datetime_object - datetime.now()).total_seconds() < 0:
			return "Date in the past"

		# check that the patient email isn't a provider
		if (userManager.getID(patient_email).isPatient() == False):
			return "Provider making appointment"


		appointment = Appointment(provider_email, patient_email, date, time, reason)

		users = userManager.getUsers()

		for user in users:
			if self.checkPreviousAppointment(user, appointment, patient_email, provider_email) == False:

				if user.isPatient() == True and user.get_id() == patient_email:

					user.addAppointment(appointment)
				elif user.isPatient() == False and user.get_id() == provider_email:

					user.addAppointment(appointment)
			else:
				return "Time Slot Taken" # return that there was an error
		return True # return that it succeeded

		
	def getAppointments(self, user):
		return user.getListOfAppointments()

	def getAppointmentUsingDate(self, user, date, time):
		Appointments = user.getListOfAppointments()
		for appointment in Appointments:
			if appointment.date == date and appointment.time == time:
				return appointment

	def updateAppointment(self, appointment, notes, medicine):
		appointment.addNotes = notes
		appointment.addMedicine = medicine

	def appointmentCompleted(self, patient, provider):
		for appointment in patient.getListOfAppointments():
			if appointment.accessed == True and appointment.provider == provider:
				return True
		return False




