# from fastapi import FastAPI, HTTPException
# from typing import Dict
# from pydantic import BaseModel
# import threading
# import json
# import sys


# app = FastAPI()
# graph = {}
# entityIndexes = {}


# @app.post("/entities/_search")
# async def search_entities(properties: Dict[str, str]):
#     if not properties:
#         return graph
#     results = {}
#     entityIds = set()
#     for key in properties:
#         indexKey = key + ":" + properties[key]
#         n = sys.maxsize
#         if indexKey in entityIndexes:
#             m = len(entityIndexes[indexKey])
#             if m < n:
#                 n = m
#                 entityIds = entityIndexes[indexKey]
#     for entityId in entityIds:
#         if { **graph[entityId]['properties'], **properties } == graph[entityId]['properties']:
#             results = { **results, **{ entityId: graph[entityId] } }
#     return results


# @app.post("/entities/{entityId}")
# async def add_entity(entityId: str, properties: Dict[str, str]):
#     if entityId in graph:
#         raise HTTPException(status_code=400, detail="Entity already exists")
#     graph[entityId] = { 'properties': properties, 'relationships': {} }
#     for key in properties:
#         indexKey = key + ":" + properties[key]
#         if not indexKey in entityIndexes:
#             entityIndexes[indexKey] = set()
#         entityIndexes[indexKey].add(entityId)
#     print(entityIndexes)
#     return graph


# @app.post("/entities/{sourceId}/{relation}/{targetId}")
# async def add_relationship(sourceId: str, relation: str, targetId: str, properties: Dict[str, str]):
#     if not sourceId in graph:
#         raise HTTPException(status_code=404, detail="Source not found")
#     if not targetId in graph:
#         raise HTTPException(status_code=404, detail="Target not found")
#     if not relation in graph[sourceId]:
#         graph[sourceId][relation] = {}
#     if targetId in graph[sourceId][relation]:
#         raise HTTPException(status_code=400, detail="Relationship already exists")
#     graph[sourceId][relation][targetId] = properties
#     return graph


# # @app.post("/relationships/")
# # async def add_relationship(relationship: Relationship):
# #     relationships.append(relationship)
# #     if not relationship.source in graph:
# #         graph[relationship.source] = {}
# #     if not relationship.name in graph[relationship.source]:
# #         graph[relationship.source][relationship.name] = []
    

# #     return relationship
 

# # @app.post("/recommendations")
# # async def find_recommendations(relationship: Relationship):
# #     relationships.append(relationship)
# #     return relationship