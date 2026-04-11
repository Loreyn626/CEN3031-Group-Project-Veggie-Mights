import plotly.graph_objects as go
from data.classes import *
from data.parsing import countries
import pandas as pd

country_names = []  # For locations

# Lists based on the data columns in the spreadsheet
all_annual_costs = [[], []]  # Daily annual healthy diet and calculated total costs in USD
all_veg_fruit_costs = [[], [], []]  # Vegetable costs, fruit costs, vegetable + fruit total costs in USD

# Dataframe for px: dict with key (specified data) : value (the actual value for country)
# https://codefinity.com/courses/v2/fb11bab5-fb60-4952-b6ba-f2a6635706b1/f9a2535c-b02e-45d1-9cb2-4963aa0e64d4/a5c4294e-6651-4f30-867b-5079330a0f9e
country_averages = {'Country': [],
                    'Cost Category': [],
                    'Average Daily Cost': [],
                    'Average Annual Cost': [],
                    'Average Vegetables Cost': [],
                    'Average Fruits Cost': [],
                    'Average Total Food Cost': [],
                    }

for country in countries:
    country_names.append(country.name)

    # Costs need to be converted to floats, otherwise the data won't properly display
    # Initialize empty "country_cost" list to prevent "index out of range" errors when adding data

    country_costs = []
    for cost in country.costPPPs:
        country_costs.append(float(cost))
    all_annual_costs[0].append(country_costs)

    country_costs = []
    for cost in country.annualCosts:
        country_costs.append(float(cost))
    all_annual_costs[1].append(country_costs)

    # Vegetable costs (index 0), fruit costs (index 1), vegetable + fruit total costs (index 2)
    country_costs = []
    for cost in country.vegetablesPPPs:
        if cost != "":
            country_costs.append(float(cost))

    # Add none outside cost iteration so all lists have at least one value (one year only)
    if len(country_costs) == 0:
        country_costs.append(None)

    all_veg_fruit_costs[0].append(country_costs)

    country_costs = []
    for cost in country.fruitsPPPs:
        if cost != "":
            country_costs.append(float(cost))

    # Add none outside cost iteration so all lists have at least one value (one year only)
    if len(country_costs) == 0:
        country_costs.append(None)

    all_veg_fruit_costs[1].append(country_costs)

    country_costs = []
    for cost in country.totalFoodCosts:
        if cost != "":
            country_costs.append(float(cost))

    # Add none outside cost iteration so all lists have at least one value (one year only)
    if len(country_costs) == 0:
        country_costs.append(None)

    all_veg_fruit_costs[2].append(country_costs)

    # Append each average data element into the key where it belongs (will be a list)
    country_averages['Country'].append(country.name)
    country_averages['Average Daily Cost'].append(f' ${country.averagePPP:.2f}')
    country_averages['Average Annual Cost'].append(f' ${country.averageAnnualCost:.2f}')

    # if/else to handle f' string format with exceptions for "N/A" values in vegetables and fruits
    if type(country.averageVegetablesPPP) != str and type(country.averageVegetablesPPP) != bool:
        country_averages['Average Vegetables Cost'].append(f' ${country.averageVegetablesPPP:.2f}')
    else:
        country_averages['Average Vegetables Cost'].append(country.averageVegetablesPPP)

    if type(country.averageFruitsPPP) != str and type(country.averageFruitsPPP) != bool:
        country_averages['Average Fruits Cost'].append(f' ${country.averageFruitsPPP:.2f}')
    else:
        country_averages['Average Fruits Cost'].append(country.averageFruitsPPP)

    country_averages['Average Total Food Cost'].append(country.averageTotalFoodCost)
    country_averages['Cost Category'].append(country.averageCostCategory)

# Use pandas library to make df for px
country_averages_df = pd.DataFrame(country_averages)  # We will pass this into px.choropleth

def plotAverageMap():
    # HOME MAP FOR AVERAGES OF ALL YEARS (2017 - 2024)
    import plotly.express as px  # https://plotly.com/python/choropleth-maps/#discrete-colors
    # Hover settings: https://plotly.com/python/hover-text-and-formatting/
    # Color settings (discrete only): https://plotly.com/python/discrete-color/#directly-mapping-colors-to-data-values
    # help(px.choropleth) # If you needed to get more info on parameters/arguments

    # DRAWS MAP
    fig = px.choropleth(country_averages_df,
                        locations='Country',
                        locationmode='country names',
                        color='Cost Category',
                        color_discrete_map={
                            'Low Cost': 'green',
                            'Medium Cost': 'orange',
                            'High Cost': 'red'
                        },
                        hover_name='Country',
                        hover_data={
                            'Country': False,
                            'Cost Category': False,
                            'Average Daily Cost': True,
                            'Average Annual Cost': True,
                            'Average Vegetables Cost': True,
                            'Average Fruits Cost': True
                        }
                        )

    # UPDATE UI
    fig.update_layout(
        title_text='Average Cost of a Healthy Diet by Country',
        geo=dict(
            showframe=True,
            showcoastlines=True,
            projection_type='equirectangular'
        ),
        annotations=[dict(
            y=0.0,
            xref='paper',
            yref='paper',
            text='Source: <a href="https://www.kaggle.com/datasets/ibrahimshahrukh/global-price-of-healthy-diet-dataset">\
               Kaggle Cost of Healthy Diet by Country (2017-2024)</a>',
            showarrow=False
        )],
        hoverlabel={}
    )

    return fig


def plotYearlyMap(data):
    cost_categories = ['Low', 'Medium', 'High']
    colors = ['green', 'orange', 'red']

    fig = go.Figure()  # Initialize graph object

    # ========== DAILY HEALTHY DIET OR ANNUAL COST ==========
    if data == 'DC':
        show = 0
    if data == 'AC':
        show = 1

    # For Choropleth z-value parameter
    all_z_values = []

    # Each year needs different z-values
    for i in range(8):  # 8 years: 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024
        year_z_values = []

        for costs in all_annual_costs[show]:
            # Add all country costs for that specific year into year_z_value
            if i < len(costs):
                cost = costs[i]
            else:
                cost = None

            # Add cost data to the specific year's list
            year_z_values.append(cost)

        # Add list of each country's annual cost for the year to a yearly list
        all_z_values.append(year_z_values)

    # Determine min and max for the specific year
    # Can't just use min() or max() on z_values because it doesn't work with "None" values
    valid_costs = []

    for year in all_z_values:
        for value in year:
            if value is not None:
                valid_costs.append(value)

    # zmin & zmax is the lowest and highest value of ALL costs over ALL years
    # This helps keep colorscale consistent between years and when we trace 8 times (1 trace per year)
    zmin = min(valid_costs)
    zmax = max(valid_costs)

    # go.Choropleth is where data is actually being inserted
    for i in range(8):
        fig.add_trace(go.Choropleth(
            # Show the most recent year upon initial map load
            visible=(i==7),
            # insert country names here as an array
            locations=country_names,
            locationmode='country names',
            # Display all annual costs for now before adding more info later
            z=all_z_values[i],
            # Color scaling, 0% of the way to max is green, 50% = orange, 100% = red
            colorscale=[[0.0, colors[0]], [0.5, colors[1]], [1.0, colors[2]]],
            showscale=True,
            # Show dollar signs too (to be consistent with average cost display)
            hovertemplate="<b>%{location}</b><br>$%{z:.2f}",
            # this contains some data being displayed
            name=str(i + 2017),
            zmin=zmin,
            zmax=zmax
        ))

    # go.Scattergeo function is only being used to incorporate figure labels for the colors
    # don't insert any data here
    for i in range(len(cost_categories)):
        fig.add_trace(go.Scattergeo(
            lat=[None],
            lon=[None],
            locationmode='country names',
            marker_color=colors[i],
            name=cost_categories[i],
            showlegend=True,
            hoverinfo='skip',
        ))

    # ============= SLIDER FUNCTIONALITY =============
    steps = []
    for i in range(8): # 8 different years
        # Only show one year at a time from one data metric, prevent overlap

        visible_list = []

        for j in range(8):
            if j == i:
                visible_list.append(True)
            else:
                visible_list.append(False)

        # Include the legend in all years
        visible_list.extend([True] * len(cost_categories))

        step = dict(
            method="update", # Updates map
            args=[{"visible": visible_list}],
            label=str(i + 2017)
        )
        steps.append(step)

    sliders = [dict(
        active=7, # Show the most recent year upon initial map load
        currentvalue={"prefix": "Year: "},
        steps=steps
    )]

    # ========== UPDATE LAYOUT/UI OPTIONS ==========
    fig.update_layout(
        title_text='Cost of Healthy Diet by Country',
        geo=dict(
            showframe=True,
            showcoastlines=True,
            projection_type='equirectangular'
        ),
        sliders=sliders,
        annotations=[dict(
            y=0.0,
            xref='paper',
            yref='paper',
            text='Source: <a href="https://www.kaggle.com/datasets/ibrahimshahrukh/global-price-of-healthy-diet-dataset">\
               Kaggle Cost of Healthy Diet by Country (2017-2024)</a>',
            showarrow=False
        )],
        legend=dict(
            x=0.89,
            itemclick=False,
            itemdoubleclick=False
        ),
    )

    return fig


# For 2021-only data metrics: Fruits, Vegetables, Fruit & Vegetables Total Costs
def plotYearMap(data):
    cost_categories = ['Low', 'Medium', 'High']
    colors = ['green', 'orange', 'red']

    fig = go.Figure()  # Initialize graph object

    if data == 'VC':
        show = 0
    if data == 'FC':
        show = 1
    if data == 'FVC':
        show = 2

    # Create merged list instead of each country having its own separate value list
    year_z_values = []
    for costs in all_veg_fruit_costs[show]:
        year_z_values.append(costs[0])

    # Determine min and max
    # Can't just use min() or max() because it doesn't work with "None" values
    valid_costs = []
    for cost in year_z_values:
        if cost is not None:
            valid_costs.append(cost)

    # zmin & zmax is the lowest and highest value of ALL costs
    zmin = min(valid_costs)
    zmax = max(valid_costs)

    # go.Choropleth is where data is actually being inserted
    fig.add_trace(go.Choropleth(
        # insert country names here as an array
        locations=country_names,
        locationmode='country names',
        # Display all annual costs for now before adding more info later
        z=year_z_values,
        # Color scaling, 0% of the way to max is green, 50% = orange, 100% = red
        colorscale=[[0.0, colors[0]], [0.5, colors[1]], [1.0, colors[2]]],
        showscale=True,
        # Show dollar signs too (to be consistent with average cost display)
        hovertemplate="<b>%{location}</b><br>$%{z:.2f}",
        # this contains some data being displayed
        name="2021", # 2021 only
        zmin=zmin,
        zmax=zmax
    ))

    # go.Scattergeo function is only being used to incorporate figure labels for the colors
    # don't insert any data here
    for i in range(len(cost_categories)):
        fig.add_trace(go.Scattergeo(
            lat=[None],
            lon=[None],
            locationmode='country names',
            marker_color=colors[i],
            name=cost_categories[i],
            showlegend=True,
            hoverinfo='skip',
        ))

    # ========== UPDATE LAYOUT/UI OPTIONS ==========
    fig.update_layout(
        title_text='Daily Cost of Food by Country (2021 only)',
        geo=dict(
            showframe=True,
            showcoastlines=True,
            projection_type='equirectangular'
        ),
        annotations=[dict(
            y=0.0,
            xref='paper',
            yref='paper',
            text='Source: <a href="https://www.kaggle.com/datasets/ibrahimshahrukh/global-price-of-healthy-diet-dataset">\
               Kaggle Cost of Healthy Diet by Country (2017-2024)</a>',
            showarrow=False
        )],
        legend=dict(
            x=0.89,
            itemclick=False,
            itemdoubleclick=False
        ),
    )

    return fig