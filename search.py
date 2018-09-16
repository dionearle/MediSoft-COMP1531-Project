from server import centreManager, userManager
from centreManager import CentreManager
from userManager import UserManager

def searchFiles(searchTerm, option):

    found = False
    searchTerm = searchTerm.lower()
    if (option == "healthCentre" or option == "suburb"):
        resultArray = []
        resultDict = {}
        if (option == "healthCentre"):
            centres = centreManager.searchHealthCentresByName(searchTerm)
        else:
            centres = centreManager.searchHealthCentresBySuburb(searchTerm)
        if centres:
            for centre in centres:
                found = True
                resultDict["typeCentre"] = centre.getCentreType()
                resultDict["abn"] = centre.getABN()
                resultDict["name"] = centre.getName()
                resultDict["phone"] = centre.getPhone()
                resultDict["suburb"] = centre.getSuburb()
                resultArray.append(resultDict.copy())


        if found == True:
            returnDict = [found, resultArray]
            return returnDict
        else:
            returnDict = [found, []]
            return returnDict
    elif (option == "healthProvider" or option == "service"):
        resultArray = []
        resultDict = {}

        if option == "healthProvider":
            providers = userManager.searchID(searchTerm)
        else:
            providers = userManager.searchProfession(searchTerm)
        if providers:
            for provider in providers:
                centres = provider.getListOfCentres()
                for centre in centres:
                    found = True
                    returnArray = searchFiles(centre[0].getName(), "healthCentre")
                    returnDict = returnArray[1][0]
                    returnDict["user"] = provider.get_id()
                    returnDict["service"] = provider.getProfession()
                    resultArray.append(returnDict)

        if found == True:
            returnDict = [found, resultArray]
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
            return returnDict
    return [False, []]


if __name__ == '__main__':
    print(str(searchFiles("Hospital", "healthCentre")))
