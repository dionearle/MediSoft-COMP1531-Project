from appointment import Appointment

# 	def __init__(self, provider, patient, date, time)
class AppointmentManager():
	def checkPreviousAppointment(self, user, appointment):
		if user.isPatient() == True: # if user is patient
			for userAppointment in user.getListOfAppointments():
				if userAppointment.patient == user.get_id() and userAppointment.date == appointment.date\
					and userAppointment.time == appointment.time:

					return True
		else: # user is provider
			for userAppointment in user.getListOfAppointments():
				if userAppointment.provider == user.get_id() and userAppointment.date == appointment.date\
					and userAppointment.time == appointment.time:

					return True
		return False


	def addAppointment(self, userManager, provider_email, patient_email, date, time, reason):


		appointment = Appointment(provider_email, patient_email, date, time, reason)
		appointment.addProviderList(provider_email)

		users = userManager.getUsers()
		for user in users:
			if user.isPatient() == True and user.get_id() == patient_email\
				and self.checkPreviousAppointment(user, appointment) == False:

				user.addAppointment(appointment)
			elif user.isPatient() == False and user.get_id() == provider_email\
				and self.checkPreviousAppointment(user, appointment) == False:

				user.addAppointment(appointment)
			elif self.checkPreviousAppointment(user, appointment) == True:
				return False # return that there was an error
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




