import html
import re

from dict.DictEntry import DictEntry, Gender, EntryKind

gender_regex = re.compile(r'.* {([a-z]+)}.*')  # todo extract using this regex and replace with ''


def parse_infos(entry: str):
    i = entry.find('[')
    if i == -1:
        return entry, []

    def strip_suffix(s: str):
        return re.sub(r'][ ]?', '', s)

    infos = map(strip_suffix, entry[i:].split('[')[1:])
    return entry[:i].strip(), list(infos)


def count_entries(file: str):
    i = 0
    with open(file, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if (not line) | line.startswith('#'):  # skip empty or comment lines
                continue
            i += 1
    return i


# todo as bit flag and extension map flag -> desc
def parse_entry_kinds(kinds: []):
    if len(kinds) == 0:
        return
    for kind in re.split(r'[ ]|/', kinds[0]):
        split = kind.split(':')
        if len(split) == 2:
            desc = split[0].lower().replace('.', '')
            kind = split[1].lower().replace('.', '')
            yield {
                'kind': EntryKind(kind).name,
                'desc': desc
            }
        else:
            kind = split[0].lower().replace('.', '')
            # work around the bugs
            if kind == 'nounnoun':
                kind = 'noun'
            if (kind == '[none]') | (kind == '[none][none]'):
                continue
            yield {
                'kind': EntryKind(kind).name
            }


def read(file: str):
    with open(file, encoding='utf-8') as f:
        for line in f:
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

                dict_entry.entry_kinds = list(parse_entry_kinds(kind))

                if EntryKind.NOUN.name in dict_entry.entry_kinds:
                    match = gender_regex.match(de)
                    if match:
                        gender = match.group(1)
                        de = re.sub(r' {[a-z]+}', '', de)
                        dict_entry.gender = Gender(gender).name

                de_entry, de_infos = parse_infos(de)
                en_entry, en_infos = parse_infos(en)
                dict_entry.de = html.unescape(de_entry)
                dict_entry.de_infos = de_infos
                dict_entry.en = html.unescape(en_entry)
                dict_entry.en_infos = en_infos

                # print(line)
                yield dict_entry
            except Exception:
                print(line)
