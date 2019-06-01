#!/usr/bin/env python
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
        self.__cache.pop(entity_id, None)

    """
    Returns entity by the given id or `None` if nothing was found.
    """
    def find_by_id(self, entity_id):
        return self.__cache.get(entity_id)

    def __load_cache(self):
        with open(self.__file_path, 'r') as json_file:
            self.__cache = {
                entity_id: self.__entity_cls(entity_dict) for (entity_id, entity_dict) in simplejson.load(json_file).items()
            }

    def __store_cache(self):
        with open(self.__file_path, 'w') as json_file:
            simplejson.dump(self.__cache, json_file, indent=4, for_json=True)
            # json.dump(self.__create_json_from_cache(), json_file, indent=4)

