class HealthCentre(object):
	# centre_type,abn,name,phone,suburb
	def __init__(self, name, suburb, phone, abn, rating, providers, centre_type):
		self._name = name
		self._suburb = suburb
		self._phone = phone
		self._abn = abn
		self._rating = rating
		self._providers = providers
		self._centre_type = centre_type

