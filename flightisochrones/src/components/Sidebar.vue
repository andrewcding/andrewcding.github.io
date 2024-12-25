<template>
    <!-- Alter width of Sidebar based on if table is shown or not -->
    <div id="sidebar" :class="{ hidden: !visible }" :style="{ width: showTable ? '32%' : '20%' }">
        
        <!-- Vary the size of header text based on if airport is selected or not-->
        <h2 v-if="!airportSelected">{{ headerText }}</h2>
        <h3 v-if="airportSelected">{{ headerText }}</h3>
        
        <span v-if="!airportSelected" style="color:#b5b5b5">A project by Andrew Ding</span>
        
        <!-- Vary spacing around horizontal line based on if table is shown -->
        <hr v-if="!showTable" style="margin-top: 15px; margin-bottom: 15px;">
        <hr v-if="showTable" style="margin-top: 10px; margin-bottom: 3px;">
        
        <!-- Sidebar elements for when airport is selected AND table is not shown -->
        <div v-if="airportSelected  && !showTable">
            <h3>Toggles</h3>
            <!-- Toggle Sliders -->
            <div class="slider-container">
                <div class="slider-container">
                    <div class="slider">
                        <label class="switch">
                            <input type="checkbox" id="slider-direction" v-model="sliderValues.direction" @change="toggleIsochroneLayer" />
                            <span class="slider-round"></span>
                        </label>
                        <label for="slider-direction">Outbound / Inbound</label>
                    </div>
                    <div class="slider">
                        <label class="switch">
                            <input type="checkbox" id="slider-route" v-model="sliderValues.route" @change="toggleRouteSymbology" />
                            <span class="slider-round"></span>
                        </label>
                        <label for="slider-route">Travel Time Difference</label>
                    </div>
                    <div class="slider">
                        <label class="switch">
                            <input type="checkbox" id="slider-isoPoly" v-model="sliderValues.isoPoly" @change="toggleIsoPoly"/>
                            <span class="slider-round"></span>
                        </label>
                        <label for="slider-isoPoly">Isochrone Contours / Polygons</label>
                    </div>
                </div>
                <div class="slider">
                    <label class="switch">
                        <input type="checkbox" id="slider-wind" v-model="sliderValues.wind" @change="toggleWindLayer" />
                        <span class="slider-round"></span>
                    </label>
                    <label for="slider-wind">Wind Layer</label>
                </div>
            </div>
            <!-- Filter Sliders -->
            <div class="filter-container">
                <h3><b>Filter</b></h3>
                <label for="durationFilter" class="filter-label">Duration: < {{ formattedDuration }}</label>
                
                <input type="range" min="0" max="20" value="20" v-model="durationFilter" 
                @input="filterRoutes"  class="filter" id="durationFilter">
                <div class="filter-labels">
                    <span>0 hr</span>
                    <span>20 hrs</span>
                </div>
                
                <label for="frequencyFilter" class="filter-label">Frequency: > {{ frequencyFilter }} daily flights</label>
                
                <input type="range" min="0" max="15" value="0" v-model="frequencyFilter" @input="filterRoutes" class="filter" id="frequencyFilter">
                <div class="filter-labels">
                    <span>0 flights/day</span>
                    <span>15 flights/day</span>
                </div>
            </div>
            <!-- Animation Button -->
            <div>
                <h3 style="padding-bottom: 5px;"><b>Animate</b></h3>
                <div id="text-button" style="font-size: 14px" @click="$emit('trigger-animation')">► Animate Routes</div>
            </div>
        </div>
        
        <!-- Table Components -->
        <div v-if="airportSelected" style="margin-top:15px; margin-bottom: 10px;">
            
            <!-- Buttons to Open Table -->
            <h3 style="padding-bottom: 5px;" v-if='!showTable'>Routes Table</h3>
            <div id="text-button" style="font-size: 14px" v-if='!showTable' @click="toggleTableVisibility">
                ▲ Show Table
            </div>
            
            <!-- Table Opened Componenets -->
            <div v-if="showTable">
                <!-- Search Input -->
                <input type="text" v-model="searchQuery" @input="filterTable" placeholder="Search routes..." class="search-input">
            </div>
            <transition name="slide-up">
                <!-- Table -->
                <div v-if="showTable" class="route-table-container">
                    <table class="route-table">
                        <!-- Table Headers -->
                        <thead>
                            <tr>
                                <th @click="sortTable('Destination_Name')">
                                    Destination
                                    <span v-if="sortKey === 'Destination_Name'">
                                        <span v-if="sortDirection === 1">▲</span>
                                        <span v-else>▼</span>
                                    </span>
                                </th>
                                <th @click="sortTable('Destination_Code')">
                                    Airport Code
                                    <span v-if="sortKey === 'Destination_Code'">
                                        <span v-if="sortDirection === 1">▲</span>
                                        <span v-else>▼</span>
                                    </span>
                                </th>
                                <th @click="sortTable('Country')">
                                    Country
                                    <span v-if="sortKey === 'Country'">
                                        <span v-if="sortDirection === 1">▲</span>
                                        <span v-else>▼</span>
                                    </span>
                                </th>
                                <th @click="sortTable('Duration')">
                                    Duration
                                    <span v-if="sortKey === 'Duration'">
                                        <span v-if="sortDirection === 1">▲</span>
                                        <span v-else>▼</span>
                                    </span>
                                </th>
                                <th @click="sortTable('Distance__km_')">
                                    Distance
                                    <span v-if="sortKey === 'Distance__km_'">
                                        <span v-if="sortDirection === 1">▲</span>
                                        <span v-else>▼</span>
                                    </span>
                                </th>
                                <th @click="sortTable('Flights_per_Day')">
                                    Daily Flights
                                    <span v-if="sortKey === 'Flights_per_Day'">
                                        <span v-if="sortDirection === 1">▲</span>
                                        <span v-else>▼</span>
                                    </span>
                                </th>
                            </tr>
                        </thead>
                        <!-- Table Elements -->
                        <tbody>
                            <tr v-for="route in filteredRoutes" :key="route.properties.Destination_Code" @click="zoomToRoute(route)">
                                <td>{{ route.properties.Destination_Name }}</td>
                                <td>{{ route.properties.Destination_Code }}</td>
                                <td>{{ route.properties.Country }}</td>
                                <td>{{ formatDuration(route) }}</td>
                                <td>{{ route.properties.Distance__km_ }} km</td>
                                <td>{{ route.properties.Flights_per_Day }}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </transition>
        </div>
        
        <!-- Button to close table -->
        <div id="text-button" style="font-size: 14px;" v-if='showTable' @click="toggleTableVisibility">
            ▼ Close Table
        </div>
        
        <!-- Intro blurb -->
        <div v-if="!airportSelected" style="font-size: 14px;">
            <p>This application visualizes direct flights from major airport hubs and their isochrones.</p>
            <br>
            <p>
                An isochrone is a line that delineates areas which can be reached in a given amount of time.
                For example, the 2 hour isochrone encircles all areas that can be reached within 2 hours or less.
            </p>
            <br>
            <p>
                By using isochrones, we can visualize the spatiotemporal aspects of air travel, which can demonstrate
                the effect of the jet stream, increased travel time due to congested airspaces, as well as the differences
                between inbound and outbound flight times.
            </p>
            <br>
            <h3>Select an airport to get started!</h3>
        </div>
        
        <!-- Data Attribution -->
        <div v-if="!airportSelected" class="attribution-text" @click="$emit('show-attribution')">
            Data Attribution
        </div>
        
        <!-- Reset Button -->
        <div v-if="airportSelected" class="reset-button-container">
            <div id="text-button" class="reset-button" @click="$emit('reset-map')">↻ Reset</div>
        </div>
    </div>
    
</template>

<script>

export default {
    props: {
        visible: {
            type: Boolean,
            default: true,
        },
        airportSelected: {
            type: Boolean,
            default: false,
        },
        duration: {
            type: Number,
            default: 20,
        },
        routes: {
            type: Object,
            default: () => ({ features: [] }), // Default empty GeoJSON
        },
        headerText: {
            type: String,
            default: 'Flight Isochrones ✈'
        },
    },
    data() {
        return {
            // Intialize variables
            durationFilter: 20,
            frequencyFilter: 0,
            sliderValues: {
                direction: false,
                route: false,
                wind: false,
            },
            showTable: false,
            searchQuery: '',
            // Table Intially sorted by flights per day, descending
            sortKey: "Flights_per_Day",
            sortDirection : -1,
        };
    },
    computed: {
        
        formattedDuration() {
            const hours = this.durationFilter;
            return `${hours} ${hours === 1 ? 'hr' : 'hrs'}`;
        },
        
        // Filters routes in table by search bar
        filteredRoutes() {
            if (!this.searchQuery) {
                return this.routes.features; // Return all routes if no search query
            }
            // Convert the search query to lowercase for case-insensitive search
            const query = this.searchQuery.toLowerCase();
            
            return this.routes.features.filter(route => {
                const destinationName = route.properties.Destination_Name.toLowerCase();
                const destinationCode = route.properties.Destination_Code.toLowerCase();
                const Country = route.properties.Country.toLowerCase();
                
                // Format the duration to include "XhYm"
                const isDeparting = this.map.getLayoutProperty('arriving-isochrones', 'visibility') === 'none';
                const durationInMinutes = isDeparting
                ? route.properties.Duration__minutes_
                : route.properties.Reverse_Duration__minutes_;
                const durationHours = Math.floor(durationInMinutes / 60);
                const durationMinutes = durationInMinutes % 60;
                const formattedDuration = `${durationHours}h${durationMinutes}m`;
                
                return (
                destinationName.includes(query) ||
                destinationCode.includes(query) ||
                Country.includes(query) ||
                formattedDuration.includes(query) // Allow searching only by formatted duration like "5h13m"
                );
            });
        }
    },
    methods: {
        // Update header text with airport name and code when selected
        updateHeaderText(airportName, airportCode) {
            this.headerText = `${airportName} (${airportCode}) ✈`; // Update the header with the selected airport name and code
        },
        // Grab data from Map.vue for current routes on map and increase width of sidebar
        toggleTableVisibility() {
            // Toggle the table visibility
            this.showTable = !this.showTable;
            
            this.$emit('update-show-table', this.showTable);
            
            // Temporarily disable overflow during animation
            const sidebar = document.getElementById('sidebar');
            sidebar.style.overflowY = 'hidden';
            
            const padding = this.showTable ? { left: 500 } : { left: 300 };
            this.map.easeTo({
                padding: padding,
                duration: 600 
            });
            
            // Restore overflow after animation completes
            setTimeout(() => {
                sidebar.style.overflowY = 'auto';
            }, 1000);
            
            // If a route is selected from clicking on table row, remove when the table is closed
            if (this.highlightedRouteCode) {
                // Reset the routes' paint properties to the original state
                this.map.setPaintProperty('routes', 'line-color', '#ffffff'); // Default color
                this.map.setPaintProperty('routes', 'line-width', 1); // Default width
                
                // Clear the highlighted route code
                this.highlightedRouteCode = null;
            }
        },
        
        // Reset variables when the airport is reset
        resetSlider() {
            this.durationFilter = 20; // Reset the slider value to 20 hours
            this.frequencyFilter = 0; 
            this.sliderValues.direction = false;
            this.sliderValues.isoPoly = false;
            this.sliderValues.route = false;
            this.sliderValues.wind = false;
            this.searchQuery = '';
            this.sortKey = "Flights_per_Day";
            this.sortDirection = -1;
            
            // Move globe back to middle if the table is open and map is reset (Sidebar returns to normal width)
            if(this.showTable) {
                this.showTable = false;
                
                this.map.easeTo({
                    padding: { left: 300 },
                    duration: 600 
                });
            }
        },
        
        // Swap between arriving / departing isocrhone layers based on state of toggle
        toggleIsochroneLayer() {
            if (this.sliderValues.direction) {
                this.map.setLayoutProperty('departing-isochrones', 'visibility', 'none');
                this.map.setLayoutProperty('arriving-isochrones', 'visibility', 'visible');
                
                this.map.setLayoutProperty('departing-isochrones-labels', 'visibility', 'none');
                this.map.setLayoutProperty('arriving-isochrones-labels', 'visibility', 'visible');
            } else {
                this.map.setLayoutProperty('arriving-isochrones', 'visibility', 'none');
                this.map.setLayoutProperty('departing-isochrones', 'visibility', 'visible');
                
                this.map.setLayoutProperty('arriving-isochrones-labels', 'visibility', 'none');
                this.map.setLayoutProperty('departing-isochrones-labels', 'visibility', 'visible');
            }
            
            if (this.sliderValues.isoPoly) {
                if (this.sliderValues.direction) {
                    this.map.setLayoutProperty('arriving-polygons', 'visibility', 'visible');
                    this.map.setLayoutProperty('departing-polygons', 'visibility', 'none');
                } else {
                    // Show departing-polygons, hide arriving-polygons
                    this.map.setLayoutProperty('arriving-polygons', 'visibility', 'none');
                    this.map.setLayoutProperty('departing-polygons', 'visibility', 'visible');
                }
            }
            
            // Rerun filter (duration may change based on depart/arrive direction)
            if (this.durationFilter != 20 || this.frequencyFilter != 0) {
                this.filterRoutes();
            }
            
            // Change route difference colours
            if (this.sliderValues.route) {
                if(this.map.getLayoutProperty('arriving-isochrones', 'visibility') === 'none') {
                    this.map.setPaintProperty('routes', 'line-color', [
                    'interpolate',
                    ['linear'],
                    ['-', ['get', 'Duration__minutes_'], ['get', 'Reverse_Duration__minutes_']],
                    -90, '#1a9641',  // Green for the minimum value (save time)
                    -45, '#a6d96a',
                    0, '#ffffbf',    // White for 0
                    45, '#fdae61',
                    90, '#d7191c'    // Red for the maximum value (more time)
                    ]);
                } else {
                    this.map.setPaintProperty('routes', 'line-color', [
                    'interpolate',
                    ['linear'],
                    ['-', ['get', 'Reverse_Duration__minutes_'], ['get', 'Duration__minutes_']],
                    -90, '#1a9641',  // Green for the minimum value (save time)
                    -45, '#a6d96a',
                    0, '#ffffbf',    // White for 0
                    45, '#fdae61',
                    90, '#d7191c'    // Red for the maximum value (more time)
                    ]);
                }
            }
        },
        // Turn on / off isochrone polygons based on state of toggle
        toggleIsoPoly() {
            // If toggle is off, hide iscorhone polygon layers
            if (!this.sliderValues.isoPoly) {
                this.map.setLayoutProperty('arriving-polygons', 'visibility', 'none');
                this.map.setLayoutProperty('departing-polygons', 'visibility', 'none');
                return;
            }
            // If toggle is on, show the appropriate layer based on direction toggle
            if (this.sliderValues.direction) {
                // Show arriving-polygons, hide departing-polygons
                this.map.setLayoutProperty('arriving-polygons', 'visibility', 'visible');
                this.map.setLayoutProperty('departing-polygons', 'visibility', 'none');
            } else {
                // Show departing-polygons, hide arriving-polygons
                this.map.setLayoutProperty('arriving-polygons', 'visibility', 'none');
                this.map.setLayoutProperty('departing-polygons', 'visibility', 'visible');
            }
        },
        // Set the multivariate route symbology
        toggleRouteSymbology() {
            if (this.sliderValues.route) {
                // Departing case
                if(this.map.getLayoutProperty('arriving-isochrones', 'visibility') === 'none') {
                    this.map.setPaintProperty('routes', 'line-color', ['interpolate',
                    ['linear'],
                    // Calculate percentage difference
                    [ '*',
                    ['/', // Division to calculate percentage
                    ['-', ['get', 'Duration__minutes_'], ['get', 'Reverse_Duration__minutes_']], 
                    ['/', // Average denominator
                    ['+', ['get', 'Duration__minutes_'], ['get', 'Reverse_Duration__minutes_']],
                    2 // Divide by 2 for average
                    ]],100 // Convert to percentage
                    ],
                    -20, '#1a9641',  // Green for -20% faster
                    -10, '#a6d96a',  // Light green for -10% faster
                    0, '#ffffbf',    // Yellow for no difference
                    10, '#fdae61',   // Orange for 10% slower
                    20, '#d7191c'    // Red for 20% slower
                    ]);
                } else { // Arriving case
                    this.map.setPaintProperty('routes', 'line-color', ['interpolate',
                    ['linear'],
                    // Calculate percentage difference
                    ['*',
                    ['/', // Division to calculate percentage
                    ['-', ['get', 'Reverse_Duration__minutes_'], ['get', 'Duration__minutes_']], // Difference
                    [
                    '/', // Average denominator
                    ['+', ['get', 'Duration__minutes_'], ['get', 'Reverse_Duration__minutes_']], // Sum of the two durations
                    2 // Divide by 2 for average
                    ]],100 // Convert to percentage
                    ],
                    -20, '#1a9641',  // Green for -20% faster
                    -10, '#a6d96a',  // Light green for -10% faster
                    0, '#ffffbf',    // Yellow for no difference
                    10, '#fdae61',   // Orange for 10% slower
                    20, '#d7191c'    // Red for 20% slower
                    ]);
                }
                // Set line width based on flight frequency
                this.map.setPaintProperty('routes', 'line-width', [
                'interpolate',
                ['linear'],
                ['+', ['to-number', ['get', 'Flights_per_Day']], 1],
                1, 1.5,           // 1 flight to 1.5 pt width
                3, 3,             // 3 flights to 3 pt width
                5, 5,             // 3 flights to 3 pt width
                10, 8,             // 3 flights to 3 pt width
                15, 10            // 10 flights to 15 pt width
                ]);
                // Tell App.vue to tell Map.vue to turn on the legend
                this.$emit('toggle-route-legend', true);
            } else {
                // If toggle is off, reset symbology to original
                this.map.setPaintProperty('routes', 'line-color', '#ffffff');
                this.map.setPaintProperty('routes', 'line-width', 1);
                // Tell App.vue to tell Map.vue to turn off the legend
                this.$emit('toggle-route-legend', false);
            }
        },
        // Show wind layer based on state of toggle
        toggleWindLayer() {
            if (this.sliderValues.wind) {
                if (this.map.getLayer('wind-layer')) {
                    this.map.setLayoutProperty('wind-layer', 'visibility', 'visible');
                }
            } else {
                if (this.map.getLayer('wind-layer')) {
                    this.map.setLayoutProperty('wind-layer', 'visibility', 'none');
                }
            }
        },
        filterRoutes() {
            // Emit the filter value from sliders to App.vue to tell Map.vue to filter 'route' symbology layer
            this.$emit('filter-routes', this.durationFilter, this.frequencyFilter);
        },
        // Format the duration from minutes into hours and minutes
        formatDuration(route) {
            const isDeparting = this.map.getLayoutProperty('arriving-isochrones', 'visibility') === 'none';
            const durationInMinutes = isDeparting
            ? route.properties.Duration__minutes_
            : route.properties.Reverse_Duration__minutes_;
            const hours = Math.floor(durationInMinutes / 60);
            const minutes = durationInMinutes % 60;
            return `${hours}h${minutes}m`;
        },
        // Sort the table by ascending or descending by key
        sortTable(key) {
            if (this.sortKey === key) {
                this.sortDirection *= -1; // Toggle between ascending and descending
            } else {
                this.sortKey = key;
                this.sortDirection = 1; // Default to ascending
            }
            
            const isDeparting = this.map.getLayoutProperty('arriving-isochrones', 'visibility') === 'none';
            
            this.routes.features.sort((a, b) => {
                let valA, valB;
                
                if (key === 'Duration') {
                    // Get the appropriate duration property based on departing or arriving
                    valA = isDeparting ? a.properties.Duration__minutes_ : a.properties.Reverse_Duration__minutes_;
                    valB = isDeparting ? b.properties.Duration__minutes_ : b.properties.Reverse_Duration__minutes_;
                } else {
                    valA = a.properties[key];
                    valB = b.properties[key];
                    
                    // Handle string comparison by converting to lowercase
                    if (typeof valA === 'string') {
                        valA = valA.toLowerCase();
                        valB = valB.toLowerCase();
                    }
                }
                
                if (valA < valB) return -1 * this.sortDirection;
                if (valA > valB) return 1 * this.sortDirection;
                return 0;
            });
        },
        // When row in table is clicked, zoom to the clicked route
        zoomToRoute(route) {
            
            // Automatically turn off duration difference symbology + toggle
            this.sliderValues.route = false;
            this.$emit('toggle-route-legend', false);
            
            const map = this.map;
            
            if (map) {
                const routeData = route.geometry;
                const coordinates = routeData.type === "LineString"
                ? routeData.coordinates
                : routeData.coordinates.flat(); // Flatten for MultiLineString
                
                // Extract first, middle, and last points
                const firstPoint = coordinates[0];
                const lastPoint = coordinates[coordinates.length - 1];
                const midIndex = Math.floor(coordinates.length / 2);
                const midPoint = coordinates[midIndex];
                
                // Initialize min and max bounds with the first point
                let minLng = firstPoint[0];
                let maxLng = firstPoint[0];
                let minLat = firstPoint[1];
                let maxLat = firstPoint[1];
                
                // Update bounds with first, mid, and last points
                [firstPoint, midPoint, lastPoint].forEach(point => {
                    const [lng, lat] = point;
                    
                    if (lng < minLng) minLng = lng;
                    if (lng > maxLng) maxLng = lng;
                    if (lat < minLat) minLat = lat;
                    if (lat > maxLat) maxLat = lat;
                });
                
                //  ------------------------------------------------------------
                //  Code generated by: ChatGPT, OpenAI
                //  Date of generation: 2024-12-01
                //  Purpose: Fix cases for routes crossing IDL
                //  Prompt: Here is this code ... fix it to cover case where it crosses IDL
                //  ------------------------------------------------------------

                // Handle International Date Line crossing
                if (maxLng - minLng > 180) {
                    // Adjust for the IDL by wrapping longitudes appropriately
                    minLng = Math.min(
                    firstPoint[0] < 0 ? firstPoint[0] + 360 : firstPoint[0],
                    midPoint[0] < 0 ? midPoint[0] + 360 : midPoint[0],
                    lastPoint[0] < 0 ? lastPoint[0] + 360 : lastPoint[0]
                    );
                    maxLng = Math.max(
                    firstPoint[0] < 0 ? firstPoint[0] + 360 : firstPoint[0],
                    midPoint[0] < 0 ? midPoint[0] + 360 : midPoint[0],
                    lastPoint[0] < 0 ? lastPoint[0] + 360 : lastPoint[0]
                    );
                }
                
                // Define bounds using the calculated min and max values
                const bounds = [
                [minLng, minLat], // Southwest corner
                [maxLng, maxLat]  // Northeast corner
                ];
                
                // Fit the map to the bounds, adjusting the padding to account for the sidebar
                map.fitBounds(bounds, {
                    padding: {
                        top: 50,
                        bottom: 50,
                        right: 50,
                        left: map.getContainer().clientWidth * 0.32 + 50, // 32% of the map width plus some extra for visibility
                    },
                    duration: 1000 // Animation duration in milliseconds
                });
                
                // Highlight the specific route
                const highlightedColor = '#ff0000'; // Red color to highlight
                const highlightedWidth = 5; // Wider line for highlighting
                
                // Update the layer with the new paint properties
                map.setPaintProperty('routes', 'line-color', [
                'case',
                ['==', ['get', 'Destination_Code'], route.properties.Destination_Code],
                highlightedColor,
                '#ffffff' // Default color for non-highlighted lines
                ]);
                map.setPaintProperty('routes', 'line-width', [
                'case',
                ['==', ['get', 'Destination_Code'], route.properties.Destination_Code],
                highlightedWidth,
                1 // Default line width
                ]);
                
                // Store the currently highlighted route to reset later
                this.highlightedRouteCode = route.properties.Destination_Code;
            }
        }
        
    },
    mounted() {
        this.$nextTick(() => {
            this.map = this.$parent.$refs.mapComponent.map;
        });
    }
};
</script>

<style scoped>
#sidebar {
    background-color: rgb(35 55 75 / 90%);
    color: #fff;
    padding: 16px;
    font-family: monospace;
    position: absolute;
    top: 0;
    left: 0;
    height: 100%;
    width: 20%;
    overflow-y: auto;
    transition: transform 0.3s ease-in-out, width 0.3s ease-in-out;
    /* Smooth transition for sliding in/out */
    transform: translateX(0);
    /* Flexbox layout */
    display: flex; 
    flex-direction: column; /* Stack children vertically */
}


#sidebar.hidden {
    transform: translateX(-100%);
    /* Slide sidebar off-screen */
}

/* Scrollbar styling */
#sidebar::-webkit-scrollbar {
    width: 8px; /* Adjust width as needed */
}

#sidebar::-webkit-scrollbar-thumb {
    background: rgb(59, 74, 92); /* Darker thumb for scrollbar */
    border-radius: 4px; /* Rounded corners for scrollbar */
}

#sidebar::-webkit-scrollbar-thumb:hover {
    background: rgb(95, 115, 135); /* Slightly lighter on hover */
}

#sidebar::-webkit-scrollbar-track {
    background: rgb(35 55 75 / 90%); /* Background for the scrollbar track */
}

#text-button {
    cursor: pointer;
    color: #ffffff; /* White text */
    font-size: 14px;
    font-weight: bold; /* Make text more prominent */
    user-select: none; /* Prevent text selection */
    height: 40px;
    transition: color 0.3s, background-color 0.3s, box-shadow 0.3s; /* Smooth transitions */
    padding: 8px 12px; /* Add padding for a button-like feel */
    border: 2px solid #ffffff; /* Add a border to highlight the button */
    border-radius: 6px; /* Rounded corners for a button-like appearance */
    background-color: transparent; /* Transparent background by default */
    text-align: center; /* Center the text */
}

/* Hover effect */
#text-button:hover {
    color: #000; /* Change text color on hover */
    background-color: #ffffff; /* Highlight the button on hover */
    box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.2); /* Add a subtle shadow */
}

/* Active effect (when clicking) */
#text-button:active {
    transform: scale(0.98); /* Slightly scale down on click */
    box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.2); /* Reduce shadow */
}

.reset-button-container {
    position: relative; /* Stays at the bottom of the sidebar */
    margin-top: auto; /* Push it to the bottom */
    padding-top: 50px; /* Optional: Add some spacing above */
}

.reset-button {
    position: absolute; /* Place the button absolutely inside its parent */
    right: 0px; /* Align to the left side */
    width: 120px; /* Set a fixed width of 120px */
    bottom: 0%; /* Position it at the bottom with a gap of 20px */
}

.slider-container {
    margin-top: 8px; /* Slightly reduced margin */
}

.slider {
    margin-bottom: 12px; /* Reduced margin for compact look */
    display: flex; /* Use flexbox for alignment */
    align-items: center; /* Vertically center the switch and label */
}

.slider label {
    margin-left: 6px; /* Reduced spacing between switch and label */
    font-weight: normal; /* Less bold font for a subtler look */
    font-size: 14px; /* Smaller font size */
}

/* Slider switch styling */
.switch {
    position: relative;
    display: inline-block;
    width: 28px; /* Smaller width */
    height: 16px; /* Smaller height */
}

.switch input {
    opacity: 0;
    width: 0;
    height: 0;
}

.slider-round {
    position: absolute;
    cursor: pointer;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: #ccc;
    transition: .3s; /* Slightly faster transition */
    border-radius: 16px; /* Adjusted to match smaller height */
}

.slider-round:before {
    position: absolute;
    content: "";
    height: 10px; /* Smaller toggle */
    width: 10px; /* Smaller toggle */
    left: 3px;
    bottom: 3px;
    background-color: white;
    transition: .3s; /* Faster transition */
    border-radius: 50%;
}

input:checked + .slider-round {
    background-color: #2196F3;
}

input:checked + .slider-round:before {
    transform: translateX(12px); /* Adjust for smaller size */
}

.filter-container {
    display: flex;
    flex-direction: column;
    align-items: flex-start; 
    margin: 10px 0; /* Adds spacing between elements */
}

.filter-label {
    display: inline-block;
    margin-right: 10px;
    font-size: 14px;
    font-weight: bold;
}

.filter {
    width: 90%; /* Adjust to your needs */
    margin: 0 10px; /* Add spacing between slider and labels */
}

.filter-labels {
    display: flex;
    justify-content: space-between;
    width: 98%; /* Matches filter width */
    margin-top: 5px; /* Adds space between filter and labels */
    font-size: 12px;
    color: gray;
}

/* Animation for sliding up */
.slide-up-enter-active,
.slide-up-leave-active {
    transition: all 0.3s ease;
}

.slide-up-enter-from,
.slide-up-leave-to {
    transform: translateY(100%);
    opacity: 0;
}

.route-table-container {
    max-height: 62vh;
    overflow-y: auto;
    overflow-x: hidden;
    margin-top: 1px;
    border: 1px solid #555;
    border-radius: 8px;
    background-color: #222;
}
/* Base table styling */
.route-table {
    width: 100%;
    table-layout: fixed;
    border-collapse: collapse;
    background-color: #222; /* Dark background for table */
}

.route-table th,
.route-table td {
    border: 1px solid #444; /* Slightly darker for better contrast */
    padding: 6px; /* Reduced padding for compact look */
    text-align: left;
    font-size: 12px; /* Smaller font size for table content */
    word-wrap: break-word; /* Ensure text wraps within cells */
    overflow: hidden; /* Hide overflowing text */
    text-overflow: ellipsis; /* Add ellipsis for long text */
}

.route-table th:hover {
    background-color: #555; /* Change to your desired color */
    cursor: pointer;
}

.route-table tr:nth-child(even) {
    background-color: #333; /* Subtle contrast for even rows */
}

.route-table tr:hover {
    background-color: #444; /* Highlight on hover */
    color: #fff; /* Ensure text is readable on hover */
}

/* Scrollbar styling */
.route-table-container::-webkit-scrollbar {
    width: 8px; /* Adjust width as needed */
}

.route-table-container::-webkit-scrollbar-thumb {
    background: #555; /* Darker thumb for scrollbar */
    border-radius: 4px; /* Rounded corners for scrollbar */
}

.route-table-container::-webkit-scrollbar-thumb:hover {
    background: #777; /* Slightly lighter on hover */
}

.route-table-container::-webkit-scrollbar-track {
    background: #222; /* Background for the scrollbar track */
}

.search-input {
    width: 100%;
    padding: 8px;
    margin-bottom: 10px;
    border-radius: 4px;
    border: 1px solid #555; /* Darker border to match the theme */
    font-size: 14px;
    outline: none;
    background-color: #333; /* Darker background to match table */
    color: #ffffff; /* White text to contrast against dark background */
    transition: border-color 0.3s, box-shadow 0.3s; /* Smooth transitions for better visual experience */
}

.search-input::placeholder {
    color: #aaa; /* Lighter gray for the placeholder to make it distinct */
    opacity: 0.8;
}

.search-input:focus {
    border-color: #00bfff; /* Light blue border color when focused */
    box-shadow: 0 0 8px rgba(0, 191, 255, 0.4); /* Add subtle glow for focus */
}

.attribution-text {
    position: relative; /* Stays at the bottom of the sidebar */
    margin-top: auto; /* Push it to the bottom */
    padding-top: 10px; /* Optional: Add some spacing above */
    font-size: 12px; /* Adjust the font size */
    color: #b5b5b5; /* Light grey text to contrast against sidebar background */
    text-align: right; /* Align the text to the right */
}

.attribution-text:hover {
    color: #ffffff;
    cursor: pointer;
}

</style>
