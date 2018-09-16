class HealthCentre(object):
	# centre_type,abn,name,phone,suburb
	_providers = []
	def __init__(self, name, suburb, phone, abn, rating, centre_type):
		self._name = name
		self._suburb = suburb
		self._phone = phone
		self._abn = abn
		self._rating = rating
		self._centre_type = centre_type
	def getName(self):
		return self._name

	def getSuburb(self):
		return self._suburb

	def getPhone(self):
		return self._phone
	def getABN(self):
		return self._abn
	def getRating(self):
		return self._rating
	def getCentreType(self):
		return self._centre_type
	def addProvider(self, provider):
		self._providers.append(provider)
	def getProviders(self):
		return self._providers


