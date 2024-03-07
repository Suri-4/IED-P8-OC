from fastapi import FastAPI, HTTPException
from mongita import MongitaClientDisk
from pydantic import BaseModel

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

@app.get("/")
async def root():
    return {"message": "Bonjour et Bienvenue sur ma Base de Données Musicale qui contient un mélange de 2 playlists différentes."}

@app.get("/Musiques/{Musique_id}") # Récupérer une musique par son ID
async def get_musique_by_id(Musique_id: int):
    if Musiques.count_documents({"id": Musique_id}) > 0:
        Musique = Musiques.find_one({"id": Musique_id})
        return {key:Musique[key] for key in Musique if key != "_id"}
    raise HTTPException(status_code=404, detail="Musique non trouvé avec cet ID : {Musique_id}")

@app.get("/Musiques") # Récupérer toutes les musiques fonctionne pas vraiment
async def get_musiques():
    liste_musiques = Musiques.find({})
    return [
        {key:Musique[key] for key in Musique if key != "_id"}
        for Musique in liste_musiques
    ]

# @app.get("/Musiques")
# async def get_all_musique():
#     liste_musiques = Musiques.find({})
#     return [
#         {key:Musique[key] for key in Musique if key != "_id"}
#         for Musique in liste_musiques
#     ]

# @app.post("/Musiques") # Ajout d'une musique
# async def post_Musique(Musique: Musique):
#     Musiques.insert_one(Musique.dict())
#     return Musique

@app.post("/Musiques") # Ajouter une musique
async def ajouter_musique(nom: str, lien: str, style: str, plateforme: str, id: int):
    musique = Musique(nom=nom, lien=lien, style=style, plateforme=plateforme, id=id)
    Musiques.insert_one(musique.model_dump())
    return musique

@app.put("/Musiques/{Musique_id}") # Modifier une musique avec son ID
async def put_Musique(Musique_id: int, Musique: Musique):
    if Musiques.count_documents({"id": Musique_id}) > 0:
        Musiques.replace_one({"id": Musique_id}, Musique.dict())
        return Musique
    raise HTTPException(status_code=404, detail="Musique non trouvé avec cet ID : {Musique_id}")

@app.delete("/Musiques/{Musique_id}") # Supprimer une musique avec son ID
async def delete_Musique(Musique_id: int):
    delete_result = Musiques.delete_one({"id": Musique_id})
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"Musique non trouvée avec cet ID : {Musique_id}")
    return {"OK": True}

