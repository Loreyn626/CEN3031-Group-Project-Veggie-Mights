import plotly.graph_objects as go
from data.classes import *
from data.parsing import countries

for country in countries:
   print(country.name)

def plotMap():
   costs = ['Low', 'Medium', 'High']
   colors = ['green', 'orange', 'red']

   fig = go.Figure()

   # go.Choropleth is where data is actaully being inserted
   for i in range(len(costs)):
      fig.add_trace(go.Choropleth(
         # insert country names here as an array
         locations=['USA'],
         locationmode='country names',
         # this containes some data being displayed for USA
         z=[1],
         # for now this is labeling USA three different times with green, then orange, then red, so it shows up as red in the end
         colorscale=[[0, colors[i]], [1, colors[i]]],
         showscale=False,
         # this contains some data being displayed
         name=costs[i],
      ))

   # go.Scattergeo function is only being used to incorporate a figure lebels for the colors
   # don't insert any data here
   for i in range(len(costs)):
      fig.add_trace(go.Scattergeo(
         locations=['USA'],
         locationmode='country names',
         marker_color= colors[i],
         name=costs[i],
         showlegend=True,
         hoverinfo='skip',
      ))

   # this can be used to adjust layout and maybe the UI for the data
   fig.update_layout(
      title_text='Cost of Healthy Diet by Country',
      geo=dict(
         showframe=True,
         showcoastlines=True,
         projection_type='equirectangular'
      ),
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