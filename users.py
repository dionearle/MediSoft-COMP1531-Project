class User(object):
	def __init__(self, email, password):
		# Initialise email and password
		self._email = email
		self._password = password
	def __str__(self):
		return str(self._email)

class Patient(User):
	def __init__(self, email, password):
		super().__init__(email, password)
	def __str__(self):
		return "Patient: " + super().__str__()

class Provider(User):
	def __init__(self, email, password, specialisation):
		super().__init__(email, password)
		self._specialisation = specialisation
	def __str__(self):
		return "Provider: " + super().__str__() + " " + self._specialisation