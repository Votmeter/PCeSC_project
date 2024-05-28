#from google.cloud import firestore
import pandas as pd
import plotly
import plotly.graph_objects as go
import plotly.express as px
import json

import os

def create_plot2():

	db = 'tesinapcesc'
	coll = 'trajectories'
	id = 'trajectories'

	# db = firestore.Client.from_service_account_json('credentials.json', database=db)
	df = pd.read_csv("document/gps.csv", header=0)

	df = df.rename(columns={'individual-taxon-canonical-name': "Bird's Type", "location-long": "longitudine"})

	fig = px.scatter_mapbox(df, lat="location-lat", lon="longitudine", color="individual-local-identifier",
							# size="car_hours",
							color_continuous_scale=px.colors.cyclical.IceFire, size_max=15,  # zoom=10,
							mapbox_style="carto-positron")
	return fig.to_json()


def create_plot():

	db = 'tesinapcesc'
	coll = 'trajectories'
	id = 'trajectories'

	#db = firestore.Client.from_service_account_json('credentials.json', database=db)
	df=pd.read_csv("document/gps.csv", header=0)

	df = df.rename(columns = {'individual-taxon-canonical-name': "Bird's Type", "location-long": "longitudine"})

	fig = px.scatter_mapbox(df, lat="location-lat", lon="longitudine", color="Bird's Type", #size="car_hours",
	                  color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, #zoom=10,
	                  mapbox_style="carto-positron")

	return fig.to_json()
