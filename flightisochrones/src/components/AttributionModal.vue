<template>
  <div v-if="visible" class="modal-overlay">
    <div class="modal-content">
      <div class="modal-header">
        <h2>Data Sources and Attribution</h2>
        <button class="close-button" @click="closeModal">✖</button>
      </div>
      <div class="modal-body">
        <h3>Data Sources 🌐</h3>
        Flight Durations from <a href="https://www.flightsfrom.com/" target="_blank"><u>https://www.flightsfrom.com/</u></a>
        <br>
        Airport Data and Locations from <a href="https://openflights.org/data/" target="_blank"><u>https://openflights.org/data/</u></a>
        <br>
        Wind Data from <a href="https://www.ncei.noaa.gov/products/weather-climate-models/global-forecast" target="_blank"><u>NOAA</u></a>
        <br>
        <br>
        <h3>Libraries 📚</h3>
        <p>
            <a href="https://docs.mapbox.com/mapbox-gl-js/" target="_blank"><u>Mapbox GL JS</u></a> was used as the mapping library.
        </p>
        <p>
            <a href="https://turfjs.org/" target="_blank"><u>Turf.js</u></a> was used to calculate spatial distances for the animation.
        </p>
        <br>
        <h3>Methodology 🔬</h3>
        <p>The flight data was preprocessed in ArcGIS and in Python.</p>
        <p>The wind data was processed by Mapbox and made available as a raster array.</p>
        <br>
        <h3>Notes 📝</h3>
        <li>Some newer airports such as BER may be excluded from the data
          <br>as they are not in the OpenFlights airport dataset.</li>
        <li>Flights marked as having 0 daily flights indicate subweekly routes</li>
        <li>
          Flights marked with missing daily flights indicate former flight routes.
        </li>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AttributionModal',
  props: {
    visible: {
      type: Boolean,
      required: true,
    },
  },
  methods: {
    // Close the attribution window
    closeModal() {
      this.$emit('close');
    },
  },
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content{
  background: rgb(35 55 75 / 90%);
  padding: 20px;
  width: 80%;
  height: 80%;
  border-radius: 8px;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);
  overflow-y: auto;
  font-family: monospace;
  text-align: center;
}

.modal-content::-webkit-scrollbar {
    width: 8px; /* Adjust width as needed */
}

.modal-content::-webkit-scrollbar-thumb {
    background: rgb(59, 74, 92); /* Darker thumb for scrollbar */
    border-radius: 4px; /* Rounded corners for scrollbar */
}

.modal-content::-webkit-scrollbar-thumb:hover {
    background: rgb(95, 115, 135); /* Slightly lighter on hover */
}

.modal-content::-webkit-scrollbar-track {
    background: rgb(35 55 75 / 90%); /* Background for the scrollbar track */
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  text-align: center;
  color: white;
}

.close-button {
  background: none;
  border: none;
  color: white;
  font-size: 1.5rem;
  cursor: pointer;
}

.modal-body {
  margin-top: 20px;
  color: white;
  
}
.modal-body ul {
  list-style-type: none;
  padding: 0;
  line-height: 1.8;
  text-align: center;
}

.modal-body ul li {
  text-align: left;
  margin-bottom: 10px;
  text-align: center;
}
</style>
