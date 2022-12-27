from random import shuffle, choice
from itertools import product, accumulate
from numpy import floor, sqrt

class ADFGVX:
    def __init__(self, spoly, k, alph='ADFGVX'):
        self.polybius = list(spoly.upper())
        self.pdim = int(floor(sqrt(len(self.polybius))))
        self.key = list(k.upper())
        self.keylen = len(self.key)
        self.alphabet = list(alph)
        pairs = [p[0] + p[1] for p in product(self.alphabet, self.alphabet)]
        self.encode = dict(zip(self.polybius, pairs))
        self.decode = dict((v, k) for (k, v) in self.encode.items())

    def encrypt(self, msg):
        chars = list(''.join([self.encode[c] for c in msg.upper() if c in self.polybius]))
        colvecs = [(lett, chars[i:len(chars):self.keylen]) \
            for (i, lett) in enumerate(self.key)]
        colvecs.sort(key=lambda x: x[0])
        return ''.join([''.join(a[1]) for a in colvecs])

    def decrypt(self, cod):
        chars = [c for c in cod if c in self.alphabet]
        sortedkey = sorted(self.key)
        order = [self.key.index(ch) for ch in sortedkey]
        originalorder = [sortedkey.index(ch) for ch in self.key]
        base, extra = divmod(len(chars), self.keylen)
        strides = [base + (1 if extra > i else 0) for i in order]
        # Перемешка столбцов
        starts = list(accumulate(strides[:-1], lambda x, y: x + y))
        starts = [0] + starts
        # Стартовый индекс
        ends = [starts[i] + strides[i] for i in range(self.keylen)]
        # Перемешанный конец индексов
        cols = [chars[starts[i]:ends[i]] for i in originalorder]
        # получить переочередные столбцы
        pairs = []
        # восстановить
        for i in range((len(chars) - 1) // self.keylen + 1):
            for j in range(self.keylen):
                if i * self.keylen + j < len(chars):
                    pairs.append(cols[j][i])

        return ''.join([self.decode[pairs[i] + pairs[i + 1]] for i in range(0, len(pairs), 2)])