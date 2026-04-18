from flask import Flask, jsonify
from mapUI import *
from tableUI import *
import plotly

app = Flask(__name__)

@app.route('/api/map', methods=['GET'])
def get_map():
   # https://stackoverflow.com/questions/72930513/how-to-plot-plotly-chart-on-react-from-json-response-from-flask-api
   # using plotly function to send map in json format
   return plotly.io.to_json(plotMap())

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