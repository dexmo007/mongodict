from dict.dictionary import load_words_dict
from dict.string_utils import get_words


def shift(c, offset):
    if c.isalpha():
        if c.isupper():
            a = 65
        else:
            a = 97
        return chr(a + (ord(c) - a + offset) % 26)
    else:
        return c


def ord_diff(w1: str, w2: str):
    return (ord(w2) - ord(w1)) % 26


def matches_diff(encrypted: str, word: str):
    offset = ord_diff(word[0], encrypted[0])
    decrypted = CaesarCipher(offset).decrypt(encrypted)
    return decrypted == word


class CaesarCipher:
    def __init__(self, offset: int):
        self.offset = offset

    def encrypt(self, phrase: str):
        # from array import array
        # return array('B', map(ord, map(shift, phrase))).tostring()
        #  todo if side for this variant leave out the ord(chr(..))
        return ''.join(map(lambda c: shift(c, self.offset), phrase))

    def decrypt(self, phrase: str):
        return ''.join(map(lambda c: shift(c, -self.offset), phrase))

    def _verify_cipher(self, word, words, dictionary):
        decrypted = []
        for w in words:
            d = self.decrypt(w)
            if d != word and d not in decrypted and d not in dictionary:
                return False
            decrypted.append(d)
        return True

    @staticmethod
    def find_offset(phrase: str, fast: bool = False):
        offset = 0
        words = sorted(get_words(phrase), key=lambda w: len(w), reverse=True)
        # print(words)
        dictionary = load_words_dict('en')
        print('Loaded', len(dictionary), 'words')
        current = words[0]
        valid_ciphers = []
        for word in dictionary:
            if len(word) == len(current) and matches_diff(current, word):
                cipher = CaesarCipher(ord_diff(word[0], current[0]))
                if cipher._verify_cipher(word, words[1:], dictionary):
                    if fast:
                        return cipher
                    else:
                        valid_ciphers.append(cipher)
        if fast:
            return None
        return valid_ciphers

    def __repr__(self):
        return f'{self.__class__.__name__}(offset={self.offset})'


def main():
    import os
    print(os.getenv('DATA_ROOT'))
    print('ABC'.lower())
    # print(ord('A'))
    # cipher = CaesarCipher(23)
    cipher = CaesarCipher(23)
    abc = ''.join(map(chr, range(65, 65 + 26)))
    encrypted_abc = cipher.encrypt(abc)

    # def ord_diff(ws):
    #     return (ord(ws[0]) - ord(ws[1])) % 26
    # print(list(map(ord_diff, map(lambda i: (abc[i], encrypted_abc[i]), range(0, len(abc))))))
    # print(abc)
    # print(cipher.encrypt(abc))
    # p = 'THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG'
    p = 'i like big butts ring tone'
    print(p)
    encrypted = cipher.encrypt(p)
    print(encrypted)
    fast = True
    found_ciphers = CaesarCipher.find_offset(encrypted, fast=fast)
    print(found_ciphers)
    if fast:
        print(found_ciphers.decrypt(encrypted))
    else:
        print(list(map(lambda c: c.decrypt(encrypted), found_ciphers)))


if __name__ == '__main__':
    main()
