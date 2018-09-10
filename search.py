def searchFiles(searchTerm, option):
    resultArray = []
    resultDict = {}
    found = False
    # if (option == "healthProvider"):
    #     with open("provider_health_centre.csv", "r") as w:
    #         readLinesArray = w.readlines()
    #         for i in range(12):
    #             (email, centre) = readLinesArray[i].split(',')
    #             if (email.find(searchTerm) != -1):
    #                 found = True
    #                 resultDict["email"] = email
    #                 resultDict["centre"] = centre
    #                 resultEmail.append(email)
    #                 resultCentre.append(centre)
                    
    #     if found == True:
    #         returnDict = [found, resultEmail, resultCentre]
    #         return returnDict
    #     else:
    #         returnDict = [found, [], []]
    #         return returnDict
    if (option == "healthCentre"):
        with open("health_centres.csv", "r") as w:
            readLinesArray = w.readlines()
            for i in range(6):
# 'Hospital', '1111', ' Sydney Children Hospital', '93821111 ', 'Randwick'
                (typeCentre, postcode, name, phone, suburb ) = readLinesArray[i].split(', ')
                if (name.find(searchTerm) != -1):
                    found = True
                    resultDict["typeCentre"] = typeCentre[1:-1]
                    resultDict["postcode"] = postcode[1:-1]
                    resultDict["name"] = name
                    resultDict["phone"] = phone[1:-1]
                    resultDict["suburb"] = suburb[1:-1]
                    resultArray.append(resultDict)
                    
        if found == True:
            returnDict = [found, resultArray]
            return returnDict
        else:
            returnDict = [found, []]
            return returnDict
    return [False, []]   


if __name__ == '__main__':
    print(str(searchFiles("Hospital", "healthCentre")))