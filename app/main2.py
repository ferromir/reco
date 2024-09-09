# from fastapi import FastAPI
# from typing import Dict
# from pydantic import BaseModel
# import threading


# class Entity(BaseModel):
#     name: str
#     properties: Dict[str, str]


# class Relationship(BaseModel):
#     name: str
#     source: str
#     target: str


# app = FastAPI()
# entities = []
# relationships = []
# graph = {}


# @app.post("/entities/")
# async def add_entity(entity: Entity):
#     entities.append(entity)
#     graph[entity.name] = {}
#     return entity


# @app.post("/entities/search")
# async def search_entities(properties: Dict[str, str]):
#     if not properties:
#         return entities
#     found = []
#     for key in properties:
#         for entity in entities:
#             if key in entity.properties:
#                 if entity.properties[key] == properties[key]:
#                     found.append(entity)
#     return found


# @app.post("/relationships/")
# async def add_relationship(relationship: Relationship):
#     relationships.append(relationship)
#     if not relationship.source in graph:
#         graph[relationship.source] = {}
#     if not relationship.name in graph[relationship.source]:
#         graph[relationship.source][relationship.name] = []
    

#     return relationship
 

# @app.post("/recommendations")
# async def find_recommendations(relationship: Relationship):
#     relationships.append(relationship)
#     return relationship