from abc import ABC, abstractmethod

class User(ABC):

    @abstractmethod
    def __init__(self, email, password, patient):
        self._email = email
        self._password = password
        self._isPatient = patient
        self._appointments = []

    def is_active(self):
        return True

    def get_id(self):
        return self._email

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False

    def isPatient(self):
        return self._isPatient

    def get_password(self):
        return self._password

    def addAppointment(self, appointment):
        self._appointments.append(appointment)

    def getListOfAppointments(self):
        return self._appointments

    def set_email(self, email):
        self._email = email
        return self._email

    def set_password(self, password):
        self._password = password
        return self._password

class Patient(User):
    def __init__(self, email, password, medicare):
        super().__init__(email, password, True)
        self._medicare = medicare

    def get_medicare(self):
        return self._medicare

    def set_medicare(self, medicare):
        self._medicare = medicare
        return self._medicare

class HealthProvider(User):
    def __init__(self, email, password, providerNum, profession, workingHours, centres):
        super().__init__(email, password, False)
        self._providerNum = providerNum
        self._profession = profession
        self._overallRating = 5
        self._listOfRatings = {}
        self._workingHours = workingHours
        self._centres = []

    # private function only used by own class functions
    def _getAverageOfDict(self, dictionary):
        total = 0
        count = 0
        for key, value in dictionary.items():
            total += value
            count += 1
        return int(total / count)

    def addCentre(self, centre):
        self._centres.append(centre)

    def getListOfCentres(self):
        return self._centres

    def getProfession(self):
        return self._profession

    def get_providerNum(self):
        return self._providerNum

    def updateRating(self, username, newRating):
        self._listOfRatings[username] = newRating
        self._overallRating = self._getAverageOfDict(self._listOfRatings)
        return self._overallRating    

    def get_rating(self):
        return self._overallRating


    def get_workingHours(self):
        return self._workingHours

    def set_providerNum(self, providerNum):
        self._providerNum = providerNum
        return self._providerNum

    def set_profession(self, profession):
        self._profession = profession
        return self._profession
