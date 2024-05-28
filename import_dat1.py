from google.cloud import firestore
import pandas as pd
import os


db = 'tesinapcesc'
coll = 'trajectories1'
id = 'trajectories'

db = firestore.Client.from_service_account_json('credentials.json', database=db)
df=pd.read_csv("document/gps.csv")
cols=["event-id","visible","timestamp","location-long","location-lat","sensor-type",
      "individual-taxon-canonical-name","tag-local-identifier","individual-local-identifier",
      "study-name"]

print(df)
df.columns=cols

for i in range(89869):
    #print(df.loc[i])
    doc_ref = db.collection(df.loc[i]['individual-local-identifier']).document(str(df.loc[i]['event-id']))
    doc_ref.set({"long":df.loc[i]['location-long'], "lat":df.loc[i]['location-lat']})



