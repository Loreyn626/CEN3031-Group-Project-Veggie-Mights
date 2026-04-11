<script setup></script>

<template>
  <div id="div-top">
    <h1>World Map: Cost of a Healthy Diet</h1>
    <ul id="dataSelectionBar">
      <li id="Home">Home</li>
      <li id="Daily Cost">Daily Cost</li>
      <li id="Annual Cost">Annual Cost</li>
      <li id="Vegetables Cost">Vegetables Cost</li>
      <li id="Fruits Cost">Fruits Cost</li>
      <li id="Fruit & Vegetables Total Cost">Fruit & Vegetables Total Cost</li>
    </ul>
  </div>
  <div style="height: 700px;" id="div-1" ></div>
  <div id="div-bottom">
    <h4>Additional Context</h4>
    <p id="div-bottom-text">Write data here!</p>
  </div>
</template>

<style scoped>
  /* ========== TITLE & NAVIGATION BUTTONS | div-top ========== */
  #div-top {
    font-family: Helvetica;
  }

  #div-top h1 {
    margin-left: 40px; /* I think this is a good number to align with buttons */
  }
  #dataSelectionBar {
    list-style-type: none;
    display: flex;
    gap: 15px; /* spacing between ul elements */
  }

  #dataSelectionBar li {
    background-color: hsl(200, 100%, 50%);
    color: white;
    font-weight: bold;
    padding: 15px;
    border-radius: 8px; /* rounds corners */
  }

  #dataSelectionBar li:hover {
    background-color: hsl(200, 100%, 45%);
    cursor: pointer;
  }

  /* ========== BOTTOM TEXT BOX | div-bottom ========== */
  #div-bottom {
    font-family: Helvetica;
    border: solid;
    border-width: 5px;
    border-color: hsl(200, 100%, 50%);
    border-radius: 4px;
  }

  #div-bottom h4 {
    margin-top: 0px;
    padding: 5px;
    background-color: hsl(200, 100%, 50%);
    color: white;
  }

  #data {
    margin-left: 5px;
  }
</style>

<script>
  import Plotly from 'plotly.js-dist-min'

  window.addEventListener("DOMContentLoaded", async () => {
    const response = await fetch('/api/map/home');
    const map = await response.json();

    /* CREATES INITIAL MAP AND LOADS TO PAGE */
    const mapPlot = await Plotly.newPlot("div-1", map.data, map.layout)
    registerClickEvent(mapPlot);

    /* CHANGE BETWEEN MAPS */
    let homeButton = document.getElementById('Home')
    homeButton.addEventListener('click', async () => {
      const response = await fetch('/api/map/home');
      const map = await response.json();
      const mapPlot = await Plotly.newPlot("div-1", map.data, map.layout)
      registerClickEvent(mapPlot);
    })

    let dailyButton = document.getElementById('Daily Cost')
    dailyButton.addEventListener('click', async () => {
      const response = await fetch('/api/map/daily');
      const map = await response.json();
      const mapPlot = await Plotly.newPlot("div-1", map.data, map.layout)
      registerClickEvent(mapPlot);
    })

    let annualButton = document.getElementById('Annual Cost')
    annualButton.addEventListener('click', async () => {
      const response = await fetch('/api/map/annual');
      const map = await response.json();
      const mapPlot = await Plotly.newPlot("div-1", map.data, map.layout)
      registerClickEvent(mapPlot);
    })

    let vegetablesButton = document.getElementById('Vegetables Cost')
    vegetablesButton.addEventListener('click', async () => {
      const response = await fetch('/api/map/vegetables');
      const map = await response.json();
      const mapPlot = await Plotly.newPlot("div-1", map.data, map.layout)
      registerClickEvent(mapPlot);
    })

    let fruitsButton = document.getElementById('Fruits Cost')
    fruitsButton.addEventListener('click', async () => {
      const response = await fetch('/api/map/fruits');
      const map = await response.json();
      const mapPlot = await Plotly.newPlot("div-1", map.data, map.layout)
      registerClickEvent(mapPlot);
    })

    let fruitVegTotalButton = document.getElementById('Fruit & Vegetables Total Cost')
    fruitVegTotalButton.addEventListener('click', async () => {
      const response = await fetch('/api/map/fruit_veg_total');
      const map = await response.json();
      const mapPlot = await Plotly.newPlot("div-1", map.data, map.layout)
      registerClickEvent(mapPlot);
    })

    /* REGISTER CLICK EVENT  */
    /* https://plotly.com/javascript/plotlyjs-events/#using-plotlyjs-events */
    function registerClickEvent(mapPlot) {
        mapPlot.removeAllListeners('plotly_click') /* Prevent duplicate click events */
        mapPlot.on('plotly_click', function(data){
          for(var i=0; i < data.points.length; i++){
            let country = data.points[i].location
            console.log(country) /* for testing */
            document.getElementById('div-bottom-text').textContent = country /* can expand to include more here */
          }
        }
      )
    }
  })
</script>