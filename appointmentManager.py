class AppointmentManager(object):
	def __init__(self):
		self._appointments = []

	def getAppointments(self):
		return self._appointments

	def addAppointment(self, appointment):
		self._appointments.append(appointment)
