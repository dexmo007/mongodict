from dict import Reader
from dict.Importer import Importer
import time
from datetime import datetime

if __name__ == '__main__':
    importer = Importer()
    clean_count = importer.clean()
    print('Cleaned up entries: ', clean_count)
    print('Entries: ', Reader.count_entries())
    count = 0
    start_time = datetime.now()
    for dict_entry in Reader.read():
        importer.import_entry(dict_entry)
        count += 1
    elapsed_time = datetime.now() - start_time
    print('Processed', count, 'entries', 'in', str(elapsed_time))
