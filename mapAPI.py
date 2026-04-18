from flask import Flask, jsonify
from mapUI import *
from tableUI import *
import plotly

app = Flask(__name__)

@app.route('/api/map/home', methods=['GET'])
def get_average_map():
    return plotly.io.to_json(plotAverageMap())


@app.route('/api/map/daily', methods=['GET'])
def get_daily_map():
    # https://stackoverflow.com/questions/72930513/how-to-plot-plotly-chart-on-react-from-json-response-from-flask-api
    # using plotly function to send map in json format
    return plotly.io.to_json(plotYearlyMap('DC'))


@app.route('/api/map/annual', methods=['GET'])
def get_annual_map():
    return plotly.io.to_json(plotYearlyMap('AC'))


# ====== 2021-ONLY DATA METRICS ======
@app.route('/api/map/vegetables', methods=['GET'])
def get_vegetables_map():
    return plotly.io.to_json(plotYearMap('VC'))


@app.route('/api/map/fruits', methods=['GET'])
def get_fruits_map():
    return plotly.io.to_json(plotYearMap('FC'))


@app.route('/api/map/fruit_veg_total', methods=['GET'])
def get_fruit_veg_total_map():
    return plotly.io.to_json(plotYearMap('FVC'))


# https://flask.palletsprojects.com/en/stable/patterns/javascript/
# use a dictionary to return a JSON object with the country info
@app.route('/api/country/<country_name>', methods=['GET'])
def get_country_info(country_name):
   country = country_info(country_name) # function from tableUI.py
   return {
      "name":country.name,
      "averageAnnualCost":country.averageAnnualCost,
      "dailyCostPPP":country.averagePPP
   }

if __name__ == '__main__':
    app.run(port=5000)