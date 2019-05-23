from modules.config import data_dir
from modules.json_entity import JsonEntity


class Purse(JsonEntity(f'{data_dir}/purse.json')):
    def __init__(self, total=0, ccy='UAH'):
        super().__init__()
        self.ccy = ccy
        self.total = total

