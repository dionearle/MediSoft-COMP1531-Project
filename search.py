

def searchFiles(searchTerm, option):

    found = False
    searchTerm = searchTerm.lower()
    if (option == "healthCentre" or option == "suburb"):
        resultArray = []
        resultDict = {}
        with open("health_centres.csv", "r") as w:
            readLinesArray = w.readlines()
            for i in range(len(readLinesArray)):
# 'Hospital', '1111', ' Sydney Children Hospital', '93821111 ', 'Randwick'
                (typeCentre, postcode, name, phone, suburb) = readLinesArray[i].split(',')
                print("name: " + name)
                if (option == "healthCentre"):
                    term = name
                elif (option == "suburb"):
                    term = suburb
                term = term.lower()
                if (term.find(searchTerm) != -1 or searchTerm == ""):
                    found = True
                    resultDict["typeCentre"] = typeCentre
                    resultDict["postcode"] = postcode
                    resultDict["name"] = name
                    resultDict["phone"] = phone
                    resultDict["suburb"] = suburb
                    resultArray.append(resultDict.copy())
        if found == True:
            returnDict = [found, resultArray]
            return returnDict
        else:
            returnDict = [found, []]
            return returnDict
    elif (option == "healthProvider"):
        resultArray = []
        resultDict = {}
        with open("provider_health_centre.csv") as w:
            readLinesArray = w.readlines()
            for i in range(len(readLinesArray)):
                (email, centre) = readLinesArray[i].split(',')
                email = email.lower()
                if (email.find(searchTerm) != -1 or searchTerm == ""):
                    found = True
                    centre = centre[:-1] # delete newline character
                    returnArray = searchFiles(centre, "healthCentre")
                    returnDict = returnArray[1][0]
                    returnDict["user"] = email
                    resultArray.append(returnDict)
        if found == True:
            returnDict = [found, resultArray]
            print("returnDict: " + str(returnDict))
            return returnDict
    elif option == "service":
        resultArray = []
        resultDict = {}
        with open("provider.csv") as w:
            readLinesArray = w.readlines()
            for i in range(len(readLinesArray)):
                (email, password, service) = readLinesArray[i].split(',')
                service = service.lower()
                if (service.find(searchTerm) != -1 or searchTerm == ""):
                    found = True
                    service = service[:-1] # delete newline character
                    returnArray = searchFiles(email, "healthProvider")
                    returnDict = returnArray[1][0]
                    returnDict["service"] = service
                    resultArray.append(returnDict)
        if found == True:
            returnDict = [found, resultArray]
            print("returnDict: " + str(returnDict))
            return returnDict
    return [False, []]


if __name__ == '__main__':
    print(str(searchFiles("Hospital", "healthCentre")))
