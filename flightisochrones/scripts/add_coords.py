# This script links the scraped data to the OpenFlights airports dataset to get lat/long coords

import os
import pandas as pd

# Define the path to the current working directory
script_directory = os.path.dirname(os.path.abspath(__file__))

# Path to the airports.csv file
airports_csv_path = os.path.join(script_directory, 'other', 'airports.csv')

# Load airports.csv data
airports_df = pd.read_csv(airports_csv_path)

# Function to merge airport data with each CSV file and add the departure airport
def add_airport_data_to_flight_routes():
    # Loop through each {airport_code}_flight_routes.csv file
    for file in os.listdir(script_directory):
        if file.endswith("flight_routes.csv"):
            # Load the flight routes CSV file
            file_path = os.path.join(script_directory, file)
            flight_routes_df = pd.read_csv(file_path)
            
            # Extract the airport code from the file name (e.g., 'AMS' from 'AMS_flight_routes.csv')
            airport_code = file.split('_')[0]
            
            # Get the departure airport details from airports.csv
            departure_airport = airports_df[airports_df['IATA'] == airport_code]
            if not departure_airport.empty:
                lat = departure_airport.iloc[0]['Latitude']
                lon = departure_airport.iloc[0]['Longitude']
                alt = departure_airport.iloc[0]['Altitude']
                city_name = departure_airport.iloc[0]['City']
                airport_name = departure_airport.iloc[0]['Name']
            else:
                lat, lon, alt, airport_name, city_name = None, None, None, None, None  # Default to None if not found

            # Create a row for the departure airport itself
            own_airport_row = {
                'Departure Airport': airport_code,
                'Destination Code': airport_code,
                'Destination Name': city_name,
                'Airline': 'null',
                'Duration (minutes)': 0,
                'Reverse Duration (minutes)': 0,
                'Distance (km)': 0,
                'Flights per Day': 'N/A',
                'Latitude': lat,
                'Longitude': lon,
                'Altitude': alt,
                'Aiport Name': airport_name
            }
            
            # Convert the row to a DataFrame
            own_airport_df = pd.DataFrame([own_airport_row])

            # Merge latitude, longitude, and altitude from airports.csv based on Destination Code
            merged_df = pd.merge(
                flight_routes_df, 
                airports_df[['IATA', 'Latitude', 'Longitude', 'Altitude', 'Name']], 
                left_on='Destination Code', 
                right_on='IATA', 
                how='left'
            )
            
            # Drop the extra 'IATA' column after merging
            merged_df = merged_df.drop(columns=['IATA'])
            
            # Append the row for the departure airport itself to the dataframe
            merged_df = pd.concat([merged_df, own_airport_df], ignore_index=True)

            # Save the updated file back to the same location
            merged_file_path = file_path
            merged_df.to_csv(merged_file_path, index=False)
            print(f"Updated file saved to: {merged_file_path}")

# Call the function to update all flight route CSVs
add_airport_data_to_flight_routes()
