from csv_io import *
from pathlib import Path


class CSVData:
    def __init__(self, file_name: str):
        self.path = Path(file_name)
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
