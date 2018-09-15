
def getProviders():
    resultArray = []
    resultDict = {}
    with open("provider_health_centre.csv") as w:
            readLinesArray = w.readlines()
            for i in range(len(readLinesArray)):
                (email, centre) = readLinesArray[i].split(',')
                email = email.lower()
                returnDict["user"] = email
                returnDict["centre"] = centre
                resultArray.append(returnDict["centre"])  
    return resultArray           


