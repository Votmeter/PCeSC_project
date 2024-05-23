import json
import numpy as np
import matplotlib.pyplot as plt
from Utils_plot import save_plot

exfile = './DB_update/ex.json'

with open(exfile, 'r') as file:
    data = json.load(file)
    # formatted_data = json.dumps(data, indent=4, ensure_ascii=False)

    coordinates= data.get("features")[0].get("geometry").get("coordinates")

    # Separa le coordinate in due array
    latitudes = [coord[1] for coord in coordinates]
    longitudes = [coord[0] for coord in coordinates]

    # Crea gli array NumPy
    latitudes_array = np.array(latitudes)
    longitudes_array = np.array(longitudes)

    # # Stampa gli array per verifica
    # print("Array di latitudini:", latitudes_array)
    # print("Array di longitudini:", longitudes_array)


save_plot( longitudes_array, latitudes_array, "test1")





