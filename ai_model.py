import pandas as pd
from fastai.tabular.all import (
    TabularDataLoaders,
    Categorify,
    FillMissing,
    Normalize,
    range_of,
    RandomSplitter,
    accuracy,
    tabular_learner,
    ShowGraphCallback,
)

# Load the CSV files into pandas dataframes
weather_df = pd.read_csv('./datasets/nyc-weather.csv')
street_flooding_df = pd.read_csv('./datasets/street-flooding.csv')
bus_breakdowns_df = pd.read_csv('./datasets/bus-breakdowns-and-delays.csv')
motor_vehicle_collisions_df = pd.read_csv('./datasets/nyc-motor-vehicle-collisions.csv')
# mta_traffic = pd.read_csv('./datasets/mta-traffic.csv')

print('Dataframes loaded successfully.')

# Check the head of each dataframe to understand their structure and identify the primary key for joining
dfs = [weather_df, street_flooding_df, bus_breakdowns_df, motor_vehicle_collisions_df]
df_names = ['Weather', 'Street Flooding', 'Bus Breakdowns', 'Motor Vehicle Collisions']

# Normalize the date formats across datasets for joining
weather_df['time'] = pd.to_datetime(weather_df['time']).dt.normalize()
street_flooding_df['Created Date'] = pd.to_datetime(street_flooding_df['Created Date']).dt.normalize()
bus_breakdowns_df['Occurred_On'] = pd.to_datetime(bus_breakdowns_df['Occurred_On']).dt.normalize()
motor_vehicle_collisions_df['CRASH DATE'] = pd.to_datetime(motor_vehicle_collisions_df['CRASH DATE']).dt.normalize()

print('Date formats normalized.')

# Merge the datasets on the date columns
merged_df = weather_df.copy()
merged_df["flooding"] = merged_df["time"].map(
    street_flooding_df["Created Date"].value_counts()
)
merged_df["bus_breakdowns"] = merged_df["time"].map(
    bus_breakdowns_df["Occurred_On"].value_counts()
)
merged_df["motor_vehicle_collisions"] = merged_df["time"].map(
    motor_vehicle_collisions_df["CRASH DATE"].value_counts()
)
# Fill NaN values with 0
merged_df[["flooding", "bus_breakdowns", "motor_vehicle_collisions"]] = (
    merged_df[
        ["flooding", "bus_breakdowns", "motor_vehicle_collisions"]
    ].fillna(0)
)

# Convert the counts to integers
merged_df[["flooding", "bus_breakdowns", "motor_vehicle_collisions"]] = (
    merged_df[
        ["flooding", "bus_breakdowns", "motor_vehicle_collisions"]
    ].astype(int)
)
# drop na
merged_df = merged_df.dropna()


# Calculate the 75th percentile for each column
bus_breakdowns_75 = merged_df['bus_breakdowns'].quantile(0.75)
motor_vehicle_collisions_75 = merged_df['motor_vehicle_collisions'].quantile(0.75)
flooding_75 = merged_df['flooding'].quantile(0.75)
rain_75 = merged_df['rain (mm)'].quantile(0.75)

# Define the decision function
def decision(row):
    options = ['bus', 'car', 'bike', 'walk', 'stay_home']
    if row['bus_breakdowns'] > bus_breakdowns_75:
        options.remove('bus')
    if row['motor_vehicle_collisions'] > motor_vehicle_collisions_75:
        options.remove('car')
    if row['flooding'] > flooding_75 or row['rain (mm)'] > rain_75:
        options.remove('walk')
        options.remove('bike')

    return options[0]

# Apply the decision function to each row
merged_df.loc[:, 'decision'] = merged_df.apply(decision, axis=1)

# Rename the columns to simpler names in the pandas dataframe 'merged_df'
merged_df.columns = ['time', 'temp', 'precipitation', 'rain', 'cloudcover', 'cloudcover_low', 'cloudcover_mid', 'cloudcover_high', 'windspeed', 'winddirection', 'flooding', 'bus_breakdowns', 'collisions', 'decision']

dls = TabularDataLoaders.from_df(
    df=merged_df, 
    y_names="decision",
    cat_names=['decision'],
    cont_names=['temp', 'precipitation', 'rain', 'cloudcover', 'cloudcover_low', 'cloudcover_mid', 'cloudcover_high', 'windspeed', 'winddirection', 'flooding', 'bus_breakdowns', 'collisions' ],
    procs = [Categorify, FillMissing, Normalize])

learn = tabular_learner(dls, metrics=accuracy)
learn.fit_one_cycle(1)

# row, clas, probs = learn.predict(merged_df.iloc[1200])

# row.show()

print('MADE IT')