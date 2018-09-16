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
        print("adding appointment!")
        self._appointments.append(appointment)

    def getListOfAppointments(self):
        return self._appointments

class Patient(User):
    def __init__(self, email, password, medicare):
        super().__init__(email, password, True)
        self._medicare = medicare

class HealthProvider(User):
    def __init__(self, email, password, providerNum, profession, rating, workingHours, centres):
        super().__init__(email, password, False)
        self._providerNum = providerNum
        self._profession = profession
        self._rating = rating
        self._workingHours = workingHours
        self._centres = []

    def addCentre(self, centre):
        self._centres.append(centre)

    def getListOfCentres(self):
        return self._centres

    def getProfession(self):
        return self._profession
