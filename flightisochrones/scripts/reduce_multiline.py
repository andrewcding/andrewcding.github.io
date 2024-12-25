# This scripts reduces the number of points in the MULTILINESTRINGS not covered by the other script.
# Multiline strings are present when the line crosses over the international date line.

import json
import os

# Function to process the GeoJSON and reduce points in MultiLineStrings
def process_multiline_geojson(file_path):
    # Load the GeoJSON file with utf-8 encoding
    with open(file_path, 'r', encoding='utf-8') as file:
        geojson_data = json.load(file)

    # Reduce points in MultiLineString geometries
    geojson_data = reduce_points_multilines(geojson_data)

    # Overwrite the original GeoJSON file
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(geojson_data, file, indent=4)

    print(f"GeoJSON processing complete. File overwritten: '{file_path}'.")

# Function to reduce points in MultiLineString geometries
def reduce_points_multilines(geojson_data):
    for feature in geojson_data['features']:
        if feature['geometry']['type'] == 'MultiLineString':
            original_multiline_coords = feature['geometry']['coordinates']
            reduced_multiline_coords = []
            # Process each line segment in the MultiLineString
            for line_coords in original_multiline_coords:
                # Reduce points while preserving the first and last points
                if len(line_coords) > 2:  # Ensure there are enough points to reduce
                    reduced_coords = [line_coords[0]] + line_coords[1:-1:250] + [line_coords[-1]]
                else:
                    reduced_coords = line_coords  # Keep original if not enough points
                reduced_multiline_coords.append(reduced_coords)
            feature['geometry']['coordinates'] = reduced_multiline_coords
    return geojson_data

# Directory where the GeoJSON files are located
directory = r'C:\Users\toron\Documents\School\Masters\AA_2024\Application Development in Cartography\Project\GeoJSON-Data\Airport Isochrones'

# Process each GeoJSON file in the directory
for filename in os.listdir(directory):
    if filename.endswith('reduced.geojson'):
        file_path = os.path.join(directory, filename)
        process_multiline_geojson(file_path)
