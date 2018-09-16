class Appointment(object):
	def __init__(self, provider, patient, date, time, reason):
		self._provider = provider
		self._patient = patient
		self._date = date
		self._time = time
		self._reason = reason
	@property
	def provider(self):
		return self._provider

	@property
	def patient(self):
		return self._patient

	@property
	def date(self):
		return self._date

	@property
	def time(self):
		return self._time

	@property
	def reason(self):
		return self._reason
	
	
	
	
	
	