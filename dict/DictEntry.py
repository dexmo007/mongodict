import json
from enum import Enum


class InvalidLine(Exception):
    def __init__(self):
        pass


class EntryKind(Enum):
    UNDEFINED = ''
    NOUN = 'noun'
    VERB = 'verb'
    ADVERB = 'adv'
    ADJECTIVE = 'adj'
    PAST_PARTICIPLE = 'past-p'
    PRESENT_PARTICIPLE = 'pres-p'
    PREPOSITION = 'prep'
    CONJUNCTION = 'conj'
    PRONOUN = 'pron'
    PREFIX = 'prefix'
    SUFFIX = 'suffix'

    @staticmethod
    def map(values: []):
        def _map():
            for v in values:
                yield EntryKind(v)

        return list(_map())

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class DictEntry:

    def json(self):
        return json.dumps(self.__dict__)


class Gender(Enum):
    MALE = 'm'
    FEMALE = 'f'
    NEUTRAL = 'n'
    PLURAL = 'pl'

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name
