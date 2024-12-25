<template>
    <div>
        <div ref="mapContainer" class="map-container">
        </div>
        
        <!-- Airport legend -->
        <div id="airport-legend" class="map-legend" v-if="showAirportLegend">
            <h3>Legend</h3>
            <hr style="margin-top: 0px; margin-bottom: 10px;">
            <div class="legend-item">
                <div class="legend-symbol" style="width: 14px; height: 14px;">
                    <span class="legend-icon" style="font-size: 9px">✈︎</span>
                </div>
                <span class="legend-label-airport">100 direct flights</span>
            </div>
            <div class="legend-item">
                <div class="legend-symbol" style="width: 18px; height: 18px;">
                    <span class="legend-icon" style="font-size: 11.5px">✈︎</span>
                </div>
                <span class="legend-label-airport">150 direct flights</span>
            </div>
            <div class="legend-item">
                <div class="legend-symbol" style="width: 22px; height: 22px;">
                    <span class="legend-icon" style="font-size: 14px">✈︎</span>
                </div>
                <span class="legend-label-airport">200 direct flights</span>
            </div>
        </div>
        
        <!-- Duration Legend -->
        <div id="route-legend" class="map-legend" v-if="showRouteLegend">
            <h3>Legend</h3>
            <hr style="margin-top: 0px; margin-bottom: 10px;">
            <!-- Time Difference Legend -->
            <h4>Travel Time Difference</h4>
            <h5 style='padding-bottom: 5px;'>(vs reverse direction)</h5>
            <div class="legend-item">
                <div class="legend-color" style="background-color: #1a9641; width: 20px; height: 20px;"></div>
                <span class="legend-label-route">20% faster</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background-color: #a6d96a; width: 20px; height: 20px;"></div>
                <span class="legend-label-route">10% faster</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background-color: #ffffbf; width: 20px; height: 20px;"></div>
                <span class="legend-label-route">No difference</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background-color: #fdae61; width: 20px; height: 20px;"></div>
                <span class="legend-label-route">10% slower</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background-color: #d7191c; width: 20px; height: 20px;"></div>
                <span class="legend-label-route">20% slower</span>
            </div>
            
            <!-- Flights per Day Legend -->
            <h4>Flights per Day</h4>
            <div class="legend-item">
                <div class="legend-line" style="width: 50px; height: 2px; background-color: #ffffff;"></div>
                <span class="legend-label-route">1 daily flight</span>
            </div>
            <div class="legend-item">
                <div class="legend-line" style="width: 50px; height: 5px; background-color: #ffffff;"></div>
                <span class="legend-label-route">5 daily flights</span>
            </div>
            <div class="legend-item">
                <div class="legend-line" style="width: 50px; height: 10px; background-color: #ffffff;"></div>
                <span class="legend-label-route">15 daily flights</span>
            </div>
        </div>
    </div>
</template>

<script>
// Import libraries
import mapboxgl from 'mapbox-gl';
import * as turf from '@turf/turf';
mapboxgl.accessToken = "pk.eyJ1IjoiYW5kd29vIiwiYSI6ImNrMjlnYnNkdTEwMHozaG5wamJvZHJyangifQ.6M4eeri_Ubmo7NedQT7NuQ";

export default {
    props: {
        sidebarVisible: {
            type: Boolean,
            default: true
        },
        filterDuration: {
            type: Number,
            default: 20
        },
        filterFrequency: {
            type: Number,
            default: 0
        },
        showRouteLegend: {
            type: Boolean,
            default: false
        }
    },
    
    data: () => ({ map: null,
        showAirportLegend: true, // Control airport legend visibility
        geojsonSubset: null, // Store currently filtered routes
    }),
    
    mounted() {
        const map = new mapboxgl.Map({
            container: this.$refs.mapContainer,
            projection: 'globe',
            style: 'mapbox://styles/mapbox/dark-v10',
            center: [-71.224518, 42.213995],
            zoom: 1.7,
            minZoom: 1.5,
        });
        
        map.on('style.load', () => {
            
            map.setPadding({left: 300})
            
            map.getStyle().layers.forEach((layer) => {
                if (layer.type === 'symbol') {
                    map.removeLayer(layer.id);
                }
            });
            
            map.setFog({
                color: 'rgb(50, 50, 50)', // Darker lower atmosphere to blend well with a dark basemap
                'high-color': '#1a1a1d', // Very dark upper atmosphere to create a subtle transition
                'horizon-blend': 0.1, // Slightly increase the horizon blend to make the atmosphere feel thicker and more immersive
                'space-color': '#0a0a0a', // Deep black background to match the dark theme
                'star-intensity': 0.15 // Low but noticeable star brightness for a subtle effect
            });
        });
        
        map.on('load', () => {
            
            // Wind layer
            map.addSource('raster-array-source', {
                'type': 'raster-array',
                'url': 'mapbox://rasterarrayexamples.gfs-winds',
                'tileSize': 512
            });
            map.addLayer({
                'id': 'wind-layer',
                'type': 'raster-particle',
                'source': 'raster-array-source',
                'source-layer': '10winds',
                'paint': {
                    'raster-particle-speed-factor': 0.4,
                    'raster-particle-fade-opacity-factor': 0.9,
                    'raster-particle-reset-rate-factor': 0.4,
                    'raster-particle-count': 4000,
                    'raster-particle-max-speed': 40,
                    'raster-particle-color': [ // Wind particle colours adapted from Mapbox demo
                    'interpolate',
                    ['linear'],
                    ['raster-particle-speed'],
                    1.5, 'rgba(134,163,171,1)',
                    2.5, 'rgba(126,152,188,1)',
                    4.12, 'rgba(110,143,208,1)',
                    4.63, 'rgba(110,143,208,1)',
                    6.17, 'rgba(15,147,167,1)',
                    7.72, 'rgba(15,147,167,1)',
                    9.26, 'rgba(57,163,57,1)',
                    10.29, 'rgba(57,163,57,1)',
                    11.83, 'rgba(194,134,62,1)',
                    13.37, 'rgba(194,134,63,1)',
                    14.92, 'rgba(200,66,13,1)',
                    16.46, 'rgba(200,66,13,1)',
                    18.0, 'rgba(210,0,50,1)',
                    20.06, 'rgba(215,0,50,1)',
                    21.6, 'rgba(175,80,136,1)',
                    23.66, 'rgba(175,80,136,1)',
                    25.21, 'rgba(117,74,147,1)',
                    27.78, 'rgba(117,74,147,1)',
                    29.32, 'rgba(68,105,141,1)',
                    31.89, 'rgba(68,105,141,1)',
                    33.44, 'rgba(194,251,119,1)',
                    42.18, 'rgba(194,251,119,1)',
                    43.72, 'rgba(241,255,109,1)',
                    48.87, 'rgba(241,255,109,1)',
                    50.41, 'rgba(256,256,256,1)',
                    57.61, 'rgba(256,256,256,1)',
                    59.16, 'rgba(0,256,256,1)',
                    68.93, 'rgba(0,256,256,1)',
                    69.44, 'rgba(256,37,256,1)'
                    ]
                },
                'layout': {
                    'visibility': 'none' // Hidden by default
                }
            });
            
            // Airports layer
            map.addSource('airports', {
                type: 'geojson',
                data: 'https://raw.githubusercontent.com/andrewcding/GeoJSON-Data/refs/heads/main/Airport%20Isochrones/Airports.geojson'
            });
            
            // Circle portion of symbology
            map.addLayer({
                id: 'airport-points',
                type: 'circle',
                source: 'airports',
                paint: {
                    'circle-color': 'rgba(0, 0, 0, 0.2)', // Color of the points
                    'circle-radius': [
                    'interpolate',
                    ['linear'],
                    ['get', 'Number_of_Routes'],
                    75, 3.5, // Minimum value, size 5
                    275, 13.5 // Maximum value, size 15
                    ],
                    'circle-stroke-color': '#fff', // White border for contrast
                    'circle-stroke-width': 1.5 // Border thickness
                }
            });
            
            // Airplane (✈︎) portion of symbology
            map.addLayer({
                id: 'airport-icon',
                type: 'symbol',
                source: 'airports',
                layout: {
                    'text-field': '✈︎', // The airplane icon as text
                    'text-size': [
                    'interpolate',
                    ['linear'],
                    ['get', 'Number_of_Routes'],
                    75, 5, // Minimum value, size 5
                    275, 25 // Maximum value, size 15
                    ],
                    'text-font': ['Arial Unicode MS Regular'], // A font that should support the airplane icon
                    'text-anchor': 'center', // Center the icon on the circle
                    'text-allow-overlap': true,
                    'text-rotate': -20 // Rotate plane
                },
                paint: {
                    'text-color': '#fff' // White color for the icon
                }
            });
            
            // Airport labels
            map.addLayer({
                id: 'airport-labels',
                type: 'symbol',
                source: 'airports',
                layout: {
                    'text-field': ['get', 'Airport_Code'],
                    'text-size': 12, 
                    'text-font': ['Open Sans Bold', 'Arial Unicode MS Bold'],
                    'text-offset': [1.5, -1.5], // Position the label slightly above and to the right of the point
                    'text-anchor': 'center' // Anchor the label at the bottom of the text
                },
                paint: {
                    'text-color': '#ffffff', // Label text color
                }
            });
            
            // Make airport symbols and label bigger on hover
            map.on('mouseenter', 'airport-points', (e) => {
                
                // Get hovered airport
                const airportCode = e.features[0].properties.Airport_Code;
                
                // Change cursor to pointer
                map.getCanvas().style.cursor = 'pointer';
                
                // Increase size of the hovered point circle
                map.setPaintProperty('airport-points', 'circle-radius', [
                'case',
                ['==', ['get', 'Airport_Code'], airportCode],
                [
                'interpolate',
                ['linear'],
                ['get', 'Number_of_Routes'],
                75, 7.5,  // Hover size
                275, 18.5
                ],
                [
                'interpolate',
                ['linear'],
                ['get', 'Number_of_Routes'],
                75, 3.5,  // Original size
                275, 13.5
                ]
                ]);
                
                // Increase size of the hovered icon
                map.setLayoutProperty('airport-icon', 'text-size', [
                'case',
                ['==', ['get', 'Airport_Code'], airportCode],
                [
                'interpolate',
                ['linear'],
                ['get', 'Number_of_Routes'],
                75, 10,  // Hover size
                275, 35
                ],
                [
                'interpolate',
                ['linear'],
                ['get', 'Number_of_Routes'],
                75, 5,  // Original size
                275, 25
                ]
                ]);
                
                // Increase size of the hovered label
                map.setLayoutProperty('airport-labels', 'text-size', [
                'case',
                ['==', ['get', 'Airport_Code'], airportCode],
                16,  // Increased size on hover
                12   // Original size
                ]);
            });
            
            map.on('mouseleave', 'airport-points', () => {
                // Reset cursor to default
                map.getCanvas().style.cursor = '';
                
                // Reset size of all airport points
                map.setPaintProperty('airport-points', 'circle-radius', [
                'interpolate',
                ['linear'],
                ['get', 'Number_of_Routes'],
                75, 3.5,
                275, 13.5
                ]);
                
                // Reset size of all airport icons
                map.setLayoutProperty('airport-icon', 'text-size', [
                'interpolate',
                ['linear'],
                ['get', 'Number_of_Routes'],
                75, 5,
                275, 25
                ]);
                
                // Reset size of all labels
                map.setLayoutProperty('airport-labels', 'text-size', 12);
            });
        });
        
        // Handle selection of airport
        map.on('click', 'airport-points', (e) => {
            
            // Get the Airport_Code of the clicked point
            const airportCode = e.features[0].properties.Airport_Code;
            
            // Emit details to App to change header on Sidebar
            this.$emit('select-airport', {
                selected: true,
                airportCode: airportCode,
                airportName: e.features[0].properties.Name
            });
            
            // Hide the airport legend and points
            this.showAirportLegend = false;
            
            map.setLayoutProperty('airport-points', 'visibility', 'none');
            map.setLayoutProperty('airport-icon', 'visibility', 'none');
            map.setLayoutProperty('airport-labels', 'visibility', 'none');
            
            // Get URLs for the GeoJSON data for selected airport
            const routesURL = `https://raw.githubusercontent.com/andrewcding/GeoJSON-Data/refs/heads/main/Airport%20Isochrones/${airportCode}_lines_reduced.geojson`;
            const outputExtentURL = `https://raw.githubusercontent.com/andrewcding/GeoJSON-Data/refs/heads/main/Airport%20Isochrones/${airportCode}_output_extent.geojson`;
            const pointsURL = `https://raw.githubusercontent.com/andrewcding/GeoJSON-Data/refs/heads/main/Airport%20Isochrones/${airportCode}_flight_routes.geojson`;
            const departingIsoURL = `https://raw.githubusercontent.com/andrewcding/GeoJSON-Data/refs/heads/main/Airport%20Isochrones/${airportCode}_Departing_Isochrone_Contours.geojson`;
            const arrivingIsoURL = `https://raw.githubusercontent.com/andrewcding/GeoJSON-Data/refs/heads/main/Airport%20Isochrones/${airportCode}_Arriving_Isochrone_Contours.geojson`;
            const departingPolygon = `https://raw.githubusercontent.com/andrewcding/GeoJSON-Data/refs/heads/main/Airport%20Isochrones/${airportCode}_Departing_Isochrone_Polygons.geojson`;
            const arrivingPolygon = `https://raw.githubusercontent.com/andrewcding/GeoJSON-Data/refs/heads/main/Airport%20Isochrones/${airportCode}_Arriving_Isochrone_Polygons.geojson`;
            
            // Remove existing layers and sources to avoid duplicates
            const layersToRemove = ['points-labels', 'points-dest', 'routes', 'output-extent', 'departing-isochrones', 
            'arriving-isochrones', 'arriving-isochrones-labels', 'departing-isochrones-labels', 'routes-hover', 'plane_points',
            'departing-polygons', 'arriving-polygons'];
            
            layersToRemove.forEach((id) => {
                if (map.getLayer(id)) {
                    map.removeLayer(id);
                }
            });
            
            const sourcesToRemove = ['points', 'routes', 'output-extent', 'departing-iso', 'arriving-iso', 'plane_points', 'departing-poly', 'arriving-poly'];
            sourcesToRemove.forEach((id) => {
                if (map.getSource(id)) {
                    map.removeSource(id);
                }
            });
            
            // Fetch routes
            fetch(routesURL)
            .then((response) => response.json())
            .then((geojson) => {
                this.geojson = geojson;
                
                // Emit routes geojson to populate table on Sidebar
                this.$emit('routes-loaded', geojson);
                
                map.addSource('routes', {
                    type: 'geojson',
                    data: geojson
                });
                
                // Add the GeoJSON source and line layer for the routes
                map.addLayer({
                    id: 'routes',
                    type: 'line',
                    source: 'routes',
                    paint: {
                        'line-color': '#ffffff',
                        'line-width': 1
                    }
                });
                
                // Add a hover effect layer for routes
                map.addLayer({
                    id: 'routes-hover',
                    type: 'line',
                    source: 'routes',
                    paint: {
                        'line-color': '#ffffff',  // Keep the same color
                        'line-width': 4,          // Make the line thicker to emphasize it
                        'line-opacity': [
                        "case",
                        ["boolean", ["feature-state", "hover"], false],
                        1,
                        0
                        ]
                    }
                });
                
                // Track the feature currently hovered
                let hoveredRouteId = null;
                
                // Mouse enter event for highlighting the route (uses routes-hover because it is wider)
                map.on('mouseenter', 'routes-hover', (e) => {
                    // Change the cursor to a pointer
                    map.getCanvas().style.cursor = 'pointer';
                    
                    // Get the feature ID of the hovered route
                    if (e.features.length > 0) {
                        if (hoveredRouteId !== null) {
                            map.setFeatureState(
                            { source: 'routes', id: hoveredRouteId },
                            { hover: false }
                            );
                        }
                        hoveredRouteId = e.features[0].id;
                        
                        // Set the hover state for the route
                        map.setFeatureState(
                        { source: 'routes', id: hoveredRouteId },
                        { hover: true }
                        );
                        
                        // Create a popup with relevant information
                        const properties = e.features[0].properties;
                        
                        // Determine the correct duration to display
                        const isDeparting = this.map.getLayoutProperty('arriving-isochrones', 'visibility') === 'none';
                        const durationInMinutes = isDeparting ? properties.Duration__minutes_ : properties.Reverse_Duration__minutes_;
                        
                        let popupContent = '';
                        
                        // If duration difference is toggled
                        if (this.showRouteLegend) {
                            const durationDifference = properties.Duration__minutes_ - properties.Reverse_Duration__minutes_;
                            
                            // Convert duration difference to hours and minutes
                            const absMinutes = Math.abs(durationDifference);
                            const diffHours = Math.floor(absMinutes / 60);
                            const diffMinutes = absMinutes % 60;
                            
                            let durationDiffString = '';
                            if (diffHours > 0) {
                                durationDiffString += `${diffHours}h`;
                            }
                            if (diffMinutes > 0 || diffHours === 0) { // Ensure minutes are always shown, even if hours are 0
                                durationDiffString += `${diffMinutes}m`;
                            }
                            
                            let fasterOrSlower;
                            if (isDeparting) {
                                // Determine if the route is faster or slower
                                fasterOrSlower = durationDifference < 0 ? 'faster than' : 'slower than';
                            } else {
                                // Determine if the route is faster or slower
                                fasterOrSlower = durationDifference < 0 ? 'slower than' : 'faster than';
                            }
                            
                            let flightsPerDay;
                            if (properties.Flights_per_Day == 0) {
                                flightsPerDay = 'subweekly flights'
                            } else if (properties.Flights_per_Day == null) {
                                flightsPerDay = 'Route currently not operating'
                            } else if (properties.Flights_per_Day == 1){
                                flightsPerDay = properties.Flights_per_Day + " flight per day"
                            } else {
                                flightsPerDay = properties.Flights_per_Day + " flights per day"
                            }
                            
                            popupContent = `
                                <div style="font-family: 'Open Sans', sans-serif; font-size: 13px; color: black;">
                                    ${properties.Departure_Airport} → ${properties.Destination_Code} (${properties.Destination_Name})
                                    <br>
                                    Duration Difference: ${durationDiffString} ${fasterOrSlower} reverse direction
                                    <br>
                                    Frequency: ${flightsPerDay}
                                </div>
                                           `;
                        } else { // Default case
                            // Convert duration to hours and minutes
                            const hours = Math.floor(durationInMinutes / 60);
                            const minutes = durationInMinutes % 60;
                            
                            // Format the duration string
                            let durationString = '';
                            if (hours > 0) {
                                durationString += `${hours} ${hours === 1 ? 'hour' : 'hours'}`;
                            }
                            if (minutes > 0) {
                                if (hours > 0) {
                                    durationString += ' ';
                                }
                                durationString += `${minutes} ${minutes === 1 ? 'minute' : 'minutes'}`;
                            }
                            
                            let flightsPerDay;
                            if (properties.Flights_per_Day == 0) {
                                flightsPerDay = 'subweekly flights'
                            } else if (properties.Flights_per_Day == null) {
                                flightsPerDay = 'Route currently not operating'
                            } else if (properties.Flights_per_Day == 1){
                                flightsPerDay = properties.Flights_per_Day + " flight per day"
                            } else {
                                flightsPerDay = properties.Flights_per_Day + " flights per day"
                            }
                            
                            // Default popup content
                            popupContent = `
                                <div style="font-family: 'Open Sans', sans-serif; font-size: 13px; color: rgb(44, 62, 80);">
                                    ${properties.Departure_Airport} → ${properties.Destination_Code} (${properties.Destination_Name})
                                    <br>
                                    Duration: ${durationString}
                                    <br>
                                    Frequency: ${flightsPerDay}
                                </div>
                            `;
                        }
                        
                        // Ensure there's only one popup at a time
                        if (window.currentPopup) {
                            window.currentPopup.remove();
                        }
                        
                        // Create a new popup
                        window.currentPopup = new mapboxgl.Popup({
                            closeButton: false,
                            closeOnClick: false
                        })
                        .setLngLat(e.lngLat)
                        .setHTML(popupContent)
                        .addTo(map);
                    }
                });
                
                // Mouse leave event to remove highlighting
                map.on('mouseleave', 'routes-hover', () => {
                    if (hoveredRouteId !== null) {
                        map.setFeatureState(
                        { source: 'routes', id: hoveredRouteId },
                        { hover: false }
                        );
                    }
                    hoveredRouteId = null;
                    
                    // Reset the cursor style
                    map.getCanvas().style.cursor = '';
                    
                    // Remove the popup
                    if (window.currentPopup) {
                        window.currentPopup.remove();
                        window.currentPopup = null;
                    }
                });
            })
            .catch((error) => console.error('Error fetching GeoJSON:', error));
            
            // Add the GeoJSON source and polygon layer for the output extent
            map.addSource('output-extent', {
                type: 'geojson',
                data: outputExtentURL
            });
            map.addLayer({
                id: 'output-extent',
                type: 'fill',
                source: 'output-extent',
                paint: {
                    'fill-color': 'rgba(255, 255, 255, 0.1)', // Very transparent white fill
                    'fill-outline-color': '#000000' // Solid black border
                }
            });
            
            // Add the GeoJSON source and circle layer for the points
            map.addSource('points', {
                type: 'geojson',
                data: pointsURL
            });
            map.addLayer({
                id: 'points-dest',
                type: 'circle',
                source: 'points',
                paint: {
                    'circle-color': '#ffffff', // White color
                    'circle-radius': [
                    'interpolate',
                    ['linear'],
                    ['zoom'],
                    2, 1.5,
                    10, 5,
                    ],
                    'circle-stroke-color': '#000', // Black border for contrast
                    'circle-stroke-width': 1.0 // Border thickness
                }
            });
            
            map.addLayer({
                id: 'points-labels',
                type: 'symbol',
                source: 'points',
                layout: {
                    'text-field': ['get', 'Destination_Code'],
                    'text-size': 12,
                    'text-font': ['Open Sans Bold', 'Arial Unicode MS Regular'], // Supported fonts
                    'text-anchor': 'top',
                    'text-offset': [1, -1.5], // Adjust label position
                    'text-allow-overlap': true // Allow overlap
                },
                paint: {
                    'text-color': '#FFFFFF', // White text color
                    'text-halo-color': '#000000', // Black halo for background effect
                    'text-halo-width': 1, // Halo width
                    'text-opacity': [
                    'interpolate',
                    ['linear'],
                    ['zoom'],
                    3, 0, // Hide or show labels based on zoom
                    3.5, 1 
                    ]
                }
            });
            
            
            // Add the GeoJSON source and line layer for the departing isochrone contours
            map.addSource('departing-iso', {
                type: 'geojson',
                data: departingIsoURL
            });
            
            map.addSource('arriving-iso', {
                type: 'geojson',
                data: arrivingIsoURL
            });
            
            // Define colour scale for isochrones
            function getColorScale(propertyName) {
                return [
                'interpolate',
                ['linear'],
                ['to-number', ['get', propertyName]],
                60, '#fde725',    // Yellow
                120, '#dce319',   // Bright yellow-green
                180, '#b6de2b',   // Yellow-green
                240, '#6ece58',   // Light green
                300, '#35b779',   // Green
                360, '#1f9e89',   // Greenish teal
                420, '#26828e',   // Teal
                480, '#31688e',   // Blue
                540, '#3e4989',   // Blue-purple
                600, '#482777',   // Purple
                660, '#440154',   // Dark purple
                ];
            }
            
            map.addLayer({
                id: 'departing-isochrones',
                type: 'line',
                source: 'departing-iso',
                paint: {'line-color': getColorScale('Contour'),
                'line-width': 2 
            },
        });
        
        map.addLayer({
            id: 'departing-isochrones-labels',
            type: 'symbol',
            source: 'departing-iso',
            layout: {
                'text-field': ['concat', ['to-string', ['/', ['get', 'Contour'], 60]],
                ['case',
                ['==', ['to-number', ['get', 'Contour']], 60],
                ' hr',
                ' hrs'
                ]],
                'text-font': ['Open Sans Bold'],
                'text-size': [
                "interpolate",
                ["linear"],
                ["zoom"],
                2, 8, // At zoom level 3, text size is 10
                10, 20 // At zoom level 10, text size is 16
                ],
                'symbol-placement': 'line',
                'symbol-spacing': 400,
            },
            'paint': {
                'text-color': '#fff', // White text color
                'text-halo-color': '#494847', // Grey halo for background effect
                'text-halo-width': 2.5, // Halo width
            }
        });
        
        map.addLayer({
            id: 'arriving-isochrones',
            type: 'line',
            source: 'arriving-iso',
            paint: {'line-color': getColorScale('Contour'),
            'line-width': 2 
        },
        'layout': {
            'visibility': 'none' // Hidden by default
        },
    });
    
    map.addLayer({
        id: 'arriving-isochrones-labels',
        type: 'symbol',
        source: 'arriving-iso',
        layout: {
            'visibility': 'none',
            'text-field': ['concat', ['to-string', ['/', ['get', 'Contour'], 60]],
            ['case',
            ['==', ['to-number', ['get', 'Contour']], 60],
            ' hr',
            ' hrs'
            ]],
            'text-font': ['Open Sans Bold'],
            'text-size': [
                "interpolate",
                ["linear"],
                ["zoom"],
                2, 8, // At zoom level 3, text size is 10
                10, 20 // At zoom level 10, text size is 16
                ],
            'symbol-placement': 'line',
            'symbol-spacing': 400,
        },
        'paint': {
            'text-color': '#fff', // White text color
            'text-halo-color': '#494847', // Grey halo for background effect
            'text-halo-width': 2.5, // Halo width
        }
    });
    
    map.addSource('departing-poly', {
        type: 'geojson',
        data: departingPolygon
    });
    
    map.addSource('arriving-poly', {
        type: 'geojson',
        data: arrivingPolygon
    });
    
    map.addLayer({
        id: 'departing-polygons',
        type: 'fill',
        source: 'departing-poly',
        paint: {
            'fill-color': getColorScale('ContourMax'),
            'fill-opacity': 0.2  // Semi-transparent polygons
        },
        layout: {
            'visibility': 'none' // Hidden by default
        },
    });
    
    map.addLayer({
        id: 'arriving-polygons',
        type: 'fill',
        source: 'arriving-poly',
        paint: {
            'fill-color': getColorScale('ContourMax'),
            'fill-opacity': 0.2  // Semi-transparent polygons
        },
        layout: {
            'visibility': 'none' // Hidden by default
        },
    });
    
});

this.map = map;
},

unmounted() {
    this.map.remove();
    this.map = null;
},

methods: {
    // On clicking the reset button on sidebar
    resetMapInternal() {
        // Show the 'airport-points' layer and legend
        this.map.setLayoutProperty('airport-points', 'visibility', 'visible');
        this.map.setLayoutProperty('airport-icon', 'visibility', 'visible');
        this.map.setLayoutProperty('airport-labels', 'visibility', 'visible');
        
        this.showAirportLegend = true;
        
        // Remove additional layers and sources
        const layersToRemove = ['points-labels', 'points-dest', 'routes', 'output-extent', 
        'departing-isochrones', 'arriving-isochrones', 'arriving-isochrones-labels', 'departing-isochrones-labels',
        'routes-hover', 'plane_points', 'departing-polygons', 'arriving-polygons'];
        layersToRemove.forEach((id) => {
            if (this.map.getLayer(id)) {
                this.map.removeLayer(id);
            }
        });
        const sourcesToRemove = ['points', 'routes', 'output-extent', 'departing-iso', 'arriving-iso', 'plane_points', 'departing-poly', 'arriving-poly'];
        sourcesToRemove.forEach((id) => {
            if (this.map.getSource(id)) {
                this.map.removeSource(id);
            }
        });
        
        this.map.setLayoutProperty('wind-layer', 'visibility', 'none'); // Turn off wind layer
        this.durationFilter = 20; // Reset filter value
        this.geojsonSubset = null;
        this.$emit('reset-filter');
    },
    
    // Filter routes on map based on duration and frequency sliders on Sidebar
    filterRoutes(duration, frequency) {
        // Convert the duration from hours to minutes
        const durationInMinutes = duration * 60;
        
        const filteredGeojson = {
            ...this.geojson,
            features: this.geojson.features.filter((feature) => {
                const isDeparting = this.map.getLayoutProperty('arriving-isochrones', 'visibility') === 'none';
                const featureDuration = isDeparting
                ? feature.properties.Duration__minutes_
                : feature.properties.Reverse_Duration__minutes_;
                
                const featureFrequency = feature.properties.Flights_per_Day
                
                return featureDuration <= durationInMinutes && featureFrequency >= frequency;
            })
        };
        // Update map layer, table, and animation spaces based on current filters
        this.map.getSource('routes').setData(filteredGeojson);
        this.$emit('routes-loaded', filteredGeojson);
        this.geojsonSubset = filteredGeojson
    },
    
    // Animates flight routes when animate button is clicked on Sidebar

    //  ------------------------------------------------------------
    //  Code generated by: ChatGPT, OpenAI
    //  Date of generation: 2024-12-02
    //  Purpose: Adapt code from Mapbox example to animate routes to fit to my needs,
    //           help create cases for routes that cross over IDL
    //  Prompt: Several various iterations for different parts of the code.
    //  ------------------------------------------------------------

    animateRoutes() {
        const isDeparting = this.map.getLayoutProperty('arriving-isochrones', 'visibility') === 'none';
        const durationProperty = isDeparting ? 'Duration__minutes_' : 'Reverse_Duration__minutes_';
        const secondsPerHour = 1; // Animation duration in seconds per hour
        const pointsPerSecond = 10; // Number of frames per second
        
        let flattenedFeatures;
        
        // If there is currently a filter, animate over the filtered routes
        if (this.geojsonSubset) {
            // Handle MultiLineString by flattening to LineString features
            flattenedFeatures = this.geojsonSubset.features.flatMap((feature, index) => {
                if (feature.geometry.type === 'MultiLineString') {
                    let mergedCoordinates;
                    // Handle case for routes going west over the IDL
                    if(
                    feature.properties.Departure_Airport == 'NRT' ||
                    feature.properties.Departure_Airport == 'ICN' ||
                    feature.properties.Departure_Airport == 'SYD' ||
                    feature.properties.Departure_Airport == 'HKG' ||
                    feature.properties.Departure_Airport == 'BKK' ||
                    feature.properties.Departure_Airport == 'SIN'
                    ) {
                        const mergedCoordinates = feature.geometry.coordinates[0].concat(feature.geometry.coordinates[1]);
                        return {
                            type: 'Feature',
                            properties: { ...feature.properties, routeIndex: index },
                            geometry: { type: 'LineString', coordinates: mergedCoordinates },
                        };
                    } else 
                    // Handle case for routes going east over the IDL
                    {
                        const coords1 = feature.geometry.coordinates[0];
                        const coords2 = feature.geometry.coordinates[1];
                        
                        // Determine the correct direction and concatenate accordingly
                        if (coords1[coords1.length - 1][0] < coords2[0][0]) {
                            // If the last point of the first line is less than the first point of the second, concatenate normally
                            mergedCoordinates = coords1.concat(coords2);
                        } else {
                            // Otherwise, reverse the order to ensure continuity across the IDL
                            mergedCoordinates = coords2.concat(coords1);
                        }
                        // Ensure continuity across IDL by adjusting the longitude values if needed
                        mergedCoordinates = mergedCoordinates.map(([lon, lat]) => {
                            if (lon < -180) {
                                return [lon + 360, lat];
                            } else if (lon > 180) {
                                return [lon - 360, lat];
                            } else {
                                return [lon, lat];
                            }
                        });
                    }
                    return {
                        type: 'Feature',
                        properties: { ...feature.properties, routeIndex: index },
                        geometry: { type: 'LineString', coordinates: mergedCoordinates },
                    };
                } else if (feature.geometry.type === 'LineString') {
                    return { ...feature, properties: { ...feature.properties, routeIndex: index } };
                } else {
                    console.warn(`Unsupported geometry type: ${feature.geometry.type}`);
                    return [];
                }
            });
        } else { // Default case, run animation over all routes
            // Handle MultiLineString by flattening to LineString features
            flattenedFeatures = this.geojson.features.flatMap((feature, index) => {
                if (feature.geometry.type === 'MultiLineString') {
                    let mergedCoordinates;
                    // Handle case from going west over the IDL
                    if(
                    feature.properties.Departure_Airport == 'NRT' ||
                    feature.properties.Departure_Airport == 'ICN' ||
                    feature.properties.Departure_Airport == 'SYD' ||
                    feature.properties.Departure_Airport == 'HKG' ||
                    feature.properties.Departure_Airport == 'BKK' ||
                    feature.properties.Departure_Airport == 'SIN'
                    ) {
                        const mergedCoordinates = feature.geometry.coordinates[0].concat(feature.geometry.coordinates[1]);
                        return {
                            type: 'Feature',
                            properties: { ...feature.properties, routeIndex: index },
                            geometry: { type: 'LineString', coordinates: mergedCoordinates },
                        };
                    } else 
                    // Handle case going east over the IDL
                    {
                        const coords1 = feature.geometry.coordinates[0];
                        const coords2 = feature.geometry.coordinates[1];
                        
                        // Determine the correct direction and concatenate accordingly
                        if (coords1[coords1.length - 1][0] < coords2[0][0]) {
                            // If the last point of the first line is less than the first point of the second, concatenate normally
                            mergedCoordinates = coords1.concat(coords2);
                        } else {
                            // Otherwise, reverse the order to ensure continuity across the IDL
                            mergedCoordinates = coords2.concat(coords1);
                        }
                        // Ensure continuity across IDL by adjusting the longitude values if needed
                        mergedCoordinates = mergedCoordinates.map(([lon, lat]) => {
                            if (lon < -180) {
                                return [lon + 360, lat];
                            } else if (lon > 180) {
                                return [lon - 360, lat];
                            } else {
                                return [lon, lat];
                            }
                        });
                    }
                    return {
                        type: 'Feature',
                        properties: { ...feature.properties, routeIndex: index },
                        geometry: { type: 'LineString', coordinates: mergedCoordinates },
                    };
                } else if (feature.geometry.type === 'LineString') {
                    return { ...feature, properties: { ...feature.properties, routeIndex: index } };
                } else {
                    console.warn(`Unsupported geometry type: ${feature.geometry.type}`);
                    return [];
                }
            });
        }
        
        // Define plane points geojson
        const planePoints = {
            type: 'FeatureCollection',
            features: flattenedFeatures.map((feature) => ({
                type: 'Feature',
                properties: { routeIndex: feature.properties.routeIndex, duration: feature.properties[durationProperty] },
                geometry: {
                    type: 'Point',
                    coordinates: feature.geometry.coordinates[0], // Start at the first coordinate
                },
            })),
        };
        
        // Precompute arcs for all routes
        const lineArcs = flattenedFeatures.map((route, idx) => {
            const lineDistance = turf.length(route);
            const durationMinutes = route.properties[durationProperty];
            const steps = (durationMinutes / 60) * pointsPerSecond * secondsPerHour;
            
            const arc = [];
            if (lineDistance > 0 && steps > 0) {
                for (let i = 0; i < lineDistance; i += lineDistance / steps) {
                    const segment = turf.along(route, i);
                    arc.push(segment.geometry.coordinates);
                }
                // Ensure the last coordinate of the line is included
                arc.push(route.geometry.coordinates[route.geometry.coordinates.length - 1]);
            }
            // Reverse the arc if inbound flight
            return isDeparting ? arc : arc.reverse();
        });
        
        // Add a single source for all animated points
        if (!this.map.getSource('plane_points')) {
            this.map.addSource('plane_points', {
                type: 'geojson',
                data: planePoints,
            });
            
            this.map.addLayer({
                id: 'plane_points',
                type: 'circle',
                source: 'plane_points',
                paint: {
                    'circle-radius': 6,
                    'circle-color': '#ff0000',
                    'circle-opacity': 0.8,
                },
            });
        }
        
        let frame = 0;
        
        // Step over animation
        const animate = () => {
            let active = false;
            
            planePoints.features.forEach((feature, index) => {
                const durationMinutes = feature.properties.duration;
                const totalSteps = (durationMinutes / 60) * pointsPerSecond * secondsPerHour;
                
                // Ensure the last point is reached
                if (frame <= totalSteps && lineArcs[index][frame]) {
                    feature.geometry.coordinates = lineArcs[index][frame];
                    active = true; // Keep animating while at least one point is active
                } else if (frame > totalSteps) {
                    feature.geometry.coordinates = lineArcs[index][lineArcs[index].length - 1];
                }
            });
            
            // Update the source in one operation
            this.map.getSource('plane_points').setData(planePoints);
            
            if (active) {
                frame++;
                requestAnimationFrame(animate);
            }
        };
        
        animate();
    },
}

};
</script>

<style>
.map-container {
    flex: 1;
    transition: width 0.3s ease; /* Smooth transition */
    height: 100vh; /* Full-height map */
}
.map-legend {
    position: absolute;
    bottom: 20px;
    right: 20px;
    background-color: rgba(35, 55, 75, 0.9);
    color: #ffffff;
    padding: 10px;
    border-radius: 8px;
    font-family: monospace;
    z-index: 1;
}

.legend-item {
    display: flex;
    align-items: center;
    margin-bottom: 8px;
}

#airport-legend .legend-item {
    display: flex; /* Use flexbox to align items */
    align-items: center; /* Vertically align symbol and label */
    justify-content: space-between; /* Space between symbol and label */
    margin-bottom: 8px;
}

.legend-symbol {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    border: 2px solid #ffffff;
    margin-right: 10px;
}

.legend-icon {
    font-size: 14px;
    color: #ffffff;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}

.legend-label-route {
    font-size: 12px;
    padding-left: 5px;
}

.legend-label-airport {
    font-size: 12px;
}

</style>