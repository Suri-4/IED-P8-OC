# *******************************************************
# Nom ......... : image_exif.py
# Rôle ........ : Afficher les métadonnées d'une image (EXIF) et les modifier
# Auteur ...... : Sacha DELIEGE
# Version ..... : V1 du 07/03/2024
# Licence ..... : réalisé dans le cadre du cours du cours OC de l'IED Paris 8
# Compilation : streamlit run image_exif.py
# Usage : Afficher les métadonnées d'une image (EXIF) et les modifier dans un formulaire
#********************************************************

import streamlit as st
from ast import literal_eval
from PIL import Image, ExifTags

# Afficher les métadonnées de l'image dans un formulaire
def display_form_metadata(formulaire, data):
    # Parcourir les métadonnées de l'image
    for key, val in data.items():
        if key in ExifTags.TAGS:
            formulaire[key] = st.text_input(ExifTags.TAGS[key], value=str(val))
        else:
            formulaire[key] = st.text_input(str(key), value=str(val))

# Afficher les coordonnées GPS dans un formulaire
def display_gps_form(data):
    new_gps_data = {} # initialiser un dictionnaire vide

    # Parcourir les coordonnées GPS
    for key, val in data.items():
        if key % 2 == 0: # si la clé est paire (elle contient les coordonnées)
            new_gps_data[key] = literal_eval(st.text_input(ExifTags.GPSTAGS[key], val)[1:-1])
        else: # si la clé est impaire (elle contient les coordonnées direction)
            new_gps_data[key] = st.text_input(ExifTags.GPSTAGS[key], str(val))

    return new_gps_data

# Mettre à jour les métadonnées de l'image (avec conversion de type si nécessaire)
def update_metadata(formulaire, new_exif_data):
    for key, val in formulaire.items():
        if key in new_exif_data and new_exif_data[key] != val:
            if type(new_exif_data[key]) == type(val):
                new_exif_data[key] = val
            elif isinstance(new_exif_data[key], int):
                new_exif_data[key] = int(val)
            elif isinstance(new_exif_data[key], float):
                new_exif_data[key] = float(val)
            elif isinstance(new_exif_data[key], bool):
                new_exif_data[key] = bool(val)

    return new_exif_data

if __name__ == "__main__":
    st.title("Image Metatada Editor")

    # Charger l'image
    uploaded_image = st.file_uploader("Upload an image", ["jpg", "jpeg", "png"])

    if uploaded_image is not None:
        img = Image.open(uploaded_image)
        st.image(img, caption="Uploaded Image", use_column_width=True)

        # Récupérer les métadonnées de l'image
        exif_data = img.getexif()
        gps_ifd_data = exif_data.get_ifd(ExifTags.IFD.GPSInfo)

        if exif_data is None:
            st.write("No metadata found for this image.")

        # Initialiser un dictionnaire vide pour stocker les métadonnées du formulaire
        form = {}

        display_form_metadata(form, exif_data)
        new_gps_data = display_gps_form(gps_ifd_data) 

        # Enregistrer les modifications
        if st.button("Save Image"):
            new_exif_data = exif_data 
            new_exif_data[ExifTags.IFD.GPSInfo] = new_gps_data

            update_metadata(form, new_exif_data)

            # Enregistrer une nouvelle image avec les nouvelles métadonnées
            img.save("new_img.jpg", exif=new_exif_data)
            # Ajouter un bouton pour télécharger l'image
            st.download_button("Download Image", "new_img.jpg", "Cliquez ici pour télécharger l'image.")

            st.success("Image saved successfully.")
