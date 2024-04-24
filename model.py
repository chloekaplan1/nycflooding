from flask import Flask, render_template
import pandas as pd
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def load_homepage():
    return render_template("index.html")

@app.route("/prediction", methods=["GET", "POST"])
def load_prediction():
    return render_template("prediction.html")

@app.route("/predictor", methods=["GET", "POST"])
def load_predictor():
    return render_template("predictor.html")