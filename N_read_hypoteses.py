import pandas as pd
argos_path = "./document/argos.csv"
gps_path = "./document/gps.csv"
reference_path = "./document/reference-data.csv"

gps =pd.read_csv(gps_path)
gps = gps.loc[:, ['event-id', 'timestamp', 'location-long', 'location-lat',
                   'individual-local-identifier']]

# Formato unix (numero di secondi trascorsi dal 1° gennaio 1970 (00:00:00 UTC)
# fino al momento specifico). Vantaggi:
# - persistenza dei dati
# - precisione 
# -universalità

# # Conversione dei valori della colonna 'timestamp' in formato Unix
# gps['timestamp'] = pd.to_datetime(gps['timestamp'])
# gps['timestamp'] = gps['timestamp'].apply(lambda x: int(x.timestamp()))
gps.to_csv("./document/gps_Updated.csv")
