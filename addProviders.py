import csv

def addProviders(centreManager, userManager):
    centres = centreManager.getHealthCentres()
    for centre in centres:
        with open("provider_health_centre.csv") as w:
            reader = csv.DictReader(w)
            for row in reader:
                # provider_email,health_centre_name
                if row['health_centre_name'] == centre.getName():
                    centre.addProvider(userManager.getID(row['provider_email']))
    return centreManager