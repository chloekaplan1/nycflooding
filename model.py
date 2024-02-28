from flask import Flask, render_template
import pandas as pd
app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def load_homepage():

    data = ingest_data('traffic.csv')
    return render_template("index.html")


@app.route("/predictor", methods=["GET", "POST"])
def load_predictor():
    return render_template("predictor.html")


def ingest_data(csv):
    data_list = pd.DataFrame([])
    for chunk in pd.read_csv(csv, iterator=True, chunksize=1000):
        data_list = pd.concat([data_list, chunk])
    return get_date_data(csv, data_list)

# def get_dates(data):
#     date_keywords = ['Date', 'Created Date', 'CRASH DATE', 'time', 'Occured_On' ]
#     for index, row in data.iterrows():
#         for keyword in date_keywords:
#             if keyword in row:
#                 print(row[keyword])


def get_date_data(csv, data_list):
    if csv == 'weather.csv': #works
        tail = data_list.tail(10000)
        front_of_tail = tail.head(1)
        print('front_of_tail')
        print(front_of_tail)
        return front_of_tail
    elif csv == 'bus_delays.csv': #does not work
        tail = data_list.tail(1000)
        front_of_tail = tail.head(1)
        print('front_of_tail')
        print(front_of_tail)
        return front_of_tail
    elif csv == 'mv_collisions.csv':  #does not work
        tail = data_list.tail(10000)
        front_of_tail = tail.head(1)
        print('front_of_tail')
        print(front_of_tail)
        return front_of_tail
    elif csv == 'street_flooding.csv': #works
        tail = data_list.tail(10000)
        front_of_tail = tail.head(1)
        print('front_of_tail')
        print(front_of_tail)
        return front_of_tail
    elif csv == 'traffic.csv': #works
        tail = data_list.tail(10000)
        front_of_tail = tail.head(1)
        print('front_of_tail')
        print(front_of_tail)
        return front_of_tail