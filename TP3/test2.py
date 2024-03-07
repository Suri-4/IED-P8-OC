from fastapi import FastAPI, HTTPException
from mongita import MongitaClientDisk
from pydantic import BaseModel

class Artiste(BaseModel):
    nom: str
    album: str
    nb_morceaux: int
    id: int

app = FastAPI()

client = MongitaClientDisk()
db = client.db
Artistes = db.Artistes

# insert some data
Artistes.insert_many([
    {"nom": "Delain", "album": "Apocalyspe And Chill", "nb_morceaux": 8, "id": 1},
    {"nom": "Nightwish", "album": "Decades", "nb_morceaux": 22, "id": 2},
    {"nom": "Epica", "album": "Omega", "nb_morceaux": 12, "id": 3},
    {"nom": "Leaves'Eyes", "album": "The Last Viking", "nb_morceaux": 28, "id": 4},
    {"nom": "Avantasia", "album": "The Metal Opera Part II", "nb_morceaux": 10, "id": 5},
])



@app.get("/")
async def root():
    return {"message": "Bonjour et Bienvenue sur ma Base de Données Musicale"}

@app.get("/Artistes") # marche pas
async def get_artistes():
    existing_artistes = Artiste.find({})
    return [
        {key:Artiste[key] for key in Artiste if key != "_id"}
        for Artiste in existing_artistes
    ]

@app.get("/Artistes/{Artiste_id}")
async def get_artiste_by_id(Artiste_id: int):
    if Artistes.count_documents({"id": Artiste_id}) > 0:
        Artiste = Artistes.find_one({"id": Artiste_id})
        return {key:Artiste[key] for key in Artiste if key != "_id"}
    raise HTTPException(status_code=404, detail="Artiste non trouvé avec cet ID : {Artiste_id}")

@app.post("/Artistes")
async def post_Artiste(Artiste: Artiste):
    Artistes.insert_one(Artiste.dict())
    return Artiste

@app.put("/Artistes/{Artiste_id}")
async def put_Artiste(Artiste_id: int, Artiste: Artiste):
    if Artistes.count_documents({"id": Artiste_id}) > 0:
        Artistes.replace_one({"id": Artiste_id}, Artiste.dict())
        return Artiste
    raise HTTPException(status_code=404, detail="Artiste non trouvé avec cet ID : {Artiste_id}")

@app.put("/Artistes/upsert/{Artiste_id}")
async def update_Artiste(Artiste_id: int, Artiste: Artiste):
    Artistes.replace_one({"id": Artiste_id}, Artiste.dict(), upsert=True)
    return Artiste

@app.delete("/Artistes/{Artiste_id}")
async def delete_Artiste(Artiste_id: int):
    delete_result = Artistes.delete_one({"id": Artiste_id})
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Artiste non trouvé avec cet ID : {Artiste_id}")
    return {"OK": True}