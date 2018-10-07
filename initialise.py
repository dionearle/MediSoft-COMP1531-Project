import csv
from users import User, Patient, HealthProvider
from healthCentre import HealthCentre

def getCentres(centreManager, email):
    # open provider_health_centres.csv and find health centres matching email given
    # run centreManager.search and get health centre and append it to array
    # return this array
    centresArray = []
    with open("provider_health_centre.csv") as w:
        reader = csv.DictReader(w)
        for row in reader:
            # provider_email,health_centre_name
            if row['provider_email'] == email:
                centre = centreManager.searchHealthCentresByName(row['health_centre_name'])
                centresArray.append(centre[0])
    return centresArray



def initialise_users(centreManager):
    users = []
    with open('provider.csv') as w:
        reader = csv.DictReader(w)
        for row in reader:
            # def __init__(self, email, password, first_name, last_name, phone, providerNum, profession, rating, workingHours, centres):
            provider = HealthProvider(row['provider_email'], row['password'], row['first_name'], row['last_name'], row['phone'], row['providerNum'], row['provider_type'], row['workingHours'], [])
            centres = getCentres(centreManager, row['provider_email'])
            for centre in centres:
                provider.addCentre(centre)
            users.append(provider)
    with open('patient.csv') as w:
        reader = csv.DictReader(w)
        for row in reader:
            patient = Patient(row['patient_email'], row['password'], row['first_name'], row['last_name'], row['phone'], row['medicare'])
            users.append(patient)
    return users

def initialise_health_centres():
    healthCentres = []
    # def __init__(self, name, suburb, phone, abn, rating, providers, centre_type):
    # centre_type,abn,name,phone,suburb
    with open('health_centres.csv') as w:
        reader = csv.DictReader(w)
        for row in reader:
            centre = HealthCentre(row['name'], row['suburb'], row['phone'], row['abn'], [], row['centre_type'])
            healthCentres.append(centre)
    return healthCentres
