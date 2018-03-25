import html
import re

from dict.DictEntry import DictEntry, Gender, EntryKind
from dict.StringUtils import split2

gender_regex = re.compile(r'.* {([a-z]+)}.*')  # todo extract using this regex and replace with ''


def parse_infos(entry: str):
    i = entry.find('[')
    if i == -1:
        return entry, []

    def strip_suffix(s: str):
        return re.sub(r'][ ]?', '', s)

    infos = map(strip_suffix, entry[i:].split('[')[1:])
    return entry[:i].strip(), list(infos)


def count_entries(file_path: str):
    i = 0
    with open(file_path, encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            # skip empty or comment lines
            if (not line) | line.startswith('#'):
                continue
            # skip faulty lines
            if line == 'noun':
                continue
            i += 1
    return i


def parse_entry_kinds(kinds: []):
    def clean_kind(s: str):
        return s.lower().replace('.', '')

    if len(kinds) == 0:
        return EntryKind.UNDEFINED, {}
    entry_kinds = EntryKind.UNDEFINED
    ext = {}
    for kind in split2(kinds[0], ' ', '/'):
        split = kind.split(':')
        if len(split) == 2:  # has extension
            desc = clean_kind(split[0])
            kind = split[1].lower().replace('.', '')
            entry_kinds |= EntryKind.map(kind)
            ext[kind] = desc
        else:
            kind = split[0].lower().replace('.', '')
            # work around the bugs
            if kind == 'nounnoun':
                kind = 'noun'
            if (kind == '[none]') | (kind == '[none][none]'):
                continue
            entry_kinds |= EntryKind.map(kind)
    return entry_kinds.value, ext


def read(file_path: str):
    with open(file_path, encoding='utf-8') as file:
        for line in file:
            try:
                line = line.strip()
                # skip empty or comment lines
                if (not line) | line.startswith('#'):
                    continue
                # skip faulty lines
                if line == 'noun':
                    continue

                de, en, *kind = line.split('\t')

                dict_entry = DictEntry()

                entry_kinds, ext = parse_entry_kinds(kind)
                dict_entry.entry_kinds = entry_kinds
                if len(ext) > 0:
                    dict_entry.ext = ext

                if EntryKind.NOUN & entry_kinds:
                    match = gender_regex.match(de)
                    if match:
                        gender = match.group(1)
                        de = re.sub(r' {[a-z]+}', '', de)  # todo multiple genders: [{} {}] and gender of multiple words
                        # todo gender in the english version
                        dict_entry.gender = Gender(gender).name

                de_entry, de_infos = parse_infos(de)
                en_entry, en_infos = parse_infos(en)
                dict_entry.de = html.unescape(de_entry)
                if len(de_infos) > 0:
                    dict_entry.de_infos = de_infos
                dict_entry.en = html.unescape(en_entry)
                if len(en_infos) > 0:
                    dict_entry.en_infos = en_infos

                # print(line)
                yield dict_entry
            except Exception as e:
                print(line, e)
