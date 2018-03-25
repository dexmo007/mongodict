from typing import Generator
from typing import Any

from pymongo import MongoClient

from dict.DictEntry import DictEntry


class Importer:
    DEFAULT_BUFFER_SIZE = 4096

    def __init__(self, host: str = 'localhost', port: int = 27017, database: str = 'dict'):
        self.client = MongoClient(host, port)
        self.db = self.client.get_database(database)
        self.collection = self.db.get_collection('de-en')
        self.last_imported = -1

    def clean(self):
        count = self.collection.count()
        self.db.drop_collection(self.collection)
        return count

    def import_all(self, dict_entries: Generator[DictEntry, Any, None], buffer_size: int = DEFAULT_BUFFER_SIZE):
        # todo check buffer size
        buffer = []
        count = 0
        for dict_entry in dict_entries:
            buffer.append(dict_entry.__dict__)
            if len(buffer) >= buffer_size:
                self.collection.insert_many(buffer)
                count += buffer_size
                buffer = []
        self.collection.insert_many(buffer)
        count += len(buffer)
        self.last_imported = count

    def import_entry(self, dict_entry: DictEntry):
        self.collection.insert_one(dict_entry.__dict__)
