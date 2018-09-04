from server import app, valid_time
from flask import request, render_template
from Calculator import Calculator


@app.route('/', methods=['POST', 'GET'])
def interest_total():
    message = ''
    if request.method == 'POST':
        initial = int(request.form["initial"])
        rate = int(request.form["rate"])
        time = int(request.form["time"])
        if (initial < 0):
            message = "Invalid amount invested"
        elif (rate < 0):
            message = "Invalid interest rate"
        elif (time < 0):
            message = "Invalid time invested"
        else:
            new1 = Calculator(initial, rate)
            total = int(new1.total_interest(time))
            message = "The calculation was successful, and the total interest is $" + str(total) + "\n"
    return render_template('interest_form.html', calc_total=True, message = message)


@app.route('/time', methods=['POST', 'GET'])
def time_interest():
    message = ''
    if request.method == 'POST':
        initial = int(request.form["initial"])
        rate = int(request.form["rate"])
        total = int(request.form["total"])
        if (initial < 0):
            message = "Invalid amount invested"
        elif (rate < 0):
            message = "Invalid interest rate"
        elif (total < 0):
            message = "Invalid total interest gained"
        else:
            new1 = Calculator(initial, rate)
            time = int(new1.time_required(total))
            message = "The calculation was successful, and the time invested is " + str(time) + " years\n"
    return render_template('interest_form.html', calc_time=True, message = message)


@app.route('/credits', methods=['GET'])
def credits():
    return render_template('credits.html', name="Dion", year = "2018")
