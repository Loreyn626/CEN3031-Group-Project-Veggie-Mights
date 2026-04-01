import plotly.graph_objects as go
from data.classes import *
from data.parsing import countries

country_names = [] # For locations
all_annual_costs = {} # For annual costs

for country in countries:
   country_names.append(country.name)

   all_annual_costs[country.name] = [] # Initialize array
   for cost in country.annualCosts:
      # Needs to be converted to float, wasn't working properly otherwise
      all_annual_costs[country.name].append(float(cost))


def plotMap():
   cost_categories = ['Low', 'Medium', 'High']
   colors = ['green', 'orange', 'red']

   fig = go.Figure() # Initialize graph object

   # ========= ANNUAL COST + SLIDERS PER YEAR =========
   yearly_z_values = []
   for i in range(8): # 8 years: 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024
      # Each year needs different z-values
      year_z_values = []

      # Add all costs for that specific year
      for name in country_names:
         costs = all_annual_costs[name]

         if i < len(costs):
            cost = costs[i]
         else:
            cost = None

         year_z_values.append(cost)
      
      # Add array of each country's annual cost for the year to a yearly array
      yearly_z_values.append(year_z_values)

   # Determine min and max for the specific year
   # Can't just use min() or max() on z_values because it doesn't work with "None" values
   yearly_costs = []

   for year in yearly_z_values:
      for value in year:
         if value is not None:
            yearly_costs.append(value)

   # zmin & zmax is the lowest and highest value of ALL costs over ALL years
   # This helps keep colorscale consistent between years and when we trace 8 times (1 trace per year)
   zmin = min(yearly_costs)
   zmax = max(yearly_costs)

   # go.Choropleth is where data is actually being inserted
   for i in range(8):
      fig.add_trace(go.Choropleth(
         # insert country names here as an array
         locations=country_names,
         locationmode='country names',
         # Display all annual costs for now before adding more info later
         z=yearly_z_values[i],
         # Color scaling, 0% of the way to max is green, 50% = orange, 100% = red
         colorscale=[[0.0, colors[0]],[0.5, colors[1]],[1.0, colors[2]]],
         showscale=True,
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
         marker_color= colors[i],
         name=cost_categories[i],
         showlegend=True,
         hoverinfo='skip',
      ))

   # Slider functionality for UI, testing with values first before setting it up fully
   # For slider creation and labeling
   steps = []
   for i in range(8): # 8 different years
      # Only show one year's map at a time, prevent overlap
      visible_list = []

      for j in range(8):
         # Include the legend in all years
         visible_list.extend([True] * len(cost_categories))

         if j == i:
            visible_list.append(True)
         else:
            visible_list.append(False)

      step = dict(
         method="update", # Updates map
         args=[{"visible": visible_list}],
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
      )
   )

   return fig
   #fig.show()