from uuid import uuid4


class Identifiable:
    def __init__(self):
        self.id = str(uuid4())

    def get_id(self): return self.id
