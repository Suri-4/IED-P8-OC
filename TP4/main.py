# *******************************************************
# Nom ......... : main.py
# Rôle ........ : Création d'une plateforme streamlit pour le TP4
# Auteur ...... : Sacha DELIEGE
# Version ..... : V1 du 07/03/2024
# Licence ..... : réalisé dans le cadre du cours du cours OC de l'IED Paris 8
# Compilation : streamlit run main.py
# Usage : Création d'une plateforme streamlit pour le TP4 qui contient 3 parties différentes
# Usage : 1. Afficher les métadonnées d'une image (EXIF)
# Usage : 2. Afficher les coordonnées GPS d'une image sur une carte
# Usage : 3. Afficher une carte avec des POI
#********************************************************

import streamlit as st

st.set_page_config(page_title="TP4 - OC")

st.write("Bienvenue sur mon travail pour le TP4 du cours d'OC de l'IED Paris 8.")

st.write("Depuis cette page, vous pouvez accéder à mes travaux pour ce TP, en cliquant sur les liens dans la sidebar.")

st.write("Ce TP est composé de 3 parties : ")

st.write("1. Afficher les métadonnées d'une image")
st.write("2. Afficher les coordonnées GPS d'une image sur une carte")
st.write("3. Afficher une carte avec des POI")


