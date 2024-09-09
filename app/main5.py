from fastapi import FastAPI, HTTPException
from typing import Dict, Set, List
from pydantic import BaseModel
import sys


app = FastAPI()
entities = []
primary = {}
secondary = {}
graph = {}


class Entity(BaseModel):
    id: str
    properties: Dict[str, str]
    relationships: Dict[str, Set[Entity]] = {}

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)
    
    def __str__(self):
        return self.id

    def matches(self, properties: Dict[str, str]):
        return { **self.properties, **properties } == self.properties


class Relationship(BaseModel):
    relation: str
    source_id: str
    target_id: str


class Step(BaseModel):
    relation: str
    properties: Dict[str, str]


@app.post("/entities/bulk")
async def add_entities(bulk: List[Entity]):
    for entity in bulk:
        if entity.id in primary:
            raise HTTPException(status_code=400, detail="Entity already exists")
        entities.append(entity)
        primary[entity.id] = entity
        for k in entity.properties:
            if not k in secondary:
                secondary[k] = [set() for i in range(10)] 
            v = entity.properties[k]
            i = hash(v) % 10
            secondary[k][i].add(entity)
        graph[entity.id] = entity.relationships
    return entities


@app.post("/entities/search")
async def search_entities(criteria: Dict[str, str]):
    if not criteria:
        return entities
    bucket = None
    n = sys.maxsize
    for k in criteria:
        if k in secondary:
            v = criteria[k]
            i = hash(v) % 10
            b = secondary[k][i]
            if b and len(b) < n:
                bucket = b
                n = len(b)
    result = []
    if bucket:
        for entity in bucket:
            if entity.matches(criteria):
                result.append(entity)
    return result
  

@app.post("/entities/{source_id}/{relation}/{target_id}")
async def add_relationship(source_id: str, relation: str, target_id: str):
    if not source_id in primary:
        raise HTTPException(status_code=404, detail="Source not found")
    if not target_id in primary:
        raise HTTPException(status_code=404, detail="Target not found")
    entity = primary[source_id]
    if not relation in entity.relationships:
        entity.relationships[relation] = set()
    entity.relationships[relation].add(target_id)
    return entity


@app.post("/relationships/bulk")
async def add_relationship(relationships: List[Relationship]):
    for r in relationships:
        if not r.source_id in primary:
            raise HTTPException(status_code=404, detail="Source not found")
        if not r.target_id in primary:
            raise HTTPException(status_code=404, detail="Target not found")
        entity = primary[r.source_id]
        if not r.relation in entity.relationships:
            entity.relationships[relation] = set()
        entity.relationships[r.relation].add(r.target_id)
    return relationships


# @app.post("/entities/{source_id}/recommend")
# async def recommend(steps: List[Step]):
#     if not source_id in primary:
#         raise HTTPException(status_code=404, detail="Source not found")

    








# from fastapi import FastAPI, HTTPException
# from typing import Dict, Set
# from pydantic import BaseModel
# import sys


# app = FastAPI()
# counter = 0
# entities = []
# primary = {}
# secondary = {}
# graph = {}


# class Entity(BaseModel):
#     id: int = 0
#     properties: Dict[str, str] = {}
#     relationships: Dict[str, Set[int]] = {}

#     def matches(self, props: Dict[str, str]):
#         return { **self.properties, **props } == self.properties


# class Step(BaseModel):



# @app.post("/entities")
# async def add_entity(entity: Entity):
#     global counter
#     entity.id = counter
#     counter += 1
#     entities.append(entity)
#     primary[entity.id] = entity
#     for k in entity.properties:
#         if not k in secondary:
#             secondary[k] = [set() for i in range(10)] 
#         v = entity.properties[k]
#         i = hash(v) % 10
#         secondary[k][i].add(entity.id)
#     graph[entity.id] = entity.relationships
#     return entity


# @app.post("/entities/search")
# async def search_entities(criteria: Dict[str, str]):
#     if not criteria:
#         return entities
#     bucket = None
#     n = sys.maxsize
#     for k in criteria:
#         if k in secondary:
#             v = criteria[k]
#             i = hash(v) % 10
#             b = secondary[k][i]
#             if b and len(b) < n:
#                 bucket = b
#                 n = len(b)
#     result = []
#     if bucket:
#         for id in bucket:
#             entity = primary[id]
#             if entity.matches(criteria):
#                 result.append(entity)
#     return result
  

# @app.post("/entities/{source_id}/{relation}/{target_id}")
# async def add_relationship(source_id: int, relation: str, target_id: int):
#     if not source_id in primary:
#         raise HTTPException(status_code=404, detail="Source not found")
#     if not target_id in primary:
#         raise HTTPException(status_code=404, detail="Target not found")
#     entity = primary[source_id]
#     if not relation in entity.relationships:
#         entity.relationships[relation] = set()
#     entity.relationships[relation].add(target_id)
#     return entity


# @app.post("/entities/{source_id}/recommend")
# async def recommend(source_id: int, relation: str, target_id: int):
#     if not source_id in primary:
#         raise HTTPException(status_code=404, detail="Source not found")
#     if not target_id in primary:
#         raise HTTPException(status_code=404, detail="Target not found")
#     entity = primary[source_id]
#     if not relation in entity.relationships:
#         entity.relationships[relation] = set()
#     entity.relationships[relation].add(target_id)
#     return entity
