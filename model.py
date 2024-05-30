from flask import Flask, render_template, request
import pandas as pd
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def load_homepage():
    return render_template("index.html")

@app.route("/prediction", methods=["GET", "POST"])
def load_prediction():
    if request.method == "POST":
       temp = request.form.get("temp")
       rain = request.form.get("rain") 
       wind = request.form.get("wind") 
       print(temp)
       print(rain)
       print(wind)
    return render_template("prediction.html", input_rain=rain, input_temp=temp, input_wind=wind)

@app.route("/predictor", methods=["GET", "POST"])
def load_predictor():
    return render_template("predictor.html")