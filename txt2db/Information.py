import re
from utils import parse_date


class Information(object):
    dimensions = [
        "carton",
        "page",
        "date",
        "lieu",
        "auteur",
        "images",
        "numéro",
        "disposition",
        "géographie_source",
        "espace_mentioné",
        "résumé"
    ]

    def __init__(self, arg: dict={}):
        self.data = {
            dimension: arg.get(dimension)
            for dimension in Information.dimensions 
        }
        
    def __str__(self) -> str:
        return self.print()[:100]

    def print(self) -> str:
        info = []
        for dim in Information.dimensions:
            data = self.get(dim)
            if data is None:
                data = ''
            if isinstance(data, set):
                if len(data) == 0:
                    data = ''
                data = re.sub(r'[\'\{\}]', '', str(data))
                data = re.sub(r',', ';', str(data))

            info.append(f'"{data}"')

        return ", ".join(info)

    def __getitem__(self, dimension: str):
        return self.data.__getitem__(dimension)
    
    def get(self, dimension: str, default_value: str=None):
        return self.data.get(dimension, default_value)
    
    def __setitem__(self, dimension: str, value):
        if dimension == "résumé":
            value = value.strip()
        if dimension == "date":
            value = parse_date(value)
        return self.data.__setitem__(dimension, value)