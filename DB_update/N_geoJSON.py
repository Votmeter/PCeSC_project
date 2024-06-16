import json
from Utils_JSON import CreateJSONfromGeoJSON
from google.cloud import firestore 

exfile = 'DB_update/json/ex.json'

with open(exfile, 'r') as new:

    data = json.load(new)
    coordinates = data.get('features')[0].get('geometry', {}).get('coordinates')
    traj = {
        "name": {
            str(index): coord for index, coord in enumerate(coordinates)



        }

    }
    print(coordinates)
    print(json.dumps(traj, indent=4))





