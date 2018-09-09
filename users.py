class User(object):
	def __init__(self, email, password, activated):
		# Initialise email and password
		self._email = email
		self._password = password
		self._activated = activated
	def __str__(self):
		return str(self._email)

	def getActivated(self):
		return self._activated
		
	@property
	def email(self):
		return self._email

class Patient(User):
	def __init__(self, email, password, activated):
		super().__init__(email, password, activated)
	def __str__(self):
		return "Patient: " + super().__str__()

class Provider(User):
	def __init__(self, email, password, specialisation, activated):
		super().__init__(email, password, activated)
		self._specialisation = specialisation
	def __str__(self):
		return "Provider: " + super().__str__() + " " + self._specialisation


	