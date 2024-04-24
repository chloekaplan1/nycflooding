import pandas as pd

# Functions for AI model prototype
# Ingesting CSV data using python pandas library 
def ingest_data(csv):
    data_list = pd.DataFrame([])
    for chunk in pd.read_csv(csv, iterator=True, chunksize=1000):
        data_list = pd.concat([data_list, chunk])

# Merge the datasets on the date columns and store in merged_df
merged_df = pd.DataFrame([])

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

# Apply the decision function to each row in merged_df