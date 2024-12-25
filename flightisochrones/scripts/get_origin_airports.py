# This script creates the points for all selectable airports with their lat/long and their number of routes.

import os
import pandas as pd

# Define the path to the directory containing the CSV files
directory_path = r"C:\Users\toron\Documents\School\Masters\AA_2024\Application Development in Cartography\Project\RAW_DATA"

# Initialize an empty list to store dataframes
dataframes = []

# Loop through each file in the directory
for filename in os.listdir(directory_path):
    if filename.endswith(".csv"):
        file_path = os.path.join(directory_path, filename)
        # Read the CSV file into a dataframe
        df = pd.read_csv(file_path)

        # Check for rows with defined Latitude and Longitude
        valid_rows = df.dropna(subset=["Latitude", "Longitude"])
        number_of_routes = len(valid_rows) - 1  # Exclude the last row

        # Get the last row of the dataframe
        last_row = df.iloc[-1]

        # Create a new dataframe with the required information
        summary_df = pd.DataFrame([last_row]).copy()
        summary_df["Number of Routes"] = number_of_routes

        # Append the dataframe to the list
        dataframes.append(summary_df)

# Concatenate all dataframes into a single dataframe
result_df = pd.concat(dataframes, ignore_index=True)

columns_to_drop = [
    "Destination Code", "Destination Name", "Airline", 
    "Duration (minutes)", "Reverse Duration (minutes)", 
    "Distance (km)", "Flights per Day", "StartLon", "StartLat"
]

result_df = result_df.drop(columns=columns_to_drop)

# Display the dataframe for review
result_df.to_csv(r"C:\Users\toron\Documents\School\Masters\AA_2024\Application Development in Cartography\Project\RAW_DATA\Airports.csv", index=False)
