import json
def CreateJSONfromCSV(group):
    
    traj = {
    "id": group.iloc[0,0],
    "specie": group.iloc[0,1],
    "technology": group.iloc[0,2],

    "coordinates": group['coordinates'].to_list(),
    "times": group['times'].to_list(),
    }
    return traj
def JSONtoFile(traj, filename):
    with open(f"DB_update/json/{filename}.json", 'w') as file:
        json.dump(traj, file, indent=4)

def CreateJSONfromGeoJSON(id, name, technology, coords, times):
    traj = {
        "id": id,
        "specie": name,
        "technology": technology,

        "coordinates": coords,
        "times": times,
    }
    return traj