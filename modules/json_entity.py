from uuid import uuid4

from schema import Schema, Optional

from modules.json_file_storage import JsonFileStorage


def JsonEntity(file_path: str, data_schema: dict):
    data_schema[Optional('id')] = str
    upd_schema = Schema({ Optional(k): v for k, v in data_schema.items()})
    schema = Schema(data_schema)

    def entity_decorator(entity_cls):
        class Entity(entity_cls):
            """
            Creates an instance of `Entity` and validates the given `json` dictionary values.
            Throws `SchemaError` if json is not compatible with the defined `data_schema`.
            """
            def __init__(self, json):
                schema.validate(json)
                if 'id' in json and type(json['id']) == str:
                    self.id = json['id']
                else:
                    self.id = str(uuid4())

                super().__init__(json)

            """
            Method implementation required for serialization by `simplejson`. 
            """
            def for_json(self): return self.__dict__

            """
            Returns storage instance that manages entites of this type.
            """
            @staticmethod
            def get_storage(): return storage

            """
            Retuns `data_schema` that was forwarded to `@Entity()` decorator for validation._
            """
            @staticmethod
            def get_schema(): return schema

            """
            Assigns keys and values that are stored in `upd` dict to the current entity.
            Argument `upd` gets validated prior to assignment, so be read to catch a `SchemaError`.
            Key `id` must not be present in the given `upd` dict.
            """
            def update(self, upd):
                upd = { k: v for k, v in upd.items() if v is not None}
                upd_schema.validate(upd)
                self.__dict__.update(upd)
                return self

        storage = JsonFileStorage(file_path, Entity)
        return Entity
    return entity_decorator
