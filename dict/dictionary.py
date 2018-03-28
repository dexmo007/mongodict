import json
import os


def load_words_dict(lang: str):
    filename = os.path.join(os.getcwd(), 'resources', lang, "words.json")
    with open(filename, "r") as english_dictionary:
        valid_words = json.load(english_dictionary)
        return valid_words


def load_words_set(lang: str):
    dictionary = load_words_dict(lang)
    words = set()
    for word in dictionary:
        words.add(word)
    return words


def load_words_dict_full(input_file: str):
    words = {}
    with open(input_file) as f:
        for line in f:
            line = line.strip().lower()
            if line.isdigit():
                continue
            words[line] = 1
    return words


def create_abbreviations_dict(input_file: str):
    abbreviations = {}
    with open(input_file) as f:
        for line in f:
            line = line.strip().replace('"', '')
            key, *values = line.split(',')
            if key == '' or len(values) == 0 or values == ['']:
                continue
            key = key.lower()
            abbreviations.setdefault(key, []).extend(values)
    return abbreviations


def create_abbreviations_json(input_file: str):
    abbreviations = {}
    with open(input_file) as f:
        for line in f:
            line = line.strip()
            key, *values = line.split(',')
            if key == '' or len(values) == 0 or values == ['']:
                continue
            abbreviations[key.lower()] = 1
    return abbreviations


def create_abbreviations_set(input_file: str):
    abbreviations = set()
    with open(input_file) as f:
        for line in f:
            line = line.strip()
            key, *values = line.split(',')
            if key == '' or len(values) == 0 or values == ['']:
                continue
            abbreviations.add(key.lower())
    return abbreviations


def main():
    # d = load_words_dict('en')
    # s = load_words_set('en')
    # import sys
    # print('Entries', len(d), 'Size', sys.getsizeof(d))
    # print(sys.getsizeof(d) - 4 * len(d))
    # print('Entries', len(s), 'Size', sys.getsizeof(s))
    root = os.getenv('DATA_ROOT')
    file = 'oed-abbreviations.csv'
    file_path = os.path.join(root, file)
    abbrs = create_abbreviations_json(file_path)
    out_path = os.path.join(root, 'abbr-keys.json')
    with open(out_path, 'w') as out:
        json.dump(abbrs, out)


if __name__ == '__main__':
    main()
