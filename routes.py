from server import app
from flask import request, render_template
from users import User, Patient, Provider


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        with open("patient.csv", "r") as w:
            patient = False
            readLinesArray = w.readlines() # interpret data in patient.csv as an array
            for i in range(4):
                (email, password) = readLinesArray[i].split(',') # split data into email and password
                password = password[:-1] # delete newline character
                # if email and password match
                if email == request.form["loginEmail"] and \
                    password == request.form["loginPassword"]:

                    patient = True # to detect later whether to check providers.csv file or not
                    break
            
            if patient == True: 
                userLoggedIn = Patient(email, password) # initialise Patient class
                return render_template("loginPost.html", userType="Patient", success=True) # return html file
        with open("provider.csv", "r") as w:
            provider = False # for detecting whether login failed or not later
            readLinesArray = w.readlines() # interpret data in provider.csv as an array
            for i in range(8):
                (name, password, specialisation) = readLinesArray[i].split(',') # pretty much same as above
                specialisation = specialisation[:-1]
                if name == request.form["loginEmail"] and \
                    password == request.form["loginPassword"]:
                    provider = True
                    break
            if provider == True:
                userLoggedIn = Provider(name, password, specialisation) # initialise Provider class
                return render_template("loginPost.html", userType="Provider", success=True) # return html file

        return render_template("loginPost.html", success=False) # if login failed, return an alert saying "Wrong email/password"
    return render_template("base.html") # runs when the user first opens the page