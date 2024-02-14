from flask import Flask, render_template
import pandas as pd
app = Flask(__name__)
@app.route("/", methods = ["GET", "POST"])
def load_homepage():
    weather_list = pd.DataFrame([])
    for df in pd.read_csv('weather.csv', iterator=True, chunksize=1000 ):
        weather_list = pd.concat([weather_list, pd.DataFrame(df.groupby(["time"]).size().reset_index(name="Count"))])
    print(weather_list.sort_values(by='Count', ascending = False).head(10))
    print("Total rows: " + str(sum(weather_list['Count'])))
    return render_template("index.html")


@app.route("/predictor", methods = ["GET", "POST"])
def load_predictor():
    return render_template("predictor.html")