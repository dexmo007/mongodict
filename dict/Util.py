def substr_until(self: str, s: str):
    find = self.find(s)
    return self[:(len(self) if find == -1 else find)]
