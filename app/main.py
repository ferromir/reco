from fastapi import FastAPI, HTTPException
from typing import Dict, List
from database import Db, Entity
    

app = FastAPI()

# Set index size to 10,000
db = Db(10000, ["type", "generation", "genre"])

# Setup data:
db.add_entity(Entity(id="fernando", props={"type": "person", "generation": "millennial"}))
db.add_entity(Entity(id="keyla", props={"type": "person", "generation": "millennial"}))
db.add_entity(Entity(id="noel", props={"type": "person", "generation": "genz"}))
db.add_entity(Entity(id="clara", props={"type": "person", "generation": "genz"}))
db.add_entity(Entity(id="coldplay", props={"type": "artist", "genre": "rock"}))
db.add_entity(Entity(id="u2", props={"type": "artist", "genre": "rock"}))
db.add_entity(Entity(id="oasis", props={"type": "artist", "genre": "rock"}))
db.add_entity(Entity(id="the1975", props={"type": "artist", "genre": "pop"}))
db.add_rel("fernando", "likes", "coldplay")
db.add_rel("keyla", "likes", "coldplay")
db.add_rel("keyla", "likes", "u2")
db.add_rel("noel", "likes", "u2")
db.add_rel("noel", "likes", "oasis")
db.add_rel("clara", "likes", "the1975")
db.add_rel("coldplay", "is_liked_by", "fernando")
db.add_rel("coldplay", "is_liked_by", "keyla")
db.add_rel("u2", "is_liked_by", "keyla")
db.add_rel("u2", "is_liked_by", "noel")
db.add_rel("oasis", "is_liked_by", "noel")
db.add_rel("the1975", "is_liked_by", "clara")


@app.post("/entities")
async def add_entity(entity: Entity) -> Entity:
    if db.has_entity(entity.id):
        raise HTTPException(status_code=400, detail="Duplicate")
    return db.add_entity(entity)


@app.post("/entities/search")
async def search_entities(props: Dict[str, str]) -> List[Entity]:
    return db.search(props)


@app.post("/entities/{source_id}/{link}/{target_id}")
async def add_relationship(source_id: str, link: str, target_id: str) -> None:
    if not db.has_entity(source_id) or not db.has_entity(target_id):
        raise HTTPException(status_code=404, detail="Missing entity")
    return db.add_rel(source_id, link, target_id)


@app.post("/entities/{id}/recommendations")
async def find_recommendations(id: str, links: List[str]) -> List[Entity]:
    acc: List[Entity] = []
    db.recommendations(id, [], 0, links, acc)
    return acc