import json
from enum import Enum, Flag, unique, auto, IntFlag


class InvalidLine(Exception):
    def __init__(self):
        pass


class EntryKind(Flag):
    UNDEFINED = 0
    NOUN = 1
    VERB = 2
    ADVERB = 4
    ADJECTIVE = 8
    PAST_PARTICIPLE = 16
    PRESENT_PARTICIPLE = 32
    PREPOSITION = 64
    CONJUNCTION = 128
    PRONOUN = 256
    PREFIX = 512
    SUFFIX = 1024
    NAME = 2048
    PP = 4096  # todo this is probably a participle
    RELATIVE_PRONOUN = 8192  # todo join with pron class
    ATTRIBUTE = 16384
    PREDICATE_ADJECTIVE = 32768  # todo join with adj class

    @staticmethod
    def to_int(values: []):
        res = EntryKind.UNDEFINED
        for entry_kind in values:
            res |= entry_kind
        return res

    mapping = {
        'noun': NOUN,
        'verb': VERB,
        'adv': ADVERB,
        'adj': ADJECTIVE,
        'past-p': PAST_PARTICIPLE,
        'pres-p': PRESENT_PARTICIPLE,
        'prep': PREPOSITION,
        'conj': CONJUNCTION,
        'pron': PRONOUN,
        'prefix': PREFIX,
        'suffix': SUFFIX,
        'name': NAME,
        'pp': PP,
        'rel': RELATIVE_PRONOUN,
        'attr': ATTRIBUTE,
        'pred': PREDICATE_ADJECTIVE
    }

    @staticmethod
    def map(value: str):
        return {
            'noun': EntryKind.NOUN,
            'verb': EntryKind.VERB,
            'adv': EntryKind.ADVERB,
            'adj': EntryKind.ADJECTIVE,
            'past-p': EntryKind.PAST_PARTICIPLE,
            'pres-p': EntryKind.PRESENT_PARTICIPLE,
            'prep': EntryKind.PREPOSITION,
            'conj': EntryKind.CONJUNCTION,
            'pron': EntryKind.PRONOUN,
            'prefix': EntryKind.PREFIX,
            'suffix': EntryKind.SUFFIX,
            'name': EntryKind.NAME,
            'pp': EntryKind.PP,
            'rel': EntryKind.RELATIVE_PRONOUN,
            'attr': EntryKind.ATTRIBUTE,
            'pred': EntryKind.PREDICATE_ADJECTIVE
        }[value]

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class DictEntry:

    def json(self):
        return json.dumps(self.__dict__)


class Gender(IntFlag):
    MALE = 1
    FEMALE = 2
    NEUTRAL = 4
    PLURAL = 8
    SINGULAR = 16

    @staticmethod
    def parse(value: str):
        if value.endswith('.'):
            value = value[:len(value) - 1]
        return {
            'm': Gender.MALE,
            'f': Gender.FEMALE,
            'n': Gender.NEUTRAL,
            'pl': Gender.PLURAL,
            'sg': Gender.SINGULAR
        }[value]
