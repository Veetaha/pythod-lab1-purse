#!/usr/bin/env python
import signal
import os
import json


class JsonFileStorage:
    def __init__(self, file_path, entity_cls):
        self.file_path = file_path
        self.entity_cls = entity_cls

        if os.path.isfile(file_path):
            self.load_cache()
        else:
            self.cache: dict[str, object] = {}
            self.store_cache()

        signal.signal(signal.SIGINT, lambda signals, frame_type: self.store_cache())

    def get_all(self): return self.cache

    def serialize(self, entity): json.dumps(entity)

    def insert(self, entity):
        self.cache[entity.get_id()] = entity

    def delete(self, entity_id):
        self.cache.pop(entity_id, None)

    def get(self, entity_id):
        return self.cache.get(entity_id)

    def load_cache(self):
        with open(self.file_path, 'r') as json_file:
            self.cache = {entity_id: self.entity_cls(**entity_dict) for entity_id, entity_dict in json.load(json_file)}

    def create_json_from_cache(self):
        return {k: v.__dict__ for k, v in self.cache.items()}

    def store_cache(self):
        with open(self.file_path, 'w') as json_file:
            json.dump(self.create_json_from_cache(), json_file, indent=4)

