import plotly.graph_objects as go
from data.classes import *
from data.parsing import countries

country_names = [] # For locations

# Lists based on the data columns in the spreadsheet
all_annual_costs = [[], []] # Daily annual healthy diet and calculated total costs in USD
all_veg_fruit_costs = [[], [], []] # Vegetable costs, fruit costs, vegetable + fruit total costs in USD

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
      if cost == "":
         country_costs.append(None)
      else:
         country_costs.append(float(cost))
   all_veg_fruit_costs[0].append(country_costs)

   country_costs = []
   for cost in country.fruitsPPPs:
      if cost == "":
         country_costs.append(None)
      else:
         country_costs.append(float(cost))
   all_veg_fruit_costs[1].append(country_costs)

   country_costs = []
   for cost in country.totalFoodCosts:
      if cost == "":
         country_costs.append(None)
      else:
         country_costs.append(float(cost))
   all_veg_fruit_costs[2].append(country_costs)

def plotMap():
   cost_categories = ['Low', 'Medium', 'High']
   colors = ['green', 'orange', 'red']

   fig = go.Figure() # Initialize graph object

   # ========= DAILY HEALTHY DIET & ANNUAL TOTAL COSTS + SLIDERS PER YEAR =========
   for metric_index, metric_data in enumerate(all_annual_costs):
      # For Choropleth z-value parameter
      all_z_values = []

      # Each year needs different z-values
      for i in range(8): # 8 years: 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024
         year_z_values = []

         # Add all costs for that specific year
         for country_index in range(len(country_names)):
            costs = metric_data[country_index] # Each country's multi-year list

            if i < len(costs):
               cost = costs[i]
            else:
               cost = None # Placeholder if missing data (doesn't show on map)

            # Add cost data to the specific year's list
            year_z_values.append(cost)

         # Add list of each country's annual cost for the year to a yearly list
         all_z_values.append(year_z_values)

      # Determine min and max for the specific year
      # Can't just use min() or max() on z_values because it doesn't work with "None" values
      yearly_costs = []

      for year in all_z_values:
         for value in year:
            if value is not None:
               yearly_costs.append(value)

      # zmin & zmax is the lowest and highest value of ALL costs over ALL years
      # This helps keep colorscale consistent between years and when we trace 8 times (1 trace per year)
      zmin = min(yearly_costs)
      zmax = max(yearly_costs)

      if metric_index == 0:
         metric_name = "Daily healthy diet costs"
      else:
         metric_name = "Calculated total annual costs"

      # go.Choropleth is where data is actually being inserted
      for i in range(8):
         fig.add_trace(go.Choropleth(
            # insert country names here as an array
            locations=country_names,
            locationmode='country names',
            # Display all annual costs for now before adding more info later
            z=all_z_values[i],
            # Color scaling, 0% of the way to max is green, 50% = orange, 100% = red
            colorscale=[[0.0, colors[0]],[0.5, colors[1]],[1.0, colors[2]]],
            showscale=True,
            # this contains some data being displayed
            name=metric_name+str(i + 2017),
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
         marker_color= colors[i],
         name=cost_categories[i],
         showlegend=True,
         hoverinfo='skip',
      ))

   # Slider functionality for UI, testing with values first before setting it up fully
   # For slider creation and labeling
   steps = []
   for i in range(8): # 8 different years
      # Only show one year at a time from one data metric, prevent overlap

      # ============= DAILY HEALTHY DIET COSTS =============
      visible_daily = []

      for j in range(8):
         if j == i:
            visible_daily.append(True)
         else:
            visible_daily.append(False)

      # Add slots for hiding annual total data
      for j in range(8):
         visible_daily.append(False)

      # Include the legend in all years
      visible_daily.extend([True] * len(cost_categories))

      # ============= CALCULATED TOTAL ANNUAL COSTS =============
      visible_annual = []

      for j in range(8):
         if j == i:
            visible_annual.append(True)
         else:
            visible_annual.append(False)

      # Add slots for hiding daily healthy diet costs
      for j in range(8):
         visible_annual.append(False)

      # Include the legend in all years
      visible_annual.extend([True] * len(cost_categories))

      # Update slider steps
      step = dict(
         method="update", # Updates map
         args=[{"visible": visible_daily}],
         label=str(i + 2017)
      )
      steps.append(step)

   sliders=[dict(
      active=0,
      currentvalue={"prefix": "Year: "},
      steps=steps
   )]

   # this can be used to adjust layout and maybe the UI for the data
   fig.update_layout(
      title_text='Cost of Healthy Diet by Country',
      geo=dict(
         showframe=True,
         showcoastlines=True,
         projection_type='equirectangular'
      ),
      sliders=sliders,
      annotations = [dict(
         y=0.0,
         xref='paper',
         yref='paper',
         text='Source: <a href="https://www.kaggle.com/datasets/ibrahimshahrukh/global-price-of-healthy-diet-dataset">\
               Kaggle Cost of Healthy Diet by Country (2017-2024)</a>',
         showarrow = False
      )],
      legend=dict(
         x=0.89,
         itemclick=False,
         itemdoubleclick=False
      ),
      # Dropdown menu for different data columns
      updatemenus=[
         dict(
            buttons=[
               dict(
                  args=[{"visible": visible_daily}],
                  label="Daily Healthy Diet Costs",
                  method="update"
               ),
               dict(
                  args=[{"visible": visible_annual}],
                  label="Calculated Total Costs",
                  method="update"
               )
            ],
            direction="down"
         )
      ]
   )

   return fig
   #fig.show()