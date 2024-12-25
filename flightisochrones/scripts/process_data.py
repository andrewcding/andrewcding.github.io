# This script takes the cleaned outputs from webscraping to interpolate isochrones and create all necessary geojsons for the webapp

import arcpy
import os
from arcpy.sa import *

arcpy.env.overwriteOutput = True

def process_airport(csv_path, output_workspace):
    # Set environment
    arcpy.env.workspace = output_workspace

    file_name = os.path.basename(csv_path).split('.')[0]
    airport_code = file_name[:3]

    # Extract the name of the CSV (without extension) to use as the feature class name
    csv_name = os.path.basename(csv_path).split('.')[0]
    output_point_fc = os.path.join(output_workspace, csv_name)

    # Create the point feature class from the CSV
    points = arcpy.management.XYTableToPoint(csv_path, output_point_fc, "Longitude", "Latitude", coordinate_system=arcpy.SpatialReference(4326))
    
    output_line_fc = os.path.join(output_workspace, f"{airport_code}_lines")
    
    # Run the XY to Line tool to create geodesic lines
    routes = arcpy.management.XYToLine(
        in_table=points,
        out_featureclass=output_line_fc,
        startx_field="StartLon",
        starty_field="StartLat",
        endx_field="Longitude",
        endy_field="Latitude",
        line_type="GEODESIC",
        id_field="Destination Code",
        attributes="ATTRIBUTES"
    )

    # Create dissolved buffer for lines
    buffer = arcpy.analysis.PairwiseBuffer(
        in_features=routes,
        out_feature_class=os.path.join(output_workspace, f"{airport_code}_output_buffer"),
        buffer_distance_or_field="12.5 DecimalDegrees",
        dissolve_option="ALL",
        method="GEODESIC"
    )

    # Smooth dissolved buffer for extent polygon
    extent = arcpy.cartography.SmoothPolygon(
        in_features=buffer,
        out_feature_class=os.path.join(output_workspace, f"{airport_code}_output_extent"),
        algorithm="PAEK",
        tolerance="30 DecimalDegrees",
        error_option="RESOLVE_ERRORS"
    )

    interpolate_values = ["Duration__minutes_", "Reverse_Duration__minutes_"]
    contour_paths = []
    raster_paths = []
    contour_poly_paths = []

    # Interpolate for both directions
    for value in interpolate_values:
        if value == "Duration__minutes_":
            name = "Departing"
        else:
            name = "Arriving"

        with arcpy.EnvManager(extent=arcpy.Describe(extent).extent, mask=f"{output_workspace}/{airport_code}_output_extent"):
            kriging_model = KrigingModelOrdinary(
                semivariogramType="CIRCULAR",
                lagSize=1.0,
                nugget=0.1,
                partialSill=0.8
            )
            out_surface_raster = arcpy.sa.Kriging(
                in_point_features=points,
                z_field=value,
                kriging_model=kriging_model,
                cell_size=0.510385873124,
                search_radius="VARIABLE 30"
            )
            raster_path = os.path.join(output_workspace, f"{airport_code}_{name}_Isochrone")
            out_surface_raster.save(raster_path)
            raster_paths.append(raster_path)  # Collect raster paths for export

            # Generate contours from the raster
            contour_path = os.path.join(output_workspace, f"{airport_code}_{name}_Isochrone_Contours")
            arcpy.sa.Contour(
                in_raster=out_surface_raster,
                out_polyline_features=contour_path,
                contour_interval=60
            )
            contour_paths.append(contour_path)  # Collect contour paths for export

            # Generate contour polygons from the raster
            contour_poly_path = os.path.join(output_workspace, f"{airport_code}_{name}_Isochrone_Polygons")
            arcpy.sa.Contour(
                in_raster=out_surface_raster,
                contour_type = "CONTOUR_POLYGON",
                out_polyline_features=contour_poly_path,
                contour_interval=60
            )
            contour_poly_paths.append(contour_poly_path)  # Collect contour paths for export


    # Collect feature classes for exporting
    output_features = [points.getOutput(0), routes.getOutput(0), extent.getOutput(0)] + contour_paths + contour_poly_paths

    # Export each feature class to GeoJSON
    for item in output_features:
        var_name = os.path.basename(item)  # Use the file name as the variable name
        out_json_file = (
            fr"C:\Users\toron\Documents\School\Masters\AA_2024\Application Development in Cartography\Project\GEOJSONS\{var_name}.geojson"
        )
        
        arcpy.conversion.FeaturesToJSON(
            in_features=item,
            out_json_file=out_json_file,
            format_json="FORMATTED",
            include_z_values="NO_Z_VALUES",
            include_m_values="NO_M_VALUES",
            geoJSON="GEOJSON",
            outputToWGS84="WGS84",
            use_field_alias="USE_FIELD_NAME"
        )
        print(f"Exported {var_name} to {out_json_file}")

    # Export each raster to GeoTIFF
    # for raster_path in raster_paths:
    #     var_name = os.path.basename(raster_path)  # Use the file name as the variable name
    #     out_tiff_file = (
    #         fr"C:\Users\toron\Documents\School\Masters\AA_2024\Application Development in Cartography\Project\GEOJSONS\{var_name}.tif"
    #     )
    #     arcpy.management.CopyRaster(
    #         in_raster=raster_path,
    #         out_rasterdataset=out_tiff_file,
    #         format="TIFF"
    #     )
    #     print(f"Exported raster {var_name} to {out_tiff_file}")


# Save intermediate data to scratch GDB
scratch_gdb_path = arcpy.env.scratchGDB

# Define the array of airport codes to loop through
airport_codes = [
    'AMS', 'ATL', 'BKK', 'CDG', 'DOH', 'DXB', 'FRA', 'GRU',
    'HKG', 'ICN', 'JFK', 'JNB', 'LAX', 'LHR', 'MEX', 'NRT',
    'SFO', 'SIN', 'SYD', 'YYZ', 'ZRH'
]

# Directory where the files are located
directory = 'C:\\Users\\toron\\Documents\\School\\Masters\\AA_2024\\Application Development in Cartography\\Project\\RAW_DATA'

# Loop through each airport code and process the corresponding file
for code in airport_codes:
    file_path = os.path.join(directory, f'{code}_flight_routes.csv')
    process_airport(file_path, scratch_gdb_path)