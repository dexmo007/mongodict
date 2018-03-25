from enum import IntFlag
from pprint import pprint

from dict.DictEntry import EntryKind, Gender


def multidict_put(multidict: {}, key, value):
    multidict[key] = multidict.get(key, 0) | value


def parse_words(entry: str):
    words = []
    genders = {}
    gender_ext = {}
    infos = {}
    offset = 0
    split = entry.split(' ')
    i = 0
    while i < len(split):
        word = split[i]
        if word.startswith('[{'):
            gender = Gender.parse(word[2:len(word) - 1])
            multidict_put(genders, i - offset, gender)
            offset += 1
            i += 1
            ext = split[i]
            if ext.startswith('{'):
                multidict_put(genders, i - offset, Gender.parse(ext[1:len(word) - 1]))
            else:
                gender_ext[i - offset] = {gender.value: ext[:len(ext) - 1]}
            offset += 1
        elif word.startswith('{'):
            multidict_put(genders, i - offset, Gender.parse(word[1:len(word) - 1]))
            offset += 1
        elif word.startswith('['):
            infos[i - offset] = word[1:len(word) - 1]
            offset += 1
        else:
            words.append(word)
        i += 1

    return words, {'genders': genders, 'gender_ext': gender_ext, 'infos': infos}


def main():
    words, info = parse_words('Jig {f} [{m} selten] [Tanz]')
    print(words)
    print(info)


if __name__ == '__main__':
    main()
