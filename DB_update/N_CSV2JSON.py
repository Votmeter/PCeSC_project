import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
from Utils_JSON import CreateJSONfromCSV, JSONtoFile

filename = "document/gps.csv"
gps = pd.read_csv(filename)
# ["individual-taxon-canonical-name","sensor-type","location-long", "location-lat", "timestamp"]
gps = gps.loc[:, ["individual-local-identifier", 
                  "individual-taxon-canonical-name", 
                  "sensor-type", 
                  "location-long", 
                  "location-lat", 
                  "timestamp"]]
# Convertire la colonna timestamp in formato datetime
gps['timestamp'] = pd.to_datetime(gps['timestamp'])

# Convertire la colonna datetime in formato Unix
gps['timestamp'] = gps['timestamp'].astype(int) // 10**9

# Rinominare le colonne
gps.rename(columns={
    "individual-local-identifier": "id",
    "individual-taxon-canonical-name": "name",
    "sensor-type": "sensor",
    "location-long": "long",
    "location-lat": "lat",
    "timestamp": "times"
}, inplace=True)

print("Visualizzazione dei gruppi:")

# traj è una lista che conterrà tutti i json delle singole traiettorie
traj = []
for name, group in gps.groupby(["id", "name"]):
    group['coordinates'] = group.apply(lambda row: [row['long'], row['lat']], axis=1)
    # per aggiungere i json è sufficiente andarli ad aggiungere alla lista
    traj.append(CreateJSONfromCSV(group))

# json goes to the file
with open("DB_update/json/trajectories.json", "w") as file:
    json.dump(traj, file, indent=4)

    
