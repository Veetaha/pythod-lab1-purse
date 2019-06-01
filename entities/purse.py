from modules.json_entity import JsonEntity


@JsonEntity(
    file_path='data/purse.json',
    data_schema={
        'ccy':   str,
        'total': lambda value: float(value) >= 0
    }
)
class Purse:
    def __init__(self, json):
        self.ccy = json['ccy']
        self.total = float(json['total'])
