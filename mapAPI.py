from flask import Flask, jsonify
from mapUI import *
import plotly

app = Flask(__name__)

@app.route('/api/map', methods=['GET'])
def get_map():
   # https://stackoverflow.com/questions/72930513/how-to-plot-plotly-chart-on-react-from-json-response-from-flask-api
   # using plotly function to send map in json format
   return plotly.io.to_json(plotMap())

if __name__ == '__main__':
   app.run(port=5000)