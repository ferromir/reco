# from fastapi import FastAPI, HTTPException
# from typing import Dict, Set, List
# from pydantic import BaseModel
# import sys
# import threading


# class Entity(BaseModel):
#     id: str
#     properties: Dict[str, str]
#     _relationships: Dict[str, Set[str]] = {}

#     def matches(self, properties: Dict[str, str]):
#         return { **self.properties, **properties } == self.properties


# class Relationship(BaseModel):
#     relation: str
#     source_id: str
#     target_id: str


# class Query(BaseModel):
#     relation: str
#     properties: Dict[str, str]


# app = FastAPI()
# entity_table = []
# primary_index = {}
# secondary_indexes = {}
# lock = threading.Lock()
# num_of_buckets = 10


# @app.post("/entities/bulk")
# async def add_entities(entities: List[Entity]):
#     with lock:
#         for entity in entities:
#             if entity.id in primary_index:
#                 raise HTTPException(status_code=400, detail="Entity already exists")
#             entity_table.append(entity)
#             table_i = len(entity_table) - 1
#             primary_index[entity.id] = table_i
#             for k in entity.properties:
#                 if not k in secondary_indexes:
#                     secondary_indexes[k] = [set() for i in range(num_of_buckets)]
#                 v = entity.properties[k]
#                 bucket_i = hash(v) % num_of_buckets
#                 secondary_indexes[k][bucket_i].add(table_i)
#     return entities


# @app.post("/entities/search")
# async def search_entities(criteria: Dict[str, str]):
#     if not criteria:
#         return entity_table
#     bucket = None
#     n = sys.maxsize
#     for k in criteria:
#         if k in secondary_indexes:
#             v = criteria[k]
#             i = hash(v) % num_of_buckets
#             b = secondary_indexes[k][i]
#             if len(b) < n:
#                 bucket = b
#                 n = len(b)
#     result = []
#     if bucket:
#         for i in bucket:
#             entity = entity_table[i]
#             if entity.matches(criteria):
#                 result.append(entity)
#     return result


# @app.post("/relationships/bulk")
# async def add_relationships(relationships: List[Relationship]):
#     for r in relationships:
#         if not r.source_id in primary_index:
#             raise HTTPException(status_code=404, detail="Source not found")
#         if not r.target_id in primary_index:
#             raise HTTPException(status_code=404, detail="Target not found")
#         i = primary_index[r.source_id]
#         entity = entity_table[i]
#         if not r.relation in entity._relationships:
#             entity._relationships[r.relation] = set()
#         entity._relationships[r.relation].add(r.target_id)
#     return relationships


# @app.post("/entities/{id}/recommend")
# async def recommend_entities(id: str, query: Query):
#     ids = set()
#     if not id in primary_index:
#         raise HTTPException(status_code=404, detail="Entity not found")
#     entity = entity_table[primary_index[id]]
#     if query.relation in entity._relationships:
#         for target_id in entity._relationships[query.relation]:
#             target = entity_table[primary_index[target_id]]

