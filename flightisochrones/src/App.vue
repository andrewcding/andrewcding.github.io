<script>

// Import other components
import Map from './components/Map.vue';
import Sidebar from './components/Sidebar.vue';
import AttributionModal from './components/AttributionModal.vue';

// Import .css file for Mapbox styling
import 'mapbox-gl/dist/mapbox-gl.css';

export default {
  components: {
    Map,
    Sidebar,
    AttributionModal,
  },
  data: () => ({
    // Intialize all variables
    headerText: 'Flight Isochrones ✈', // Default Header
    selectedAirportCode: '',
    selectedAirportName: '',
    sidebarVisible: true, // Sidebar visibility state
    selectedAirport: false, // Airport selection state
    showTable: false, // Table opened state
    filterDuration: 20, // Default filter values
    filterFrequency: 0,
    routes: null,
    showAttributionModal: false,
    showRouteLegend: false,
  }),
  methods: {
    // Reset variables when map is reset
    resetMap() {
      this.selectedAirport = false; // Reset selected airport on reset map
      this.headerText = 'Flight Isochrones ✈';
      this.selectedAirportCode = '';
      this.selectedAirportName = '';
      this.$refs.mapComponent.resetMapInternal();
      this.showRouteLegend = false;
    },

    // Toggle sidebar visibility
    toggleSidebar() {
      this.sidebarVisible = !this.sidebarVisible;
      
      // Shift map over when sidebar is opened / closed to ensure it is always in the middle of the map
      const map = this.$refs.mapComponent.map;
      
      if (map) {
        
        let padding;
        
        // Decide the padding based on sidebar and table state
        if (this.sidebarVisible && this.showTable) {
          padding = { left: 500 }; // Table open
        } else if (this.sidebarVisible) {
          padding = { left: 300 }; // Only sidebar open
        } else {
          padding = { left: 0 }; // Sidebar closed
        }
        
        // Animate globe movement
        map.easeTo({
          padding: padding,
          duration: 600 
        });
      }
    },

    // Change header for when airport is selected
    handleAirportSelection({ selected, airportCode, airportName }) {

        this.selectedAirport = selected;
        this.selectedAirportCode = airportCode;
        this.selectedAirportName = airportName;

        if (this.selectedAirportName && this.selectedAirportCode) {
            this.headerText = `${this.selectedAirportName} (${this.selectedAirportCode}) ✈`;
        } else {
            this.headerText = 'Flight Isochrones ✈';
        }
    },

    
    handleShowTableUpdate(showTable) {
      this.showTable = showTable;
    },

    // Reset sidebar filter values when map is reset
    resetSidebarFilter() {
      this.$refs.sidebarComponent.resetSlider(); // Call the resetSlider method in Sidebar.vue
    },
    // Pass arguments from Sidebar to Map when filters are activated
    onFilterRoutes(duration, frequency) {
      this.filterDuration = duration;
      this.filterFrequency = frequency;
      this.$refs.mapComponent.filterRoutes(duration, frequency);
    },

    // Animate routes in Map when animate button on Sidebar is clicked
    onAnimateRoutes() {
      // Invoke animateRoutes in Map component
      this.$refs.mapComponent.animateRoutes();
    },

    // Pass route data to table from Map to Sidebar
    handleRoutesLoaded(routes) {
      this.routes = routes;
    },

    // Pass route symbology toggle value from sidebar to activate legend + other details
    handleToggleRouteLegend(value) {
            this.showRouteLegend = value;
        },
  },
};
</script>


<template>
  <div id="layout">
    <!-- Button for opening and closing the sidebar -->
    <div id="toggle-sidebar" @click="toggleSidebar">
      {{ sidebarVisible ? "<<" : ">>" }}
    </div>
    <Map
    id="map"
    ref="mapComponent"
    :showRouteLegend="showRouteLegend"
    @select-airport="handleAirportSelection"  
    @reset-filter="resetSidebarFilter"
    @routes-loaded="handleRoutesLoaded"
    />
    <Sidebar
    ref="sidebarComponent"
    :visible="sidebarVisible"
    :airportSelected="selectedAirport"
    :routes="routes"
    :headerText="headerText"
    @filter-routes="onFilterRoutes"
    @toggle-route-legend="handleToggleRouteLegend"
    @trigger-animation="onAnimateRoutes"
    @reset-map="resetMap"
    @update-show-table="handleShowTableUpdate"
    @show-attribution="showAttributionModal = true"
    />
    <AttributionModal 
    :visible="showAttributionModal"
    @close="showAttributionModal = false" />
  </div>
</template>

<style>
#layout {
  flex: 1;
  display: flex;
  position: relative;
  overflow-y: hidden;
  height: 100vh; /* Ensure layout spans full height */
}

#toggle-sidebar {
  position: fixed;
  bottom: 15px;
  left: 10px;
  z-index: 2;
  cursor: pointer;
  color: #ffffff; /* White text */
  font-size: 20px;
  font-weight: bold;
  user-select: none; /* Prevent text selection */
  transition: color 0.3s; /* Smooth color transition */
}

#toggle-sidebar:hover {
  color: #a0a0a0; /* Gray color on hover */
}

#toggle-button {
  position: fixed;
  bottom: 10px;
  left: 10px;
  z-index: 2;
  padding: 8px 12px;
  cursor: pointer;
}

#map {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}
</style>
