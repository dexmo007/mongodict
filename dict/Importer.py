from typing import Generator
from typing import Any

from pymongo import MongoClient

from dict.DictEntry import DictEntry


class Importer:
    DEFAULT_BUFFER_SIZE = 1024

    def __init__(self, host: str = 'localhost', port: int = 27017):
        self.client = MongoClient(host, port)
        self.db = self.client.dict

    def clean(self):
        result = self.db.deen.delete_many({})
        return result.deleted_count

    def import_all(self, dict_entries: Generator[DictEntry, Any, None], buffer_size: int = DEFAULT_BUFFER_SIZE):
        # todo check buffer size
        buffer = []
        for dict_entry in dict_entries:
            buffer.append(dict_entry)
            if len(buffer) >= buffer_size:
                self.db.deen.insert_many(buffer)
                buffer = []
        self.db.deen.insert_many(buffer)

    def import_entry(self, dict_entry: DictEntry):
        self.db.deen.insert_one(dict_entry.__dict__)
