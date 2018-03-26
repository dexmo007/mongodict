import html

from dict.DictEntry import Gender


def find_close_index(s: str, open_c, close_c, open_index: int):
    open_count = 1
    i = open_index + 1
    while open_count != 0:
        c = s[i]
        if c == open_c:
            open_count += 1
        elif c == close_c:
            open_count -= 1
        i += 1
    return i - 1


def extract(entry: str):
    words = ''
    genders = {}

    def add_gender(key, value):
        genders[str(key)] = genders.get(str(key), 0) | value

    gender_infos = {}
    infos = {}

    def add_info(key, value):
        infos[str(key)] = infos.get(str(key), []) + [value]

    i = 0
    index = 0
    while i < len(entry):
        c = entry[i]
        if c == ' ':
            words += c
            index += 1
            i += 1
        elif c == '{':
            close_index = find_close_index(entry, c, '}', i)
            content = entry[i + 1:close_index]
            if len(content) > 2:
                # todo see if it's a gender with info: '{m: <info>}'
                add_info(index, content)
            else:
                add_gender(index, Gender.parse(content))
            i = close_index + 1
            if i < len(entry) and entry[i] == ' ':
                i += 1
        elif c == '(':
            close_index = find_close_index(entry, c, ')', i)
            words += entry[i:close_index + 1]  # todo recursive parse out gender and infos
            i = close_index + 1
        elif c == '[':
            # todo sometimes if it contains gender infos, this whole content is a gender_info
            close_index = find_close_index(entry, c, ']', i)
            content = entry[i + 1:close_index]
            add_info(index, content)
            i = close_index + 1
            if i < len(entry) and entry[i] == ' ':
                i += 1
        else:
            words += c
            i += 1
    return html.unescape(words), genders, infos


def main():
    infos = {}

    def add_info(key, value):
        ls = infos.get(str(key), [])
        ls.append(value)
        infos[str(key)] = ls

    add_info(1, 'hello')
    add_info(1, 'world')
    print(infos)
    line = 'Abluftfilter {m} [fachspr. meist {n}]	exhaust filter	noun'
    print(line)
    print('--------------------------')
    open_index = line.find('{')
    print(open_index, find_close_index(line, '{', '}', open_index))
    de, en, kind = line.split('\t')
    words, genders, infos = extract(de)
    print(words)
    print(genders)
    print(infos)
    words, genders, infos = extract(en)
    print(words)
    print(genders)
    print(infos)


if __name__ == '__main__':
    main()
