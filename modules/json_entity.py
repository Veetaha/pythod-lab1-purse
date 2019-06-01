from uuid import uuid4

from schema import Schema, Optional

from modules.json_file_storage import JsonFileStorage


def JsonEntity(file_path: str, data_schema: dict):
    data_schema[Optional('id')] = str
    schema = Schema(data_schema)

    def entity_decorator(entity_cls):
        class Entity(entity_cls):
            def __init__(self, json):
                schema.validate(json)

                super().__init__(json)
                if 'id' in json and type(json['id']) == 'str':
                    self.id = json['id']
                else:
                    self.id = str(uuid4())

            def for_json(self): return self.__dict__

            @staticmethod
            def get_storage(): return storage

            @staticmethod
            def get_schema(): return schema

        storage = JsonFileStorage(file_path, Entity)
        return Entity
    return entity_decorator
