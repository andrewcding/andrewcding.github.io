# This script adds the country from the open flights dataset to each route, joined by IATA code.

import os
import geopandas as gpd
import pandas as pd
import json
from shapely.geometry import mapping  # For geometry conversion

# Define paths
lines_reduced_folder = r"C:\Users\toron\Documents\School\Masters\AA_2024\Application Development in Cartography\Project\flightisochrone_mapbox\flightisochrones\public\geojson"
airports_file = r"C:\Users\toron\Documents\School\Masters\AA_2024\Application Development in Cartography\Project\RAW_DATA\other\airports.csv"

# Load airports.csv and select necessary columns
airports_df = pd.read_csv(airports_file, usecols=["IATA", "Country"])

# Iterate over GeoJSON files in the folder
for file in os.listdir(lines_reduced_folder):
    if file.endswith("IST_lines_reduced.geojson"):
        # Load the GeoJSON file
        file_path = os.path.join(lines_reduced_folder, file)
        lines_reduced_gdf = gpd.read_file(file_path)

        # Merge with airports data
        merged_gdf = lines_reduced_gdf.merge(
            airports_df, left_on="Destination_Code", right_on="IATA", how="left"
        )
        merged_gdf.drop(columns=["IATA"], inplace=True)

        # Reformat to the desired GeoJSON format
        features = []
        for _, row in merged_gdf.iterrows():
            feature = {
                "type": "Feature",
                "id": row["OID"],
                "geometry": mapping(row["geometry"]),  # Use mapping for geometry
                "properties": row.drop(["geometry"]).to_dict(),
            }
            features.append(feature)

        formatted_geojson = {
            "type": "FeatureCollection",
            "features": features,
        }

        # Save the reformatted GeoJSON
        with open(file_path, "w") as geojson_file:
            json.dump(formatted_geojson, geojson_file, indent=4)

print("All files updated with the desired GeoJSON format.")

# NOTE!! Since geopandas dataframe is used, null has been replaced with NaN. Need to replace NaN values back with null after processing.
# (find/replace must be case sensitive due to Nantes Airport)