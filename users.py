

class User():
	def __init__(self, email, password, patient):
		self._email = email
		self._password = password
		self._isPatient = patient
	def is_active(self):
		return True
	def get_id(self):
		return self._email

	def is_authenticated(self):
		return self.authenticated 
	def is_anonymous(self):
		return False
	def isPatient(self):
		return _isPatient
	def get_password(self):
		return self._password

class Patient(User):
	def __init__(self, email, password, medicare):
		super().__init__(email, password, True)
		self._medicare = medicare

class HealthProvider(User):
	def __init__(self, email, password, providerNum, profession, rating, workingHours, centres):
		super().__init__(email, password, False)
		self._providerNum = providerNum
		self._profession = profession
		self._rating = rating
		self._workingHours = workingHours
		self._centres = centres


