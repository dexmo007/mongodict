import re

from dict.DictEntry import Gender

from dict.Reader import parse_entry_kinds

if __name__ == '__main__':
    print(list(parse_entry_kinds([])))
    print(list(parse_entry_kinds(['archaic.:adv. adj.'])))
