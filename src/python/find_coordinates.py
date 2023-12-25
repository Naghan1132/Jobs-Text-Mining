from geopy.geocoders import Nominatim
import pandas as pd

# Charger le DataFrame à partir du fichier CSV
df = pd.read_csv("src/data/concatenated_data.csv")

# Initialiser le géocodeur
geolocator = Nominatim(user_agent="my_geocoder")

# Fonction pour obtenir les coordonnées à partir d'un nom de ville
def get_coordinates(city):
    location = geolocator.geocode(f"{city}, France")
    if location:
        print(location.latitude, location.longitude)
        return location.latitude, location.longitude
    else:
        return None, None

# Appliquer la fonction get_coordinates pour chaque ville et créer de nouvelles colonnes
df[['latitude', 'longitude']] = df['location'].apply(lambda x: pd.Series(get_coordinates(x)))

# Afficher les 5 premières lignes pour vérifier
print(df.head())

# Sauvegarder le DataFrame avec les nouvelles colonnes dans un nouveau fichier CSV si nécessaire
df.to_csv("src/data/concatenated_data_with_coordinates.csv", index=False)
