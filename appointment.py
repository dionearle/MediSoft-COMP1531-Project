class Appointment(object):
	def __init__(self, provider, patient, date, time, reason):
		self._provider = provider
		self._patient = patient
		self._date = date
		self._time = time
		self._reason = reason

		self._notes = None
		self._prescribedMedicine = None
		self._accessed = False

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

	@property
	def notes(self):
		return self._notes

	@notes.setter
	def notes(self, notes):
		self._notes = notes

	@property
	def prescribedMedicine(self):
		return self._prescribedMedicine

	@prescribedMedicine.setter
	def prescribedMedicine(self, prescribedMedicine):
		self._prescribedMedicine = prescribedMedicine

	@property
	def accessed(self):
		return self._accessed

	@accessed.setter
	def accessed(self, boolean):
		self._accessed = boolean


