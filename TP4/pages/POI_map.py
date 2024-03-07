# *******************************************************
# Nom ......... : POI_map.py
# Rôle ........ : Afficher une carte avec des POI
# Auteur ...... : Sacha DELIEGE
# Version ..... : V1 du 07/03/2024
# Licence ..... : réalisé dans le cadre du cours du cours OC de l'IED Paris 8
# Compilation : streamlit run POI_map.py
# Usage : Afficher une carte avec des POI listés dans un DataFrame
#********************************************************

import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd

# Définir les coordonnées des POI
poi_data = {
    'POI1': {'lat': 49.156049217101454, 'lon': 5.3876759913344285},
    'POI2': {'lat': 39.62621032451711, 'lon': 2.925570871255565},
    'POI3': {'lat': 38.909029655779214, 'lon': 1.4332002297202795},
    'POI4': {'lat': 39.99993073715325, 'lon': 3.839112018027784},
    'POI5': {'lat': 49.79096666344613, 'lon': 5.06095400906704},
    'POI6': {'lat': 48.862530383028634, 'lon': 2.3671350191873497},
    'POI7': {'lat': 50.93428192804182, 'lon': 1.8740564398964432},
    'POI8': {'lat': 49.35984640264357, 'lon': 0.0779518861444517},
    'POI9': {'lat': 51.505051543695124, 'lon': -0.12034290599502562},
    'POI10': {'lat': 48.54306864182446, 'lon': 7.775658465569326},
    'POI11': {'lat': 46.16333346393875, 'lon': -1.134637462198862},
    
}

# Créer un DataFrame à partir des données
df = pd.DataFrame.from_dict(poi_data, orient='index')

# Créer une carte
m = folium.Map(zoom_start=4, location=[47.20383788585732, 2.660937787435307])

# Ajouter les POI à la carte
for index, row in df.iterrows():
    folium.Marker([row['lat'], row['lon']]).add_to(m)

# Relier les points entre eux
for i in range(len(df)-1):
    folium.PolyLine(df).add_to(m)

# Afficher la carte
st_folium(m)


