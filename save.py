import pickle

def saveData(centreManager, userManager, appointmentManager):
    # write objects to file
    pickle.dump(centreManager, open("pickleFiles/centreManager.p", "wb"))
    pickle.dump(userManager, open("pickleFiles/userManager.p", "wb"))
    pickle.dump(appointmentManager, open("pickleFiles/appointmentManager.p", "wb"))