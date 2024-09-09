from fastapi import FastAPI
from typing import Dict, Set, List
from pydantic import BaseModel


class EntityDto(BaseModel):
    id: str
    properties: Dict[str, str]


class RelationshipDto(BaseModel):
    source_id: str
    link: str
    target_id: str
    

class Database:
    def __init__(self):
        self.graph = {
            "fernando": {
                "likes": ["coldplay"]
            },
            "keyla": {
                "likes": ["coldplay", "u2"]
            },
            "noel": {
                "likes": ["u2", "oasis"]
            },
            "clara": {
                "likes": ["muse"]
            },
            "coldplay": {
                "is_liked_by": ["fernando", "keyla"]
            },
            "u2": {
                "is_liked_by": ["keyla", "noel"]
            },
            "oasis": {
                "is_liked_by": ["noel"]
            },
            "muse": {
                "is_liked_by": ["clara"]
            }
        }
        # self.entities = {}
        # self.relationships = {}

    # def add_entity(self, id, properties):
    #     self.entities[id] = properties
    #     if not id in self.graph:
    #         self.graph[id] = []

    # def add_relationship(self, source_id, link, target_id):
    #     if source_id in self.graph and target_id in self.graph:
    #         id = source_id + "->" + target_id
    #         if not id in self.relationships:
    #             self.relationships[id] = []
    #         if not link in self.relationships[id]:
    #             self.relationships[id].append(link)
    #         if not target_id in self.graph[source_id]:
    #             self.graph[source_id].append(target_id)

    def search(self, source_id, visited, depth, links, acc):
        if source_id in visited:
            return
        visited.append(source_id)
        if depth < len(links):
            link = links[depth]
            if link in self.graph[source_id]:
                for target_id in self.graph[source_id][link]:
                    if target_id not in visited:
                        if depth == len(links) - 1:
                            print(target_id)
                            if target_id not in acc:
                                acc.append(target_id)
                        else:
                            self.search(target_id, visited, depth + 1, links, acc)
        
    
    # def add_relationship(self, source_id, target_id, link, properties):
    #     if not source_id in self.entities:
    #         return

    #     if not target_id in self.entities:
    #         return

    #     id = source_id + "->" + link + "->" + target_id

    #     if id in self.relationships:
    #         return

    #     self.relationships[id] = properties
    #     graph[source_id].append(target_id)


app = FastAPI()
db = Database()


@app.post("/entities/bulk")
async def add_entities(entities: List[EntityDto]):
    for entity in entities:
        db.add_entity(entity.id, entity.properties)
    print(db.graph)
    print(db.entities)
    print(db.relationships)
    return db.graph


@app.post("/relationships/bulk")
async def add_relationships(relationships: List[RelationshipDto]):
    for rel in relationships:
        db.add_relationship(rel.source_id, rel.link, rel.target_id)
    print(db.graph)
    print(db.entities)
    print(db.relationships)
    return db.graph



@app.post("/entities/{id}/recommend")
async def recommend(id: str, links: List[str]):
    acc = []
    db.search(id, [], 0, links, acc)
    return acc



# graph = {
#     "fernando": ["coldplay"],
#     "coldplay": ["fernando", "keyla"],
#     "keyla": ["coldplay", "u2"],
#     "u2": ["keyla", "noel"],
#     "noel": ["u2", "oasis"],
#     "oasis": ["noel"],
#     "clara": ["muse"]
# }

# visited = []

# def traverse(source):
#     if source in visited:
#         return
#     visited.append(source)
#     for target in graph[source]:
#         if target not in visited:
#             traverse(target)

# traverse("fernao")

# print(visited)
