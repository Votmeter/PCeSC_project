from google.cloud import firestore
import pandas as pd
import os


db = 'tesinapcesc'
coll = 'trajectories'
id = 'trajectories'

db = firestore.Client.from_service_account_json('credentials.json', database=db)
df=pd.read_csv("document/gps.csv")
cols=["event-id","visible","timestamp","location-long","location-lat","sensor-type",
      "individual-taxon-canonical-name","tag-local-identifier","individual-local-identifier",
      "study-name"]

print(df)
df.columns=cols
#dd
for i in range(89871):
    #print(df.loc[i])
    doc_ref = db.collection(coll).document(str(df.loc[i]['event-id']))
    doc_ref.set({"time":df.loc[i]['timestamp'],"location-long":df.loc[i]['location-long'],
                 "location-lat":df.loc[i]['location-lat'],"bird":df.loc[i]['individual-taxon-canonical-name'],
                 "bird-id":df.loc[i]['individual-local-identifier']})




