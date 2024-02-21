from flask import Flask, render_template
import pandas as pd
app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def load_homepage():

    data = ingest_data('traffic.csv')
    get_dates(data)
    return render_template("index.html")


@app.route("/predictor", methods=["GET", "POST"])
def load_predictor():
    return render_template("predictor.html")


def ingest_data(csv):
    data_list = pd.DataFrame([])
    for chunk in pd.read_csv(csv, iterator=True, chunksize=1000):
        data_list = pd.concat([data_list, chunk])
    return data_list.tail(3)

def get_dates(data):
    date_keywords = ['Date', 'Created Date', 'CRASH DATE', 'time', 'Occured_On' ]
    for index, row in data.iterrows():
        for keyword in date_keywords:
            if keyword in row:
                print(row[keyword])
