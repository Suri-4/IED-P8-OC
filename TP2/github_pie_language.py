# *******************************************************
# Nom ......... : github_pie_language.py
# Rôle ........ : Réalise un graphique circulaire des langages de programmation utilisés dans les 50 projets les plus populaires sur Github
# Auteur ...... : Sacha DELIEGE
# Version ..... : V1 du 20/02/2024
# Licence ..... : réalisé dans le cadre du cours du cours OC de l'IED Paris 8
# Compilation : python3 github_pie_language.py
# Usage : Génère un fichier html contenant un graphique circulaire des langages de programmation utilisés dans les 50 projets les plus populaires sur Github (triés par nombre d'étoiles)
#********************************************************

import requests
from plotly.graph_objs import Pie
from plotly import offline

# URL de l'API Github - tri par nombre d'étoiles et limité à 50 résultats
url = 'https://api.github.com/search/repositories?q=stars:>0&sort=stars&order=desc&per_page=50'

headers = {'Accept': 'application/vnd.github.v3+json'}

# Récupération des données - Status code 200 = OK
r = requests.get(url, headers=headers)
print(f"Status code: {r.status_code}")
result = r.json()


# Récupération des dépôts dans une liste
repos = result['items']

# Création d'un dictionnaire pour les langages de programmation
languages = {}

# Comptage des langages de programmation
for repo in repos:
    language = repo['language']
    if language in languages:
        # Si le langage est déjà dans le dictionnaire, on incrémente le compteur
        languages[language] += 1
    else:
        # Si le langage n'est pas dans le dictionnaire, on l'ajoute
        languages[language] = 1

# Création des listes pour les données du graphique
labels = list(languages.keys())
values = list(languages.values())

# Création des données pour le graphique
data = [{
    'type': 'pie',
    'labels': labels,
    'values': values,
    'hovertext': labels, 
    'text': labels, 
    'marker': {
        'line': {
            'color': 'black',
            'width': 1
        },
    }
}]

# Création du layout
layout = {
    'title': 'Nombre de dépôts par langage de programmation (Top 50 Github Projects)',
    'titlefont': {'size': 28},
}

# Création du graphique
fig = {'data': data, 'layout': layout}
offline.plot(fig, filename='github_language.html')