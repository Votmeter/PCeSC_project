import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Funzione che calcola la distanza tra due punti sulla superficie della Terra usando la formula di Haversine
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Raggio della Terra in km
    phi1, phi2 = np.radians(lat1), np.radians(lat2)
    dphi = np.radians(lat2 - lat1)
    dlambda = np.radians(lon1 - lon2)
    a = np.sin(dphi / 2) ** 2 + np.cos(phi1) * np.cos(phi2) * np.sin(dlambda / 2) ** 2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    return R * c


# Funzione principale per creare il grafico
def create_corridor_plot():
    try:
        # Leggi i 2 file CSV
        df_gps = pd.read_csv("document/gps.csv", header=0)
        df_ref = pd.read_csv("document/reference-data.csv", header=0)
        # gestisco gli eventuali errori
    except FileNotFoundError:
        print("Errore: Uno o più file CSV non sono stati trovati.")
        return
    except pd.errors.EmptyDataError:
        print("Errore: Uno o più file CSV sono vuoti.")
        return
    except pd.errors.ParserError:
        print("Errore: Uno o più file CSV non sono stati parsati correttamente.")
        return

    # Rinominiamo le colonne per facilità di accesso per document/gps.csv
    df_gps = df_gps.rename(columns={
        'individual-taxon-canonical-name': "Tipologia di uccello",
        'location-long': "Longitudine",
        'location-lat': "Latitudine",
        'individual-local-identifier': 'animal-id'
    })
    # Rinominiamo le colonne per facilità di accesso per document/reference-data.csv
    df_ref = df_ref.rename(columns={
        'individual-local-identifier': 'animal-id',
        'manipulation-comments': 'comments'
    })

    # Uniamo i dataframe sui valori comuni di 'animal-id'
    df = pd.merge(df_gps, df_ref, on='animal-id')

    # Determiniamo l'origine degli uccelli basandosi su: 'comments'
    df['Origine'] = df['comments'].apply(
        lambda x: 'Helgoland' if 'Heligoland' in x else 'Kazan' if 'Kazan' in x else 'Unknown')

    # Filtra i dati per includere solo gli uccelli che hanno realizzato lo spostamento
    df = df[df['Origine'] != 'Unknown']

    # Ordina i dati per 'animal-id'
    df = df.sort_values(by=['animal-id'], ascending=[True])

    # Utilizziamo come traiettoria migratoria la mediana delle Longitudini
    long_traiettoria_migratoria = df['Longitudine'].median()
    print("Il punto medio per le Longitudini è:", long_traiettoria_migratoria)

    # Calcola la distanza tra ciascun punto e la longitudine media, tenendo conto del segno
    df['Distance_to_mean'] = df.apply(lambda row: haversine(
        row['Latitudine'], row['Longitudine'],
        row['Latitudine'], long_traiettoria_migratoria
    ) * (-1 if row['Longitudine'] < long_traiettoria_migratoria else 1), axis=1)

    # Calcola le distanze medie per latitudine e tipologia di uccello
    grouped = df.groupby(['Origine', 'Tipologia di uccello', 'Latitudine']).agg(
        Distance_mean=('Distance_to_mean', 'mean'),
        Distance_std=('Distance_to_mean', 'std')
    ).reset_index()

    # Calcola i punti medi per ciascuna latitudine
    mean_points = df.groupby(['Origine', 'Latitudine']).agg(
        Longitudine_mean=('Longitudine', 'mean')
    ).reset_index()

    # Creazione del grafico
    fig, ax = plt.subplots(figsize=(14, 7))
    #fig.suptitle('Distanze Medie degli Uccelli Traslocati dal Corridoio Migratorio', fontsize=16)
    #vedere se aggiungere colonna per olfatto
    '''
    color_map = {
        'Uccelli di controllo': 'blue',
        'Uccelli con sezione del nervo trigemino': 'green',
        'Uccelli con sezione del nervo olfattivo': 'red'
    }'''

    for origine in ['Helgoland', 'Kazan']:
        temp_df = grouped[grouped['Origine'] == origine]
        mean_df = mean_points[mean_points['Origine'] == origine]

        # Traccia le linee per tutti i punti
        for bird_type in temp_df['Tipologia di uccello'].unique():
            bird_df = temp_df[temp_df['Tipologia di uccello'] == bird_type]
            ax.errorbar(bird_df['Distance_mean'], bird_df['Latitudine'],
                        xerr=bird_df['Distance_std'], fmt='-o', label=f'{origine} - {bird_type}' )

        # Traccia i punti medi per ciascuna latitudine
        ax.scatter(mean_df['Longitudine_mean'], mean_df['Latitudine'], label=f'{origine} - Punti medi', s=100)

    ax.axvline(x=0, color='green', linestyle='--')  # Linea verticale mediana
    ax.set_xlabel('Distanza dal corridoio migratorio (km)')
    ax.set_ylabel('Latitudine')
    ax.legend()

    # Salvataggio del grafico come file immagine
    plt.savefig('static/corridor_plot.png')
    #plt.show()


if __name__ == '__main__':
    create_corridor_plot()
