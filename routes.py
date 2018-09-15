from server import app
from flask import request, render_template
from users import User, Patient, Provider
from search import searchFiles


@app.route('/', methods=['GET','POST'])
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
                userLoggedIn = Patient(email, password, True) # initialise Patient class
                return render_template("loginPost.html", userType="Patient", success=True, username=userLoggedIn.email) # return html file
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
                userLoggedIn = Provider(name, password, specialisation, True) # initialise Provider class
                return render_template("loginPost.html", userType="Provider", success=True, username=userLoggedIn.email) # return html file

        return render_template("loginPost.html", success=False) # if login failed, return an alert saying "Wrong email/password"
    return render_template("base.html") # runs when the user first opens the page

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == "POST":
        print("radio: " + str(request.form["radioSearch"]))
        searchArray = searchFiles(request.form["searchText"], request.form["radioSearch"])
        if (searchArray[0] == True):
            return render_template("searchResults.html", searchArray=searchArray, option=request.form["radioSearch"])

    return render_template('searchBox.html')

@app.route('/profile/<name>', methods=['GET', 'POST'])
def profile(name):
    if request.method == "POST":
        option = request.form["option"]
        if option == "healthCentre" or option == "suburb":
            typeCentre = request.form["typeCentre"]
            name = request.form["name"]
            postcode = request.form["postcode"]
            phone = request.form["phone"]
            suburb = request.form["suburb"]
            return render_template("profile.html",option=option, typeCentre=typeCentre, name=name, postcode=postcode,
            phone=phone, suburb=suburb, rating = 0)
        elif option == "healthProvider":
            email = request.form["user"]
            typeCentre = request.form["typeCentre"]
            name = request.form["name"]
            postcode = request.form["postcode"]
            phone = request.form["phone"]
            suburb = request.form["suburb"]
            return render_template("profile.html",option=option, email=email, typeCentre=typeCentre, name=name, postcode=postcode,
            phone=phone, suburb=suburb, rating = 0)
        elif option == "service":
            email = request.form["user"]
            service = request.form["service"]
            typeCentre = request.form["typeCentre"]
            name = request.form["name"]
            postcode = request.form["postcode"]
            phone = request.form["phone"]
            suburb = request.form["suburb"]
            return render_template("profile.html",option=option, email=email, service=service, typeCentre=typeCentre, name=name, postcode=postcode,
            phone=phone, suburb=suburb, rating = 0)
    return render_template("profile.html")
