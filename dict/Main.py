from datetime import datetime

import click

from dict import Reader
from dict.Importer import Importer


@click.command()
@click.option('--input', '-i', 'input_file', type=click.Path(exists=True, dir_okay=False),
              help='Path to the dict.cc translation file')
@click.option('--clean', '-c', is_flag=True, help='Whether to clean the collection before import')
@click.option('--host', default='localhost', help='Host address of the MongoDB')
@click.option('--port', default=27017, help='MongoDB port')
@click.option('--database', default='dict', help='Database name')
def main(input_file, clean, host, port, database):
    print('Input', input_file)
    print('Clean', clean)
    print('Host', host)
    print('Port', port)
    print('DB', database)

    importer = Importer(host, port)
    if clean:
        clean_count = importer.clean()
        print('Cleaned up entries: ', clean_count)

    print('Entries: ', Reader.count_entries(input_file))
    start_time = datetime.now()
    # count = 0
    # for dict_entry in Reader.read(input_file):
    #     importer.import_entry(dict_entry)
    #     count += 1
    importer.import_all(Reader.read(input_file))
    elapsed_time = datetime.now() - start_time
    print('Processed', importer.last_imported, 'entries', 'in', str(elapsed_time))


if __name__ == '__main__':
    main()
