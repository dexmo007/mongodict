def split2(s: str, d1: str, d2: str):
    res0 = s.split(d1)
    res = []
    for r in res0:
        if d2 in r:
            res.extend(r.split(d2))
        else:
            res.append(r)
    return res


def substring_until(self: str, s: str):
    find = self.find(s)
    return self[:(len(self) if find == -1 else find)]


if __name__ == '__main__':
    print(split2('foo barr/was or this/that', ' ', '/'))
