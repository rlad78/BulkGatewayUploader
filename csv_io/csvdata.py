from .csvtools import *
from pathlib import Path


class CSVData:
    def __init__(self, file_name: str):
        self.path = Path(file_name).resolve()
        if not self.path.is_file():
            raise Exception(f'"{self.path.resolve()}" does not exist')
        self.filename = file_name
        self.csv: list[dict] = csv_as_dict_list(file_name)
        self.categories: list[str] = list(self.csv[0].keys())

    def __iter__(self):
        for entry in self.csv:
            yield entry

    def __check_categories(self, *args) -> None:
        for item in args:
            if item in self.categories:
                return None
            else:
                raise Exception(f'"{item}" not available in {self.filename}\'s categories:\n{self.categories}')

    def count(self):
        return len(self.csv)

    def find(self, category: str, match_value: str) -> dict:
        self.__check_categories(category)
        for entry in self.csv:
            if entry[category] == match_value:
                return entry
        # if not found, return empty dict
        return {}

    def findall(self, category: str, match_value: str) -> list[dict]:
        self.__check_categories(category)
        found: list[dict] = []
        for entry in self.csv:
            if entry[category == match_value]:
                found.append(entry)
        return found

    def values(self, category: str, search_category: str, match_value: str) -> list[str]:
        self.__check_categories(category, search_category)
        found: list[dict] = self.findall(search_category, match_value)
        if not found:
            return []
        else:
            return [x[category] for x in found]


class MakeCSV:
    def __init__(self):
        self.data: list[dict] = []
        self.categories: list[str] = []

    def __add_categories(self, data: dict) -> None:
        if not self.categories:  # if empty, just put in all of data's categories
            self.categories = list(data.keys()).copy()
        else:  # check for missing categories, and append any missing to all data (to retain sameness for write)
            for k in data.keys():
                if k not in self.categories:
                    self.categories.append(k)
                    for entry in self.data:
                        if k not in entry.keys():
                            entry[k] = ''

    def add(self, data: dict) -> None:
        if type(data) != dict:
            print(f"[MakeCSV | ERROR]: Tried to insert {type(data)} when {type({})} is required")
            return None
        self.__add_categories(data)

        # make sure incoming data has all categories
        for cat in self.categories:
            if cat not in data.keys():
                data[cat] = ''
        self.data.append(data)

    def write(self, file_path: str):
        path = Path(file_path).resolve()
        if not path.parent.is_dir():
            raise Exception(f'Directory "{path.parent}" does not exist')
        csv_dict_write(str(path), self.data)
