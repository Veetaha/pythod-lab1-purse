#!/usr/bin/env python
from flask import make_response
import signal
import os
import simplejson



class JsonFileStorage:
    def __init__(self, file_path, entity_cls):
        self.__file_path = file_path
        self.__entity_cls = entity_cls

        if os.path.isfile(file_path):
            self.__load_cache()
        else:
            self.__cache: dict[str, object] = {}
            self.__store_cache()

        signal.signal(signal.SIGINT, lambda signals, frame_type: self.__store_cache())

    """
    Returns a dictionary that contains all the entities in the storage.
    """
    def get_all(self):
        return self.__cache

    """
    Returns json compatible dictionary representation of `entity`.
    """
    def serialize(self, json_adt): return simplejson.dumps(json_adt, indent=4, for_json=True)

    """
    Inserts `entity` to the storage cache.
    """
    def insert(self, entity):
        self.__cache[entity.id] = entity
        return entity

    """
    Deletes entity from the cache. Returns deleted entity or `None` if nothing was found.
    """
    def delete_by_id(self, entity_id):
        return self.__cache.pop(entity_id, None)

    """
    Returns entity by the given id or `None` if nothing was found.
    """
    def find_by_id(self, entity_id):
        return self.__cache.get(entity_id)

    """
    Updates entity with `upd` values for the given `entity_id`.
    """
    def update_by_id(self, entity_id, upd):
        print(entity_id)
        entity = self.find_by_id(entity_id)
        return None if entity is None else entity.update(upd)


    """
    Creates flask response that contains `entities` json representation and returns it.
    """
    def create_json_response(self, entities):
        if entities is None: return None, 404
        response = make_response(self.serialize(entities))
        response.headers['content-type'] = 'application/json'
        return response

    def __load_cache(self):
        with open(self.__file_path, 'r') as json_file:
            self.__cache = {
                entity_id: self.__entity_cls(entity_dict) for (entity_id, entity_dict) in simplejson.load(json_file).items()
            }

    def store_cache(self):
        with open(self.__file_path, 'w') as json_file:
            simplejson.dump(self.__cache, json_file, indent=4, for_json=True)
