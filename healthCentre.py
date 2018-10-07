class HealthCentre(object):
	# centre_type,abn,name,phone,suburb
	def __init__(self, name, suburb, phone, abn, providers, centre_type):
		self._name = name
		self._suburb = suburb
		self._phone = phone
		self._abn = abn
		self._listOfRatings = {}
		self._overallRating = 5
		self._providers = providers
		self._centre_type = centre_type

	# private function only used by own class functions
	def _getAverageOfDict(self, dictionary):
		total = 0
		count = 0
		for key, value in dictionary.items():
			total += value
			count += 1
		return int(total / count)

	def getName(self):
		return self._name

	def getSuburb(self):
		return self._suburb
	def getPhone(self):
		return self._phone
	def getABN(self):
		return self._abn
	def getRating(self):
		return self._overallRating
	def updateRating(self, username, newRating):
		self._listOfRatings[username] = newRating
		self._overallRating = self._getAverageOfDict(self._listOfRatings)
		return self._overallRating

	def getProviders(self):
		return self._providers
	def getCentreType(self):
		return self._centre_type
	def addProvider(self, provider):
		self._providers.append(provider)
	def __str__(self):
		return "Health Centre " + self._name + ": " + self._suburb + ", " + self._phone + ", " + \
		self._abn + ", " + str(self._rating) + ", " + self._centre_type + ", providers: " + str(self._providers)
