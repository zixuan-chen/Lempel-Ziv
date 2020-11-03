import numpy as np


class LZ77:
    """
    define coding method C(d) = ASCII(d)
    """
    def __init__(self, searchBuffSize, lookAheadBuffSize):
        self.searchBuffSize = searchBuffSize
        self.lookAheadBuffSize = lookAheadBuffSize
        pass

    def encode(self, input):
        """
        :param input: should be a list containing characters
        eg:
        input = ['A', 'B', 'C', '0', '1']
        :return: a 1-dimensional list of numbers
        i.e  [o_1, l_1, c_1, o_2, l_2, c_2, ...., o_n, l_n, c_n]
        where 'o_i' is the offset, 'l_i' is the length of the match, and 'c_i' is the codeword corresponding to
        the symbol in the look-ahead buffer
        """
        maxLenMatched = [0]*self.searchBuffSize
        i = 0
        codeword = []
        for i in range(min(self.searchBuffSize, len(input))):
            codeword.append((0, 0, ord(input[i])))
        if len(input) <= self.searchBuffSize:
            return codeword

        pointer = self.searchBuffSize
        while pointer < len(input):
            

        return codeword

    def decode(self, codeword):
        pass


