from initialise import initialise_health_centres

class centreManager(object):
	def __init__(self):
		self._healthCentres = initialise_health_centres()

	def addHealthCentre(self, healthCentre):
		self._healthCentres.append(healthCentre)
        
	def getHealthCentres(self):
		return self._healthCentres

	def searchHealthCentresByName(self, name):
		for centre in self._healthCentres:
			if centre.getName(name) == name:
				return centre
		return None
