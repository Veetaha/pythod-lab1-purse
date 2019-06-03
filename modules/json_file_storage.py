#!/usr/bin/env python
from uuid import uuid4

from flask import make_response
import signal
import os
import simplejson
from schema import Optional, Schema

# doctest mocks

data_schema = {
    Optional('id'): str,
    'ccy': str,
    'total': lambda value: float(value) >= 0
}
upd_schema = Schema({Optional(k): v for k, v in data_schema.items()})
schema = Schema(data_schema)


class MockEntity:
    def __init__(self, json):
        self.ccy = json['ccy']
        self.id = json['id']
        self.total = float(json['total'])

    def for_json(self): return self.__dict__

    def update(self, upd):
        upd = {k: v for k, v in upd.items() if v is not None}
        upd_schema.validate(upd)
        self.__dict__.update(upd)
        return self
# mocks end

class JsonFileStorage:
    def __init__(self, file_path='data/mocks.json', entity_cls=MockEntity):
        self.__file_path = file_path
        self.__entity_cls = entity_cls

        if os.path.isfile(file_path):
            self.__load_cache()
        else:
            self.__cache: dict[str, object] = {}
            self.store_cache()

        signal.signal(signal.SIGINT, lambda signals, frame_type: self.store_cache())


    def get_all(self):
        """
        Returns a dictionary that contains all the entities in the storage.
        >>> mock_storage = JsonFileStorage("../data/mocks.json", MockEntity)
        >>> res = mock_storage.get_all()
        >>> len(res) >= 2
        True
        >>> res.__contains__('1')
        True
        >>> res.__contains__('2')
        True
        >>> res.__contains__('3')
        False
        """
        return self.__cache


    def serialize(self, json_adt):
        """
        Returns json compatible dictionary representation of `entity`.
        """
        return simplejson.dumps(json_adt, indent=4, for_json=True)


    def insert(self, entity):
        """
        Inserts `entity` to the storage cache.
        >>> mock_storage = JsonFileStorage("../data/mocks.json", MockEntity)
        >>> mock_storage.insert(MockEntity({"id": "19", "ccy": "UAH", "total": 1000})).id
        '19'
        >>> entities = mock_storage.get_all()
        >>> entities.__contains__('19')
        True
        """
        self.__cache[entity.id] = entity
        return entity


    def delete_by_id(self, entity_id):
        """
        Deletes entity from the cache. Returns deleted entity or `None` if nothing was found.
        >>> mock_storage = JsonFileStorage("../data/mocks.json", MockEntity)
        >>> mock_storage.insert(MockEntity({"id": "17", "ccy": "UAH", "total": 1000})).id
        '17'
        >>> entities = mock_storage.get_all()
        >>> entities.__contains__('17')
        True
        >>> mock_storage.delete_by_id('17').id
        '17'
        >>> entities = mock_storage.get_all()
        >>> entities.__contains__('17')
        False
        """
        return self.__cache.pop(entity_id, None)


    def find_by_id(self, entity_id):
        """
        Returns entity by the given id or `None` if nothing was found.
        >>> mock_storage = JsonFileStorage("../data/mocks.json", MockEntity)
        >>> mock_storage.insert(MockEntity({"id": "17", "ccy": "UAH", "total": 1000})).id == '17'
        True
        >>> mock_storage.find_by_id('17').id
        '17'
        >>> mock_storage.find_by_id('17').ccy
        'UAH'
        >>> mock_storage.find_by_id('17').total
        1000.0
        """
        return self.__cache.get(entity_id)


    def update_by_id(self, entity_id, upd):
        """
        Updates entity with `upd` values for the given `entity_id`.
        >>> mock_storage = JsonFileStorage("../data/mocks.json", MockEntity)
        >>> mock_storage.insert(MockEntity({"id": "21", "ccy": "UAH", "total": 1000})).id == '21'
        True
        >>> res = mock_storage.update_by_id('21', { "ccy": "EUR", "total": 5000})
        21
        >>> res.ccy
        'EUR'
        >>> res.total
        5000
        """
        print(entity_id)
        entity = self.find_by_id(entity_id)
        return None if entity is None else entity.update(upd)


    def create_json_response(self, entities):
        if entities is None:
            return None, 404
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