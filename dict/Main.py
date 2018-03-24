import getopt
import sys
from datetime import datetime

from dict import Reader
from dict.Importer import Importer


def run(input_file: str, clean: bool):
    importer = Importer()
    if clean:
        clean_count = importer.clean()
        print('Cleaned up entries: ', clean_count)

    print('Entries: ', Reader.count_entries(input_file))
    count = 0
    start_time = datetime.now()
    for dict_entry in Reader.read(input_file):
        importer.import_entry(dict_entry)
        count += 1
    elapsed_time = datetime.now() - start_time
    print('Processed', count, 'entries', 'in', str(elapsed_time))


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:c", ["help", "input=", "clean"])
    except getopt.GetoptError:
        print('Invalid args')
        sys.exit(2)

    input_file = None
    clean = False
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print('HELP ME')
            sys.exit()
        elif opt in ('-i', '--input'):
            input_file = arg
        elif opt in ('-c', '--clean'):
            clean = True
    if not input_file:
        print('No input file specified')
        sys.exit(2)
    print('Input', input_file)
    print('Clean', clean)
    run(input_file, clean)


if __name__ == '__main__':
    main()
