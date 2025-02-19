from initialise import initialise_health_centres

class CentreManager(object):
	def __init__(self):
		self._healthCentres = initialise_health_centres()

	def addHealthCentre(self, healthCentre):
		self._healthCentres.append(healthCentre)

	def getHealthCentres(self):
		return self._healthCentres

	def searchHealthCentresByName(self, name):
		returnArray = []
		name = name.lower()
		for centre in self._healthCentres:
			if centre.getName().lower().find(name) != -1:
				returnArray.append(centre)
		return returnArray

	def searchHealthCentresByObject(self, centre):
		for index, localCentre in enumerate(self._healthCentres):
			if localCentre is centre:
				return index

	def searchHealthCentresBySuburb(self, suburb):
		returnArray = []
		for centre in self._healthCentres:
			if centre.getSuburb().lower().find(suburb) != -1:
				returnArray.append(centre)
		return returnArray

	def addProviders(self, UserManager):
		Users = UserManager.getUsers()
		for user in Users:
			if user.isPatient() == False:
				for centre in user.getListOfCentres():
					self._healthCentres[self.searchHealthCentresByObject(centre)].addProvider(user)
