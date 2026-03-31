import plotly.graph_objects as go
from data.classes import *
from data.parsing import countries

country_names = [] # For locations
all_annual_costs = {} # For annual costs

for country in countries:
   print(country.name)
   country_names.append(country.name)

   all_annual_costs[country.name] = [] # Initialize array
   for cost in country.annualCosts:
      # Needs to be converted to float, wasn't working properly otherwise
      all_annual_costs[country.name].append(float(cost))


def plotMap():
   cost_categories = ['Low', 'Medium', 'High']
   colors = ['green', 'orange', 'red']

   fig = go.Figure()

   # go.Choropleth is where data is actually being inserted
   for i in range(8): # 8 years: 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024
      # Each year needs different z-values
      z_values_for_year = []

      # Add all costs for that specific year
      for name in country_names:
         costs = all_annual_costs[name]

         if i < len(costs):
            cost_value = costs[i]
         else:
            cost_value = None

         z_values_for_year.append(cost_value)

      # Determine min and max for the specific year
      # Can't just use min() or max() on z_values because it doesn't work with "None" values
      year_costs = []

      for value in z_values_for_year:
         if value is not None:
            year_costs.append(value)

      zmin = min(year_costs)
      zmax = max(year_costs)

      fig.add_trace(go.Choropleth(
         # insert country names here as an array
         locations=country_names,
         locationmode='country names',
         # Display all annual costs for now before adding more info later
         z=z_values_for_year,
         # Color scaling, 0% of the way to max is green, 50% = orange, 100% = red
         colorscale=[[0.0, colors[0]],[0.5, colors[1]],[1.0, colors[2]]],
         showscale=True,
         # this contains some data being displayed
         name=str(i + 2017),
         zmin=zmin,
         zmax=zmax
      ))

   # Legend currently bugged at the moment
   """
   # go.Scattergeo function is only being used to incorporate figure labels for the colors
   # don't insert any data here
   for i in range(len(cost_categories)):
      fig.add_trace(go.Scattergeo(
         locations=['USA'],
         locationmode='country names',
         marker_color= colors[i],
         name=cost_categories[i],
         showlegend=True,
         hoverinfo='skip',
      ))
   """

   # Slider functionality for UI, testing with values first before setting it up fully
   # For slider creation and labeling
   steps = []
   for i in range(8): # 8 different years
      # Only show one year's map at a time, prevent overlap
      visible_list = []
      for j in range(8):
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
         x=0.89
      )
   )

   return fig
   #fig.show()