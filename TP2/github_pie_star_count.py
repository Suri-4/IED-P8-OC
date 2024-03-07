# *******************************************************
# Nom ......... : github_pie_star_count.py
# Rôle ........ : Récupère les 50 projets les plus populaires sur Github et les affiche dans un graphique circulaire
# Auteur ...... : Sacha DELIEGE
# Version ..... : V2 du 19/02/2024
# Licence ..... : réalisé dans le cadre du cours du cours OC de l'IED Paris 8
# Compilation : python3 github_pie_star_count.py
# Usage : Génère un fichier html contenant un graphique circulaire des 50 projets les plus populaires sur Github (triés par nombre d'étoiles)
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
# print(f"Total repositories: {result['total_count']}")

# Récupération des dépot dans une liste
repos = result['items']

# Création des listes pour les données du graphique
repo_links, stars, labels = [], [], []

for repo in repos:
    # Création des liens pour les dépots
    repo_name = repo['name']
    repo_url = repo['html_url']
    repo_link = f"<a href='{repo_url}' style='color: #000000; border: 1px solid #000000;'>{repo_name}</a>"
    repo_links.append(repo_link)

    # Récupération du nombre d'étoiles
    stars.append(repo['stargazers_count'])

    # Création des labels pour les dépots
    owner = repo['owner']['login']
    language = repo['language']
    label = f"Name: {repo_name}<br />Owner: {owner}<br />Language: {language}" 
    labels.append(label)

# Création des données pour le graphique
data = [{
    'type': 'pie',
    'labels': repo_links,
    'values': stars,
    'hovertext': labels, 
    'text': repo_links, 
    'marker': {
        'line': {
            'color': 'black',
            'width': 1
        }
    }
}]

# Création du layout
layout = {
    'title': 'Top 50 Github Projects (Triés par nombre d\'étoiles)',
    'titlefont': {'size': 28},
}

# Création du graphique
fig = {'data': data, 'layout': layout}
offline.plot(fig, filename='github_star.html')