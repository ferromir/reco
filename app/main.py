from fastapi import FastAPI
from typing import Dict, List
from database import Database, Entity

app = FastAPI()
db = Database()

# Testing dataset:

db.add_entity(Entity(id="fernando",properties={"generation":"millennial"}))
db.add_entity(Entity(id="keyla",properties={"generation":"millennial"}))
db.add_entity(Entity(id="noel",properties={"generation":"genz"}))
db.add_entity(Entity(id="clara",properties={"generation":"genz"}))

db.add_entity(Entity(id="coldplay"))
db.add_entity(Entity(id="u2"))
db.add_entity(Entity(id="oasis"))
db.add_entity(Entity(id="muse"))

db.add_relationship("fernando", "likes", "coldplay")
db.add_relationship("keyla", "likes", "coldplay")
db.add_relationship("keyla", "likes", "u2")
db.add_relationship("noel", "likes", "u2")
db.add_relationship("noel", "likes", "oasis")
db.add_relationship("clara", "likes", "muse")

db.add_relationship("coldplay", "is_liked_by", "fernando")
db.add_relationship("coldplay", "is_liked_by", "keyla")
db.add_relationship("u2", "is_liked_by", "keyla")
db.add_relationship("u2", "is_liked_by", "noel")
db.add_relationship("oasis", "is_liked_by", "noel")
db.add_relationship("muse", "is_liked_by", "clara")


@app.post("/entities")
async def add_entity(entity: Entity) -> bool:
    return db.add_entity(entity)


@app.post("/entities/{source_id}/{link}/{target_id}")
async def add_relationship(source_id: str, link: str, target_id: str) -> bool:
    return db.add_relationship(source_id, link, target_id)


@app.post("/entities/{id}/recommend")
async def recommend(id: str, links: List[str]) -> List[str]:
    acc = []
    db.recommendations(id, [], 0, links, acc)
    return acc


@app.post("/entities/search")
async def search(criteria: Dict[str, str]) -> List[Entity]:
    return db.search(criteria)
