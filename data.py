from csv_io import *


class Data:
    def __init__(self, file_name: str):
        self.csv: list[dict] = csv_as_dict_list(file_name)

    def __iter__(self):
        for entry in self.csv:
            yield entry

    def count(self):
        return len(self.csv)
