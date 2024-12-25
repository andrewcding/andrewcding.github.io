# This scripts reduces the number of points used to create the geodesic routes line to improve the performance of the web app

import json
import numpy as np
import os

# Function to process the GeoJSON for a given airport code
def process_airport_geojson(directory, airport_code):
    # File path to the specific airport GeoJSON
    file_path = os.path.join(directory, f'{airport_code}_lines.geojson')

    # Load the GeoJSON file with utf-8 encoding
    with open(file_path, 'r', encoding='utf-8') as file:
        geojson_data = json.load(file)

    # Reduce points by a factor of 250 and preserve the first and last points
    geojson_data = reduce_points(geojson_data)

    # Process 'Flights_per_Day' attribute
    geojson_data, unique_flights_values = process_flights_per_day(geojson_data)

    # Print the unique 'Flights_per_Day' values
    print(f"Unique 'Flights_per_Day' values for {airport_code}: {unique_flights_values}")

    # Save the modified GeoJSON
    output_path = file_path.replace('.geojson', '_reduced.geojson')
    with open(output_path, 'w', encoding='utf-8') as file:
        json.dump(geojson_data, file, indent=4)

    print(f"GeoJSON processing complete for {airport_code}. Output saved as '{output_path}'.")

# Function to reduce points by a factor of 250 and preserve the first and last points
def reduce_points(geojson_data):
    for feature in geojson_data['features']:
        if feature['geometry']['type'] == 'LineString':
            original_coords = feature['geometry']['coordinates']
            # Reduce points while preserving the first and last points
            if len(original_coords) > 2:  # Ensure there are enough points to reduce
                reduced_coords = [original_coords[0]] + original_coords[1:-1:250] + [original_coords[-1]]
                feature['geometry']['coordinates'] = reduced_coords
    return geojson_data

# Function to process 'Flights_per_Day' attribute
# Flights per day was given a range of values such as 8-10, this function takes the average of the
# range of values
def process_flights_per_day(geojson_data):
    unique_values = set()
    
    for feature in geojson_data['features']:
        flights_per_day = feature['properties'].get('Flights_per_Day')
        if flights_per_day is not None:
            unique_values.add(flights_per_day)
            # If the value is a range, calculate the mean
            if '-' in flights_per_day:
                lower, upper = map(int, flights_per_day.split('-'))
                feature['properties']['Flights_per_Day'] = int(np.mean([lower, upper]))
            else:
                feature['properties']['Flights_per_Day'] = int(flights_per_day)
    
    return geojson_data, list(unique_values)

# Directory where the GeoJSON files are located
directory = r'C:\Users\toron\Documents\School\Masters\AA_2024\Application Development in Cartography\Project\GEOJSONS'

# List of airport codes to process
airport_codes = [
    'AMS', 'ATL', 'BKK', 'CDG', 'DOH', 'DXB', 'FRA', 'GRU',
    'HKG', 'ICN', 'JFK', 'JNB', 'LAX', 'LHR', 'MEX', 'NRT',
    'SFO', 'SIN', 'SYD', 'YYZ', 'ZRH'
]

# Loop through each airport code and process the corresponding GeoJSON
for airport_code in airport_codes:
    process_airport_geojson(directory, airport_code)
