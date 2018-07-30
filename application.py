from flask import Flask, render_template, request

app = Flask(__name__)


def bmi(weight, height):
    res = weight / (height ** 2)
    return res


calculations = []


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        height = float(request.form.get("height"))
        weight = float(request.form.get("weight"))
        calculated_bmi = round(bmi(weight, height), 1)
        calculations.append(calculated_bmi)
    return render_template("index.html", calculations=calculations)


@app.route("/calculate", methods=["POST"])
def calculate():
    height = float(request.form.get("height"))
    weight = float(request.form.get("weight"))
    calculated_bmi = round(bmi(weight, height), 1)
    return render_template("calculate.html", calculated_bmi=calculated_bmi)
