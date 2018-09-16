from initialise import initialise_users

class UserManager(object):
	def __init__(self):
		self._users = initialise_users()
		self._healthCentres = initialise_health_centres()
	def addUser(self, user):
		self._users.append(user)
	def getUsers(self):
		return self._users
	def __str__(self):
		return str(self._users)
	def correctCredentials(self, email, password):
		for user in self._users:
			if user.get_id() == email and user.get_password() == password:
				return True
		return False
	def getID(self, email):
		for user in self._users:
			if user.get_id() == email:
				return user