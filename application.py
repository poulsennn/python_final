from flask import Flask, render_template, request

app = Flask(__name__)

def bodyfat_M(sf_sum, age):
    res = 0.465 + 0.18*sf_sum - (0.0002406*sf_sum)**2 + 0.06619*age
    return res

def bodyfat_F(sf_sum):
    res = 13.1 + 0.12*sf_sum
    return res


calculations = []


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        input_date = request.form.get("date")
        input_sex = request.form.get("sex")
        input_age = int(request.form.get("age"))
        input_weight = float(request.form.get("weight"))
        input_pec = float(request.form.get("pectoralis"))
        input_tri = float(request.form.get("triceps"))
        input_sub = float(request.form.get("subscapular"))
        input_axi = float(request.form.get("axillary"))
        input_sup = float(request.form.get("suprailliac"))
        input_abd = float(request.form.get("abdomen"))
        input_thi = float(request.form.get("thigh"))
        input_sf_sum = input_pec + input_tri + input_sub + input_axi +\
        input_sup + input_abd + input_thi
        if input_sex == "M":
            bf_calc = bodyfat_M(input_sf_sum, input_age)
        else:
            bf_calc = bodyfat_F(input_sf_sum)
        fat_mass = input_weight*(bf_calc/100)
        fat_free_mass = input_weight - fat_mass
        calculations.append([input_date, input_sex, input_age, input_weight,\
        input_pec, input_tri, input_sub, input_axi, input_sup, input_abd,\
        input_thi, round(input_sf_sum, 1), round(bf_calc, 1),\
        round(fat_free_mass, 1), round(fat_mass, 1)])
    return render_template("index.html", calculations=calculations)


if __name__ == "__main__":
    app.run()
