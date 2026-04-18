<script setup></script>

<template>
  <div>
    <h1 id="countrynotif" style="display:none;">Im Testing???</h1>

    <!-- Reference: https://coreui.io/answers/how-to-build-a-table-in-vue/ -->
    <!-- Reference: https://stackoverflow.com/questions/10610963/how-to-position-a-table-html -->
    <table id="myTable">
      <thead>
        <tr>
          <th>Country</th>
          <th>Annual Costs</th>
          <th>Daily Costs</th>
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

    <div style="height: 700px;" id="div-1" ></div>
  </div>
</template>

<style>
#myTable {
  position: absolute;
  margin-top:350px;
  z-index: 10;
  border: 1px solid;
  max-width: 350px;
  border-collapse: collapse;

}
th,td {
  padding: 5px;
  border: 1px solid;
}


</style>

<script>
  import Plotly from 'plotly.js-dist-min'

  window.addEventListener("DOMContentLoaded", async () => {
    const response = await fetch('/api/map');
    const map = await response.json();
    Plotly.newPlot("div-1", map.data, map.layout)

    const myPlot = document.getElementById("div-1")

    myPlot.on('plotly_click', async function(data) {
      const country = data.points[0].location;
      const response = await fetch(`/api/country/${encodeURIComponent(country)}`); //encode needed if data has spaces
      const _country = await response.json();
      var table = document.getElementById("myTable");
      var numCountries = document.getElementById("myTable").rows.length;
      var added = false;
      

      if (numCountries == 1) {
        var row = table.insertRow(1);
        var cell1 = row.insertCell(0);
        var cell2 = row.insertCell(1);
        var cell3 = row.insertCell(2);

        cell1.innerHTML = _country.name;
        cell2.innerHTML = _country.averageAnnualCost;
        cell3.innerHTML = _country.dailyCostPPP;
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

          cell1.innerHTML = _country.name;
          cell2.innerHTML = _country.averageAnnualCost;
          cell3.innerHTML = _country.dailyCostPPP;
        }
        
      } 
      
    });
  })

  function resetTable() {
    var numCountries = document.getElementById("myTable").rows.length;

        if (numCountries > 0) {
          for (let i = numCountries - 2; i > 0; i--) {
            document.getElementById("myTable").deleteRow(i);
          }
        }
      }

  window.resetTable = resetTable;
</script>
