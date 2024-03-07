# *******************************************************
# Nom ......... : map_gps_image.py
# Rôle ........ : Afficher les coordonnées GPS d'une image sur une carte
# Auteur ...... : Sacha DELIEGE
# Version ..... : V1 du 07/03/2024
# Licence ..... : réalisé dans le cadre du cours du cours OC de l'IED Paris 8
# Compilation : streamlit run map_gps_image.py
# Usage : Afficher les coordonnées GPS d'une image sur une carte
#********************************************************

import streamlit as st
import pandas as pd
from PIL import Image, ExifTags

# Convertir les coordonnées GPS en décimal
def convert_gps_ifd_decimal(image):
    img = Image.open(image)
    # Récupérer les données EXIF
    exif_data = img.getexif()
    gps_ifd_data = exif_data.get_ifd(ExifTags.IFD.GPSInfo)

    if gps_ifd_data:
        # Récupérer les coordonnées GPS
        latitude = gps_ifd_data[2]
        longitude = gps_ifd_data[4]
        
        # Convertir les coordonnées en décimal
        latitude_decimal = float(latitude[0]) + float(latitude[1]/60) + float(latitude[2]/3600)
        longitude_decimal = float(longitude[0]) + float(longitude[1]/60) + float(longitude[2]/3600)
    
        return latitude_decimal, longitude_decimal
    else:
        st.write("No GPS information found.")

if __name__ == "__main__":
    st.title("Image GPS data viewer")
    uploaded_image = st.file_uploader("Upload an image", ["jpg", "jpeg", "png"])

    if uploaded_image is not None:
        lat, lon = convert_gps_ifd_decimal(uploaded_image)

        # Afficher les coordonnées GPS sur une carte
        st.map(pd.DataFrame({'lat': [lat], 'lon': [lon]}), zoom=4)