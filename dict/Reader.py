import html
import re

from dict.DictEntry import DictEntry, Gender, EntryKind
from dict.string_utils import split2

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
    return entry_kinds, ext


def parse_words(entry: str):
    words = ''
    genders = {}

    def add_gender(key, value):
        genders[str(key)] = genders.get(str(key), 0) | value

    gender_ext = {}
    infos = {}

    def add_info(key, value):
        infos[str(key)] = infos.get(key, []).append(value)

    offset = 1
    split = entry.split(' ')
    i = 0
    while i < len(split):
        word = split[i]
        if word.startswith('[{'):
            if word.endswith('}]'):
                end_index = len(word) - 2
                gender = Gender.parse(word[2:end_index])
                add_gender(i - offset, gender)
                offset += 1
            else:
                end_index = len(word) - 1
                gender = Gender.parse(word[2:end_index])
                add_gender(i - offset, gender)
                offset += 1
                i += 1
                ext = split[i]
                if ext.startswith('{'):
                    add_gender(i - offset, Gender.parse(ext[1:len(word) - 1]))
                else:
                    gender_ext[i - offset] = {gender.value: ext[:len(ext) - 1]}
                offset += 1
        elif word.startswith('{'):
            close_index = word.rfind('}')
            if close_index != -1:
                add_gender(i - offset, Gender.parse(word[1:close_index]))  # todo append remainder to words
                offset += 1
            else:
                j = 1
                close_index = split[i + j].rfind('}')
                while close_index == -1:
                    j += 1
                    close_index = split[i + j].rfind('}')
                info = ' '.join(split[i:i + j + 1])
                add_info(i - offset, info[1:len(info) - 1])
        elif word.startswith('['):
            close_index = word.rfind(']')
            if close_index != -1:
                add_info(i - offset, word[1:close_index])
                offset += 1
                words += word[close_index:len(word)]
            else:
                j = 1
                close_index = split[i + j].rfind(']')
                while close_index == -1:
                    j += 1
                    close_index = split[i + j].rfind(']')
                info = ' '.join(split[i:i + j + 1])
                add_info(i - offset, info[1:len(info) - 1])
                offset += 1 + j
                i += j
        else:
            words += ' ' + word
        i += 1

    info = {}
    if len(genders) > 0:
        info['genders'] = genders
    if len(gender_ext) > 0:
        info['gender_ext'] = gender_ext
    if len(infos) > 0:
        info['infos'] = infos
    return words[1:], info


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

                entry_kinds, entry_kind_ext = parse_entry_kinds(kind)
                dict_entry.entry_kinds = entry_kinds.value
                if len(entry_kind_ext) > 0:
                    dict_entry.entry_kind_ext = entry_kind_ext

                # if EntryKind.NOUN & entry_kinds:
                #     match = gender_regex.match(de)
                #     if match:
                #         if de.count('[{') >= 1:
                #             print(line)
                #         gender = match.group(1)
                #         de = re.sub(r' {[a-z]+}', '', de)  # todo multiple genders: [{} {}] and gender of multiple words
                #         # todo gender in the english version
                #         dict_entry.gender = Gender(gender).name
                #
                # de_entry, de_infos = parse_infos(de)
                # en_entry, en_infos = parse_infos(en)
                # dict_entry.de = html.unescape(de_entry)
                # if len(de_infos) > 0:
                #     dict_entry.de_infos = de_infos
                # dict_entry.en = html.unescape(en_entry)
                # if len(en_infos) > 0:
                #     dict_entry.en_infos = en_infos

                de_words, de_infos = parse_words(de)
                dict_entry.de = html.unescape(de_words)
                if len(de_infos) > 0:
                    dict_entry.de_infos = de_infos
                en_words, en_infos = parse_words(en)
                dict_entry.en = html.unescape(en_words)
                if len(en_infos) > 0:
                    dict_entry.en_infos = en_infos

                # print(line)
                yield dict_entry
            except Exception as e:
                print(line, e)
