import plotly.graph_objects as go

def plotMap():
   costs = ['Low', 'Medium', 'High']
   colors = ['green', 'orange', 'red']

   fig = go.Figure()

   for i in range(len(costs)):
      fig.add_trace(go.Choropleth(
         locations=['USA'],
         locationmode='country names',
         z=[1],
         colorscale=[[0, colors[i]], [1, colors[i]]],
         showscale=False,
         name=costs[i],
      ))

   for i in range(len(costs)):
      fig.add_trace(go.Scattergeo(
         locations=['USA'],
         locationmode='country names',
         marker_color= colors[i],
         name=costs[i],
         showlegend=True,
         hoverinfo='skip',
      ))

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