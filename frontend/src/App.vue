<template>
  <div>
    
    <!-- Whenever a letter is typed into the search bar, it will call the highlightCountry function -->
    <input 
      id="search"
      type="search" 
      @input="highlightCountry" 
      placeholder="Search for a country.."
    >
    <div style="height: 700px;" id="div-1"></div>
  </div>
</template>

<style scoped></style>

<script setup>
  import Plotly from "plotly.js-dist-min";

  let chartDiv = null;
  let map = null;

  window.addEventListener("DOMContentLoaded", async () => {
    const response = await fetch("/api/map");
    map = await response.json();
    chartDiv = document.getElementById("div-1");
    await Plotly.newPlot(chartDiv, map.data, map.layout);
    // tracks whether a change has been made to the slider
    chartDiv.on('plotly_sliderchange', (data) => {
      const searchInput = document.getElementById("search");
      if (searchInput && searchInput.value) {
        // need to set a timeout to make sure the trace visibilities were updated based on slider changes before calling highlightCountry and checking that the country is visible
        setTimeout(() => {
          highlightCountry({ target: searchInput });
        }, 100);
      }
    });
  })

  function highlightCountry(event) {
    const searchTerm = event.target.value;
    
    // if the search bar is empty, clear the highlighting
    if (!searchTerm) {
      for (let i = 0; i < chartDiv.data.length; i++) {
        // sets lines to defaults again
        Plotly.restyle(chartDiv, {
          "marker.line.width": 1,
          "marker.line.color": "#444"
        }, [i]);
      }
      return;
    }
    
    // Find which map trace has locations
    for (let i = 0; i < chartDiv.data.length; i++) {
      let trace = chartDiv.data[i];
      
      // because scattergeo doesn't have a .locations value
      if (trace.type == "choropleth" && trace.visible !== false) {
        // update array w/ with which country should get the blue highlight
        const lineWidths = [];
        const lineColors = [];
        
        for (let i = 0; i < trace.locations.length; i++) {
          const country = trace.locations[i];
          const isMatch = country.toLowerCase().includes(searchTerm.toLowerCase());
          lineWidths.push(isMatch ? 3 : 1);
          lineColors.push(isMatch ? "blue" : "#444");
        }
        
        // restyle for setting trace styling
        Plotly.restyle(chartDiv, {
          "marker.line.width": [lineWidths],
          "marker.line.color": [lineColors]
        }, [i]);
      }
    }
  }
</script>