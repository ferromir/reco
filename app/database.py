from typing import Dict, List
from pydantic import BaseModel


class Entity(BaseModel):
    id: str
    props: Dict[str, str]
    rels: Dict[str, List[str]] = {}

    def matches(self, props: Dict[str, str]) -> bool:
        return {**self.props, **props} == self.props

    def add_rel(self, link: str, target_id: str) -> None:
        if not link in self.rels:
            self.rels[link] = []
        if not target_id in self.rels[link]:
            self.rels[link].append(target_id)


class Db:
    def __init__(self, index_size: int, index_keys: List[str]) -> None:
        self.entities: List[Entity] = []
        self.primary: Dict[str, Entity] = {}
        self.secondary: Dict[str, Dict[str, List[Entity]]] = {}
        self.index_size = index_size
        for key in index_keys:
            self.secondary[key] = [[] for _ in range(index_size)]

    def has_entity(self, id: str) -> bool:
        return id in self.primary

    def add_entity(self, entity: Entity) -> None:
        self.entities.append(entity)
        self.primary[entity.id] = entity
        for k in entity.props:
            if k in self.secondary:
                v = entity.props[k]
                h = hash(v) % self.index_size
                self.secondary[k][h].append(entity)

    def search(self, props: Dict[str, str]) -> List[Entity]:
        search_bucket = self.entities
        for k in props:
            if k in self.secondary:
                v = props[k]
                h = hash(v) % self.index_size
                bucket = self.secondary[k][h]
                if len(bucket) < len(search_bucket):
                    search_bucket = bucket
        return filter(lambda e: e.matches(props), search_bucket)

    def add_rel(self, source_id: str, link: str, target_id: str) -> None:
        source = self.primary[source_id]
        source.add_rel(link, target_id)

    def recommendations(self, source_id: str, visited: List[str], depth: int, links: List[str], acc: List[Entity]):
        if not source_id in self.primary:
            return
        if source_id in visited:
            return
        visited.append(source_id)
        source = self.primary[source_id]
        if depth < len(links):
            link = links[depth]
            if link in source.rels:
                for target_id in source.rels[link]:
                    if target_id not in visited:
                        if depth == len(links) - 1:
                            if target_id not in acc:
                                acc.append(self.primary[target_id])
                        else:
                            self.recommendations(target_id, visited, depth + 1, links, acc)