import csv
from users import User, Patient, HealthProvider
from healthCentre import HealthCentre
def initialise_users():
    users = []
    with open('provider.csv') as w:
        reader = csv.DictReader(w)
        for row in reader:
            # def __init__(self, email, password, providerNum, profession, rating, workingHours, centres):
            provider = HealthProvider(row['provider_email'], row['password'], "", row['provider_type'], 0, 0, [])
            users.append(provider)
    with open('patient.csv') as w:
        reader = csv.DictReader(w)
        for row in reader:
            patient = Patient(row['patient_email'], row['password'], "0123456789")
            users.append(patient)
    return users



def initialise_health_centres():
    healthCentres = []
    # def __init__(self, name, suburb, phone, abn, rating, providers, centre_type):
    # centre_type,abn,name,phone,suburb
    with open('health_centres.csv') as w:
        reader = csv.DictReader(w)
        for row in reader:
            centre = HealthCentre(row['name'], row['suburb'], row['phone'], row['abn'], 0, [], row['centre_type'])
            healthCentres.append(centre)
    return healthCentres