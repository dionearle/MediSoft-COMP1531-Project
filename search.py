def searchFiles(searchTerm, option):

    found = False
    if (option == "healthCentre"):
        resultArray = []
        resultDict = {}
        with open("health_centres.csv", "r") as w:
            readLinesArray = w.readlines()
            for i in range(len(readLinesArray)):
# 'Hospital', '1111', ' Sydney Children Hospital', '93821111 ', 'Randwick'
                (typeCentre, postcode, name, phone, suburb ) = readLinesArray[i].split(', ')
                if (name.find(searchTerm) != -1 or searchTerm == ""):
                    found = True
                    resultDict["typeCentre"] = typeCentre[1:-1]
                    resultDict["postcode"] = postcode[1:-1]
                    resultDict["name"] = name[1:-1]
                    resultDict["phone"] = phone[1:-2]
                    resultDict["suburb"] = suburb[1:-2]
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
        with open("provider_health_centre.csv"):
            readLinesArray = w.readlines()
            for i in range(len(readLinesArray)):
                (email, centre) = readLinesArray[i].split(',')
                if (name.find(searchTerm) != -1 or searchTerm == ""):
                    found = True
                    
    return [False, []]   


if __name__ == '__main__':
    print(str(searchFiles("Hospital", "healthCentre")))