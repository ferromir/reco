from fastapi import FastAPI
from typing import Dict
from pydantic import BaseModel
import threading
import sys


class EntityData(BaseModel):
    properties: Dict[str, str]


class Entity(BaseModel):
    id: str
    properties: Dict[str, str]


class RelationshipData(BaseModel):
    relation: str
    source_id: str
    target_id: str


class Relationship(BaseModel):
    id: str
    relation: str
    source_id: str
    target_id: str


app = FastAPI()
lock = threading.Lock()
ent_counter = 0
rel_counter = 0
entities = {}
relationships = []
graph = {}
indexes = {}


@app.post("/entities/")
async def add_entity(data: EntityData):
    global ent_counter

    with lock:
        id = str(ent_counter)
        entity = Entity(id=id, properties=data.properties)
        ent_counter += 1
        entities[id] = entity

        graph[id] = {}

        for k in entity.properties:
            if not k in indexes:
                indexes[k] = {}
            v = entity.properties[k]
            if not v in indexes[k]:
                indexes[k][v] = set()
            indexes[k][v].add(id)

    print(entities)
    print(graph)
    print(indexes)

    return entity


@app.post("/relationships/")
async def add_relationship(data: RelationshipData):
    global rel_counter

    if not data.source_id in graph:
        raise HTTPException(status_code=404, detail="Source not found")
    if not data.target_id in graph:
        raise HTTPException(status_code=404, detail="Target not found")

    with lock:
        id = str(rel_counter)
        relationship = Relationship(id=id, relation=data.relation, source_id=data.source_id, target_id=data.target_id)
        rel_counter += 1
        relationships[id] = relationship

        if not relationship.relation in graph[relationship.source_id]:
            graph[relationship.source_id][relationship.relation] = set()
        graph[relationship.source_id][relationship.relation].add(relationship.target_id)

    return entity


@app.post("/entities/search")
async def search_entities(criteria: Dict[str, str]):
    n = sys.maxsize
    bucket = []
    results = []
    for k in criteria:
        if not k in indexes:
            continue
        v = criteria[k]
        if not v in indexes[k]:
            continue
        if len(indexes[k][v]) < n:
            n = len(indexes[k][v])
            bucket = indexes[k][v]
    for id in bucket:
        entity = entities[id]
        if { **entity.properties, **criteria } == entity.properties:
            results.append(entity)
    return results


# @app.post("/relationships/")
# async def add_relation(criteria: Dict[str, str]):
