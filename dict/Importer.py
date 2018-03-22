from typing import Generator
from typing import Any

from pymongo import MongoClient

from dict.DictEntry import DictEntry


class Importer:
    def __init__(self, host: str = 'localhost', port: int = 27017):
        self.client = MongoClient(host, port)
        self.db = self.client.dict

    def clean(self):
        result = self.db.deen.delete_many({})
        return result.deleted_count

    def import_all(self, dict_entries: Generator[DictEntry, Any, None]):
        for dict_entry in dict_entries:
            self.db.deen.insert_one(dict_entry.__dict__)

    def import_entry(self, dict_entry: DictEntry):
        # if dict_entry.gender:
        #     dict_entry.gender = dict_entry.gender.name
        self.db.deen.insert_one(dict_entry.__dict__)
