from Information import Information

class Inserter:
    def __init__(self, kind='csv', filepath: str=None):
        self.kind = kind
        if filepath is not None:
            self.filepath = filepath

    @staticmethod
    def _save_as_csv(informations, filepath):
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(", ".join(Information.dimensions))
            for info in informations:
                file.write("\n" + info.print())

    def save(self, informations):
        if self.kind == 'csv':
            self._save_as_csv(informations, self.filepath)
