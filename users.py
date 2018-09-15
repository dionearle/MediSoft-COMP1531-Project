from flask_login import UserMixin

class User():
	def __init__(self, email, password):
		self._email = email
		self._password = password
	def is_active(self):
		return True
	def get_id(self):
		return self._email

	def is_authenticated(self):
		return self.authenticated 
	def is_anonymous(self):
		return False