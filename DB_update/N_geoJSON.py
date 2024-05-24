import json
from Utils_JSON import CreateJSONfromGeoJSON

exfile = 'DB_update/json/ex.json'
DB = "DB_update/json/trajectories.json"
# input
id = ""
name = ""
technology = ""
times = []


with open(exfile, 'r') as update:
    data = json.load(update)
    coordinates = data.get('features')[0].get('geometry', {}).get('coordinates')
    traj = CreateJSONfromGeoJSON(id, name, technology, coordinates, times)


with open(DB, "r") as file:
    dbtraj = json.load(file)
    dbtraj.append(traj)

with open(DB, "w") as file:
    json.dump(dbtraj, file, indent=4)
