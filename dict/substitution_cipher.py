import random
import itertools
from itertools import combinations, product

from dict import string_utils
from dict.dictionary import load_words_dict, load_words_set


def create_alphabet():
    return list(map(chr, range(97, 97 + 26)))


class SubstitutionCipher:
    def __init__(self, alphabet=None):
        if alphabet:
            self.alphabet = alphabet
        else:
            alphabet = list(range(0, 26))
            random.shuffle(alphabet)
            self.alphabet = alphabet

    def _substitute(self, c: str):
        if c.isalpha():
            if c.isupper():
                a = 65
            else:
                a = 97
            return chr(self.alphabet[ord(c) - a] + a)
        else:
            return c

    def encrypt(self, phrase: str):
        return ''.join(map(self._substitute, phrase))

    def decrypt(self, phrase: str):
        def substitute(c: str):
            if c.isalpha():
                if c.isupper():
                    a = 65
                else:
                    a = 97
                return chr(self.alphabet.index(ord(c) - a) + a)
            else:
                return c

        return ''.join(map(substitute, phrase))

    @staticmethod
    def crack(phrase: str):
        dictionary = load_words_dict('en')
        words = string_utils.get_words(phrase)

        def rec_crack(i: int, j: int, l: int, a: {}) -> object:
            word = words[i]
            if j >= len(word):
                i += 1
                if i >= len(words):
                    return a
                j = 0
                word = words[i]
            c = word[j]
            if c in a:
                return rec_crack(i, j + 1, l, a)
            else:
                a[c] = chr(l)
                matches = list(
                    filter(lambda w: len(w) == len(word) and w.startswith(SubstitutionCipher(a).decrypt(word[:j + 1])),
                           dictionary))
                return rec_crack(i, j + 1, l + 1, a)

        alphabet = rec_crack(0, 0, 97, {})
        print(alphabet)
        return SubstitutionCipher(alphabet)


def crack_word(word: str):
    dictionary = load_words_set('en')

    def rec_crack_tail(i, ms, a):
        if i >= len(word):
            return a  # return first match
        c = word[i]
        if c in a:
            filtered_ms = list(filter(lambda m: m[i] == a[c], ms))
            if len(filtered_ms) == 0:
                return None
            return rec_crack_tail(i + 1, filtered_ms, a)
        else:
            return  # todo

    alphabets = []
    for l in range(97, 97 + 26):
        matches = list(filter(lambda w: len(w) == len(word) and w.startswith(chr(l)), dictionary))
        alphabet = rec_crack_tail(1, matches, {f'{word[0]}': chr(l)})
        alphabets.append(alphabet)
    return list(map(SubstitutionCipher, alphabets))


def crack_word_stupid(encrypted: str):
    dictionary = load_words_set('en')

    def try_find_alphabet(_a: {}, possibility: str):
        for j, c in enumerate(possibility):
            letter = encrypted[j]
            if letter in _a:
                if _a[letter] != c:
                    return None
            else:
                _a[letter] = c
        return _a

    alphabets = []
    encrypted_words = string_utils.get_words(encrypted)
    for word in filter(lambda w: len(w) == len(encrypted_words[0]), dictionary):
        a = try_find_alphabet({}, word)
        if a:
            alphabets.append(a)
    for e in encrypted_words[1:]:
        new_alphabets = []
        possibilities = filter(lambda w: len(w) == len(e), dictionary)
        for p in possibilities:
            for alphabet in alphabets.copy():
                alphabet = try_find_alphabet(alphabet, p)
                if alphabet:
                    new_alphabets.append(alphabet)
        alphabets = new_alphabets

    return alphabets


def main():
    cipher = SubstitutionCipher(
        [22, 11, 20, 14, 8, 15, 24, 16, 12, 6, 13, 4, 23, 2, 0, 19, 5, 10, 25, 21, 7, 3, 18, 17, 1, 9])
    print(cipher.alphabet)
    # p = 'there goes the dog in the pan crazy'
    p = 'onomatopoeia you dirty bag'
    print('Phrase:', p)
    e = cipher.encrypt(p)
    print('Encrypted:', e)
    d = cipher.decrypt(e)
    print('Decrypted:', d)
    cracked_cipher = crack_word_stupid(e)
    for c in cracked_cipher:
        print(''.join(map(c.get, e)))


if __name__ == '__main__':
    main()
