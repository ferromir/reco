from typing import Dict, List
from pydantic import BaseModel
import sys


class Entity(BaseModel):
    id: str
    properties: Dict[str, str] = {}
    relationships: Dict[str, List[str]] = {}

    def matches(self, properties):
        return { **self.properties, **properties } == self.properties
    

class Database:
    def __init__(self):
        self.entities = {}
        self.indexes = {}

    def add_entity(self, entity):
        if not entity.id in self.entities:
            self.entities[entity.id] = entity
            for k in entity.properties:
                if not k in self.indexes:
                    self.indexes[k] = {}
                v = entity.properties[k]
                if not v in self.indexes[k]:
                    self.indexes[k][v] = []
                self.indexes[k][v].append(entity)
            return True
        return False

    def add_relationship(self, source_id, link, target_id):
        if source_id in self.entities and target_id in self.entities:
            if not link in self.entities[source_id].relationships:
                self.entities[source_id].relationships[link] = []
            if not target_id in self.entities[source_id].relationships[link]:
                self.entities[source_id].relationships[link].append(target_id)
            return True
        return False

    def search(self, criteria):
        bucket = None
        n = sys.maxsize
        for k in criteria:
            if k in self.indexes:
                v = criteria[k]
                if v in self.indexes[k]:
                    b = self.indexes[k][v]
                    if len(b) < n:
                        bucket = b
                        n = len(b)
        result = []
        if bucket:
            for entity in bucket:
                if entity.matches(criteria):
                    result.append(entity)
        return result

    def recommendations(self, source_id, visited, depth, links, acc):
        if source_id in visited or (not source_id in self.entities):
            return
        visited.append(source_id)
        if depth < len(links):
            link = links[depth]
            if link in self.entities[source_id].relationships:
                for target_id in self.entities[source_id].relationships[link]:
                    if target_id not in visited:
                        if depth == len(links) - 1:
                            if target_id not in acc:
                                acc.append(target_id)
                        else:
                            self.recommendations(target_id, visited, depth + 1, links, acc)