class Appointment(object):
	def __init__(self, provider, patient, date, time):
		self._provider = provider
		self._patient = patient
		self._date = date
		self._time = time
	@property
	def provider(self):
		return self._provider
	
	