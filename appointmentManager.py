from appointment import Appointment

# 	def __init__(self, provider, patient, date, time)
class AppointmentManager():
	def addAppointment(self, userManager, provider_email, patient_email, date, time, reason):
		appointment = Appointment(provider_email, patient_email, date, time, reason)

		users = userManager.getUsers()
		for user in users:
			if user.isPatient() == True and user.get_id() == patient_email:
				user.addAppointment(appointment)
			elif user.isPatient() == False and user.get_id() == provider_email:

				user.addAppointment(appointment)
	def getAppointments(self, user):
		return user.getListOfAppointments()

	def getAppointmentUsingDate(self, user, date, time):
		Appointments = user.getListOfAppointments()
		for appointment in Appointments:
			if appointment.date == date and appointment.time == time:
				return appointment
