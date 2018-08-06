from flask import Flask, render_template, request  # For the app itself.
import pygal  # For making graphs.
from datetime import date  # For converting input to date format.

app = Flask(__name__)  # Define the app.

# Male bodyfat function.
# Takes sum of skinfolds and age as input and returns a bodyfat percentage.
def bodyfat_M(sf_sum, age):
    res = 0.465 + 0.18*sf_sum - (0.0002406*sf_sum)**2 + 0.06619*age
    return res

# Female bodyfat function.
# Takes sum of skinfolds as input and returns a bodyfat percentage.
def bodyfat_F(sf_sum):
    res = 13.1 + 0.12*sf_sum
    return res

# Local "database" containing all the input data.
date_data = []
weight_data = []
pec_data = []
tri_data = []
sub_data = []
axi_data = []
sup_data = []
abd_data = []
thi_data = []
bf_data = []
ffm_data = []
fm_data = []
calculations = []

# Define web path that can be called in browser and by an entry post.
@app.route("/", methods=["GET", "POST"])
# Main function of this path.
def index():
    try:
        # If path is called by an entry post:
        if request.method == "POST":
            # Save all input data as variables.
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
            # Calculate sum of input skinfolds.
            input_sf_sum = input_pec + input_tri + input_sub + input_axi +\
            input_sup + input_abd + input_thi
            # Calculate and save bodyfat percentage dependent on sex.
            if input_sex == "M":
                bf_calc = bodyfat_M(input_sf_sum, input_age)
            else:
                bf_calc = bodyfat_F(input_sf_sum)
            # Calculate and save fat and fat free mass.
            fat_mass = input_weight*(bf_calc/100)
            fat_free_mass = input_weight - fat_mass

            # Add all variables to the local "database"
            calculations.append([input_date, input_sex, input_age, input_weight,\
            input_pec, input_tri, input_sub, input_axi, input_sup, input_abd,\
            input_thi, round(input_sf_sum, 1), round(bf_calc, 1),\
            round(fat_free_mass, 1), round(fat_mass, 1)])
            date_data.append(input_date.split("-"))
            weight_data.append(input_weight)
            pec_data.append(input_pec)
            tri_data.append(input_tri)
            sub_data.append(input_sub)
            axi_data.append(input_axi)
            sup_data.append(input_sup)
            abd_data.append(input_abd)
            thi_data.append(input_thi)
            bf_data.append(round(bf_calc, 1))
            ffm_data.append(round(fat_free_mass, 1))
            fm_data.append(round(fat_mass, 1))

#-----CHART 1 (bodyfat and skinfold measurements over time)-----#
        sites_date_chart = pygal.DateLine(x_label_rotation=20)
        # Data for the bodyfat line. List of tuples in the format (date, bodyfat)
        sites_date_chart.add("Bodyfat (%)", [(date(int(j[0]), int(j[1]), int(j[2])),
        bf_data[i]) for i, j in enumerate(date_data)])
        # The same for the all the sites
        sites_date_chart.add("Pectoralis (mm)", [(date(int(j[0]), int(j[1]), int(j[2])),
        pec_data[i]) for i, j in enumerate(date_data)])
        sites_date_chart.add("Triceps (mm)", [(date(int(j[0]), int(j[1]), int(j[2])),
        tri_data[i]) for i, j in enumerate(date_data)])
        sites_date_chart.add("Subscapular (mm)", [(date(int(j[0]), int(j[1]), int(j[2])),
        sub_data[i]) for i, j in enumerate(date_data)])
        sites_date_chart.add("Axillary (mm)", [(date(int(j[0]), int(j[1]), int(j[2])),
        axi_data[i]) for i, j in enumerate(date_data)])
        sites_date_chart.add("Suprailliac (mm)", [(date(int(j[0]), int(j[1]), int(j[2])),
        sup_data[i]) for i, j in enumerate(date_data)])
        sites_date_chart.add("Abdomen (mm)", [(date(int(j[0]), int(j[1]), int(j[2])),
        abd_data[i]) for i, j in enumerate(date_data)])
        sites_date_chart.add("Thigh (mm)", [(date(int(j[0]), int(j[1]), int(j[2])),
        thi_data[i]) for i, j in enumerate(date_data)])
        # Render chart.
        sites_date_chart_data = sites_date_chart.render_data_uri()

#-----CHART 2 (weight, fat free mass and fat mass over time)-----#
        mass_date_chart = pygal.DateLine(x_label_rotation=20)
        # Adds data to chart as above.
        mass_date_chart.add("Weight (kg)", [(date(int(j[0]), int(j[1]), int(j[2])),
        weight_data[i]) for i, j in enumerate(date_data)])
        mass_date_chart.add("Fat free mass (kg)", [(date(int(j[0]), int(j[1]), int(j[2])),
        ffm_data[i]) for i, j in enumerate(date_data)])
        mass_date_chart.add("Fat mass (kg)", [(date(int(j[0]), int(j[1]), int(j[2])),
        fm_data[i]) for i, j in enumerate(date_data)])
        # Render chart.
        mass_date_chart_data = mass_date_chart.render_data_uri()

    # If any error is encountered, go to oops.html.
    except:
        return render_template("oops.html")

    # Go to index.html and bring listed data.
    return render_template("index.html", calculations=calculations,
    sites_date_chart_data=sites_date_chart_data,
    mass_date_chart_data=mass_date_chart_data)

# Run application if this file is run directly.
if __name__ == "__main__":
    app.run()
