from initialise import initialise_users, initialise_health_centres

class UserManager(object):
	def __init__(self, centreManager):
		self._users = initialise_users(centreManager)
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
		
	def searchID(self, searchTerm):
		searchTerm = searchTerm.lower()
		returnArray = []
		for user in self._users:
			if user.get_id().lower().find(searchTerm) != -1 and user.isPatient() == False:
				returnArray.append(user)
		return returnArray

	def searchProfession(self, searchTerm):
		searchTerm = searchTerm.lower()
		returnArray = []
		for user in self._users:
			if user.isPatient() == False:
				if user.getProfession().lower().find(searchTerm) != -1:
					returnArray.append(user)
		return returnArray
