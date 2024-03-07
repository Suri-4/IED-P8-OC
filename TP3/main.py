# *******************************************************
# Nom ......... : main.py
# Rôle ........ : Création d'une API REST pour une base de données musicale
# Auteur ...... : Sacha DELIEGE
# Version ..... : V1 du 26/02/2024
# Licence ..... : réalisé dans le cadre du cours du cours OC de l'IED Paris 8
# Compilation : python3 main.py
# Usage : Création d'une API REST pour une base de données musicale
# Usage : L'API permet de récupérer, ajouter, modifier et supprimer des musiques
# Usage : Utilisation d'une base de données NoSQL Mongita et d'un serveur local uvicorn
#********************************************************

from fastapi import FastAPI, HTTPException
from mongita import MongitaClientDisk
from pydantic import BaseModel

# Création de la classe Musique
class Musique(BaseModel):
    nom: str
    lien: str
    style: str
    plateforme: str
    id: int

app = FastAPI()

client = MongitaClientDisk()
db = client.db
Musiques = db.Musiques

# Initialisation de la base de données
if Musiques.count_documents({}) == 0:
    Musiques.insert_many([
        {"nom": "L'amour Toujours (Hardstyle)", "lien": "https://www.youtube.com/watch?v=nsX979LauNY", "style": "Hardstyle", "plateforme": "Youtube", "id": 1},
        {"nom": "Starset - My Demons (Official Music Video)", "lien": "https://www.youtube.com/watch?v=nkll0StZJLA", "style": "Alternative Rock", "plateforme": "Youtube", "id": 2},
        {"nom": "Just Dance (Hardstyle Remix) (SPED UP)", "lien": "https://www.youtube.com/watch?v=7W9IOhk1-z4", "style": "Hardstyle", "plateforme": "Youtube", "id": 3},
        {"nom": "tatli - depression(dragon ball remix)", "lien": "https://www.youtube.com/watch?v=mYe_zcCDqiA", "style": "Electro", "plateforme": "Youtube", "id": 4},
        {"nom": "Il changeait la vie", "lien": "https://open.spotify.com/track/3YedumgdhKXi5MRAvvzNP2", "style": "French Indie", "plateforme": "Spotify", "id": 5},
        {"nom": "Freed From Desire", "lien": "https://open.spotify.com/track/3u5N55tHf7hXATSQrjBh2q", "style": "Electro", "plateforme": "Spotify", "id": 6},
        {"nom": "What is Love", "lien": "https://open.spotify.com/track/0DXswAITgjQTi7anZG33af", "style": "Pop", "plateforme": "Spotify", "id": 7},
        {"nom": "blu da ba dee", "lien": "https://open.spotify.com/track/2yAVzRiEQooPEJ9SYx11L3", "style": "Electro", "plateforme": "Spotify", "id": 8},
        {"nom": "Gimme! Gimme! Gimme! (Hardstyle Edit)", "lien": "https://www.youtube.com/watch?v=aMR59YrgiM8", "style": "Hardstyle", "plateforme": "Youtube", "id": 9},
        {"nom": "Tevvez - Legend", "lien": "https://www.youtube.com/watch?v=5OZ-JOSWx1Q", "style": "Hardstyle", "plateforme": "Youtube", "id": 10},
        {"nom": "fnaf hardstyle remix", "lien": "https://www.youtube.com/watch?v=VhgAcrfBa1M", "style": "Hardstyle", "plateforme": "Youtube", "id": 11},
        {"nom": "Bring Me To Life", "lien": "https://open.spotify.com/track/0COqiPhxzoWICwFCS4eZcp", "style": "Hard rock", "plateforme": "Spotify", "id": 12},
        {"nom": "In The End", "lien": "https://open.spotify.com/track/60a0Rd6pjrkxjPbaKzXjfq", "style": "Rap/Metal", "plateforme": "Spotify", "id": 13},
        {"nom": "Ce matin va être une pure soirée", "lien": "https://open.spotify.com/track/7jkGEREsrWQrNU6PwurJA4", "style": "French Rap", "plateforme": "Spotify", "id": 14},
        {"nom": "THE DOOMSLAYER - KIL KROOK", "lien": "https://www.youtube.com/watch?v=1XhzCk_3r1c", "style": "Hardstyle", "plateforme": "Youtube", "id": 15},
    ])
else:
    Musiques.delete_many({})

@app.get("/")
async def root():
    return {"message": "Bonjour et Bienvenue sur ma Base de Données Musicale qui contient un mélange de 2 playlists différentes."}

@app.get("/Musiques/{Musique_id}") # Récupérer une musique par son ID
async def get_musique_by_id(Musique_id: int):
    if Musiques.count_documents({"id": Musique_id}) > 0:
        Musique = Musiques.find_one({"id": Musique_id})
        return {key:Musique[key] for key in Musique if key != "_id"}
    raise HTTPException(status_code=404, detail="Musique non trouvé avec cet ID : {Musique_id}")

@app.get("/Musiques") # Récupérer toutes les musiques
async def get_all_musique():
    liste_musiques = Musiques.find({})

    return [
        { key: m[key] for key in m if key != "_id" }
        for m in liste_musiques
    ]

@app.post("/Musiques") # Ajouter une musique
async def ajouter_musique(nom: str, lien: str, style: str, plateforme: str, id: int):
    musique = Musique(nom=nom, lien=lien, style=style, plateforme=plateforme, id=id)
    Musiques.insert_one(musique.model_dump())
    return musique

@app.put("/Musiques/{Musique_id}") # Modifier une musique avec son ID
async def put_Musique(Musique_id: int, Musique: Musique):
    if Musiques.count_documents({"id": Musique_id}) > 0:
        Musiques.replace_one({"id": Musique_id}, Musique.model_dump())
        return Musique
    raise HTTPException(status_code=404, detail="Musique non trouvé avec cet ID : {Musique_id}")

@app.delete("/Musiques/{Musique_id}") # Supprimer une musique avec son ID
async def delete_Musique(Musique_id: int):
    delete_result = Musiques.delete_one({"id": Musique_id})
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"Musique non trouvée avec cet ID : {Musique_id}")
    return {"OK": True}

@app.get("/Musiques/plateforme/{plateforme}") # Récupérer une musique par sa plateforme
async def get_musique_by_plateforme(plateforme: str):
    liste_musiques = Musiques.find({"plateforme": plateforme})

    return [
        {key: m[key] for key in m if key != "_id"}
        for m in liste_musiques
    ]
