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

    <div id="topText">
      <h4>Description:</h4>
      <p id="details"></p>
    </div>

    <!-- Whenever a letter is typed into the search bar, it will call the highlightCountry function -->
    <input
      id="search"
      type="search"
      @input="highlightCountry"
      placeholder="Search for a country.."
    >
  </div>

  <!-- Country Comparison Table -->
  <div id="tableContainer">
    <!-- Reference: https://coreui.io/answers/how-to-build-a-table-in-vue/ -->
    <!-- Reference: https://stackoverflow.com/questions/10610963/how-to-position-a-table-html -->
    <table id="myTable">
      <thead>
        <tr>
          <th>Country</th>
          <th>Average Daily Costs</th>
          <th>Average Annual Costs</th>
          <th>2021 Daily Vegetables Costs</th>
          <th>2021 Daily Fruits Costs</th>
        </tr>
      </thead>
      <tbody>

      </tbody>
      <tfoot>
        <tr>
          <td>
            <button type = "button" class = "resetButton" onclick="resetTable()">Reset Table</button>
          </td>
        </tr>
      </tfoot>

    </table>
  </div>

  <div style="height: 700px;" id="div-1"></div> <!-- This is where MAP lives -->

  <div id="div-bottom">
    <h4>Additional Context</h4>
    <p id="div-bottom-text">Write data here!</p>
  </div>
</template>

<style>
  /* ========== TITLE & NAVIGATION BUTTONS | div-top ========== */
  #div-top {
    font-family: Helvetica;
  }

  #topText, #search, #div-top h1 {
    margin-left: 40px; /* I think this is a good number to align with buttons */
  }

  #topText h4 {
    margin-top: 0px;
    margin-right: 10px;
    border-radius: 4px;
    padding: 5px;
    background-color: gray;
    color: white;
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

  #dataSelectionBar li.active {
    background-color: hsl(360, 100%, 50%);
    cursor: default;
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

  #tableContainer {
    height: 170px;
  }

  #myTable {
    margin-top: -20px;
    margin-left: 230px;
    z-index: 10;
    border: 1px solid gray;
    border-collapse: collapse;

  }

  #myTable thead {
    background-color: gray;
    color: white;
    font-family: Helvetica;

  }

  #myTable th,td {
    padding-left: 10px;
    padding-right: 10px;
    border: 1px solid gray;
    font-family: Helvetica;
  }
  
</style>

<script setup>
  import Plotly from 'plotly.js-dist-min'
  let map = null;
  let chartDiv = null;

  /* Descriptions Map*/
  const mapDescriptions = {
    "Home" : `The map displays the general costs of a healthy diet per country scored by low, medium, and high cost.
    The averages for daily cost of diet and annual cost of diet per country was calculated from data that spanned between 2017-2024.
    Cost thresholds are listed below. The Cost Category side legend can be operated to filter cost categories.
    <ul>
      <li>Low Cost: <$2.50/day</li>
      <li>Medium Cost: $2.50-$3.49/day</li>
      <li>High Cost: >$3.50/day</li>
    </ul>
    <br>`,
    "Daily Cost" : `Daily cost of healthy diet per country by year.
    Slide to across the years to view changes.`,
    "Annual Cost" : `Annual cost of healthy diet per country by year.
    Slide to across the years to view changes.`,
    "Vegetables Cost" : `Daily cost of vegetables per country.
    Data was collected only for the year 2021.`,
    "Fruits Cost" : `Daily cost of fruits per country.
    Data was collected only for the year 2021.`,
    "Fruit & Vegetables Total Cost" : `Total daily cost of fruits and vegetables per country.
    Data was collected only for the year 2021.`
  }

  window.addEventListener("DOMContentLoaded", async () => {
    const response = await fetch('/api/map/home');
    const map = await response.json();

    /* CREATES INITIAL MAP AND LOADS TO PAGE */
    chartDiv = document.getElementById("div-1");
    const mapPlot = await Plotly.newPlot(chartDiv, map.data, map.layout);
    registerClickEvent(mapPlot);

    // tracks whether a change has been made to the slider
    chartDiv.on('plotly_sliderchange', (data) => {
      const searchInput = document.getElementById("search");
      if (searchInput && searchInput.value) {
        // need to set a timeout to make sure the trace visibilities were updated based on slider changes before calling highlightCountry and checking that the country is visible
        setTimeout(() => {
          highlightCountry({ target: searchInput });
        }, 100);
      }
      updateCountryComparison()
    });

    /* CHANGE BETWEEN MAPS */
    let homeButton = document.getElementById('Home')
    homeButton.addEventListener('click', async () => {
      const response = await fetch('/api/map/home');
      const map = await response.json();
      const mapPlot = await Plotly.newPlot("div-1", map.data, map.layout)
      registerClickEvent(mapPlot);
      updateCountryComparison(mapPlot)
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
    function registerClickEvent(chartDiv) {
        chartDiv.removeAllListeners('plotly_click') /* Prevent duplicate click events */
        chartDiv.on('plotly_click', function(data){
          for(var i=0; i < data.points.length; i++){
            let country = data.points[i].location
            // console.log(country) /* for testing */
            document.getElementById('div-bottom-text').textContent = country /* can expand to include more here */
            updateCountryComparison(country);
          }
        }
      )
    }

    async function updateCountryComparison(country) {
      const response = await fetch(`/api/country/${encodeURIComponent(country)}`); //encode needed if data has spaces
      const _country = await response.json();
      var table = document.getElementById("myTable");
      var numCountries = document.getElementById("myTable").rows.length;
      var added = false;

      // Country comparison table
      if (numCountries == 1) {
        var row = table.insertRow(1);
        var cell1 = row.insertCell(0);
        var cell2 = row.insertCell(1);
        var cell3 = row.insertCell(2);
        var cell4 = row.insertCell(3);
        var cell5 = row.insertCell(4);

        cell1.innerHTML = _country.name;
        cell2.innerHTML = "$" + _country.dailyCostPPP;
        cell3.innerHTML = "$" + _country.averageAnnualCost;
        cell4.innerHTML = "$" + _country.averageVegetableCost;
        cell5.innerHTML = "$" + _country.averageFruitCost;
      }

      else if (numCountries < 5) {

        for (let i = 0; i < numCountries; i++) {
          if (document.getElementById("myTable").rows[i].cells[0].innerText == _country.name) {
            added = true;
            break;
          }
        }
        if (added == false) {

          var row = table.insertRow(1);
          var cell1 = row.insertCell(0);
          var cell2 = row.insertCell(1);
          var cell3 = row.insertCell(2);
          var cell4 = row.insertCell(3);
          var cell5 = row.insertCell(4);

          cell1.innerHTML = _country.name;
          cell2.innerHTML = "$" + _country.dailyCostPPP;
          cell3.innerHTML = "$" + _country.averageAnnualCost;
          cell4.innerHTML = "$" + _country.averageVegetableCost;
          cell5.innerHTML = "$" + _country.averageFruitCost;
        }

      }

    };

    function resetTable() {
      var numCountries = document.getElementById("myTable").rows.length;

      if (numCountries > 0) {
        for (let i = numCountries - 2; i > 0; i--) {
          document.getElementById("myTable").deleteRow(i);
        }
      }
    }

    window.resetTable = resetTable;

  /* Tracks active page & updates description */
  document.getElementById('Home').classList.add('active'); // sets Home to active on start
  document.getElementById('details').innerHTML = mapDescriptions['Home'];
  const tabList = document.querySelectorAll('#dataSelectionBar li')
  tabList.forEach(tab => {
    tab.addEventListener('click', () => {
      document.querySelector('.active')?.classList.remove('active');
      tab.classList.add('active');
      document.getElementById('details').innerHTML = mapDescriptions[tab.id];
      })
    })
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