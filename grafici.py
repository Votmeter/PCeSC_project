import plotly.graph_objects as go
import plotly.express as px
import json
import os
import pandas as pd
import plotly.express as px
import json

def create_plot():

	db = 'tesinapcesc'
	coll = 'trajectories'
	id = 'trajectories'

	df = pd.read_csv("document/gps.csv", header=0)
	df = df.rename(columns={'individual-taxon-canonical-name': "Tipologia di uccello",
        'location-long': "Longitudine",
        'location-lat': "Latitudine",
        'individual-local-identifier': 'animal-id'})

	# Scatter plot for points
	scatter = px.scatter_mapbox(df, lat="Latitudine", lon="Longitudine", color="animal-id",
								color_continuous_scale=px.colors.cyclical.IceFire, size_max=15,
								mapbox_style="carto-positron")

	# Line plot for trajectories
	line = px.line_mapbox(df, lat="Latitudine", lon="Longitudine", color="animal-id",
						  mapbox_style="carto-positron")

	# Combine scatter and line plots
	fig = go.Figure()
	for data in scatter.data:
		data.showlegend = False  # Hide legend for scatter plot
		fig.add_trace(data)
	for data in line.data:
		fig.add_trace(data)

	fig.update_layout(mapbox_style="carto-positron")
	return fig.to_json()

# Generate the plots
combined_plot_json2 = create_plot()

fig2 = go.Figure(json.loads(combined_plot_json2))
#fig2.show()