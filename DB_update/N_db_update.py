import json
import matplotlib.pyplot as plt
from Utils_plot import save_plot

exfile = './DB_update/json/trajectories.json'

# input
idtraj = "91930A"
points = [2, 5 , 9]
u_coords= [[
                0,
                0
            ],
            [
                2,
                2
            ],
            [
                3,
                3
            ]]


with open(exfile, 'r') as file:
    data = json.load(file)

    for t in range(len(data)):
        if data[t].get("id") == idtraj:
            iter = 0
            for h in points:
                data[t].get("coordinates")[h] = u_coords[iter]
                iter+= 1

    print(json.dumps(data[-1], indent=4))

 
# save_plot( longitudes_array, latitudes_array, "test1")





