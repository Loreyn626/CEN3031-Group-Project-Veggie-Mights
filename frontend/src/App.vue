<script setup></script>

<template>
  <div style="height: 700px;" id="div-1" ></div>
</template>

<style scoped></style>

<script>
  import Plotly from 'plotly.js-dist-min'

  window.addEventListener("DOMContentLoaded", async () => {
    const response = await fetch('/api/map');
    const map = await response.json();
    Plotly.newPlot("div-1", map.data, map.layout)
  })
</script>
