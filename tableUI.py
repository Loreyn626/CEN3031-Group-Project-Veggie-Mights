import plotly.graph_objects as go
from data.classes import *
from data.parsing import countries

# Used to get country info for mapAPI to be sent to the frontend
def country_info(country_name):
    for country in countries:
        if country.name == country_name:
            return country
    return None
