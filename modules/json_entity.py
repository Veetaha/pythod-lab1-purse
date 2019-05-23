from modules.identifiable import Identifiable
from modules.json_file_storage import JsonFileStorage


def JsonEntity(file_path: str):

    class BaseEntity(Identifiable):

        def __init__(self): super().__init__()

        @staticmethod
        def find_by_id(entity_id): return storage.get(entity_id)

        @staticmethod
        def delete_by_id(entity_id): return storage.delete(entity_id)

        @staticmethod
        def get_all():
            return storage.get_all()

        def save(self):
            storage.insert(self)
            return self

        def delete(self):
            return storage.delete(self.get_id())

        def to_json(self): return storage.serialize(self)

    storage = JsonFileStorage(file_path, BaseEntity)

    return BaseEntity
