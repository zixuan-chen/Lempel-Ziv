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
        input = "cabracadabrarrarrad"
        :return: a 1-dimensional list of numbers
        i.e  [o_1, l_1, c_1, o_2, l_2, c_2, ...., o_n, l_n, c_n]
        where 'o_i' is the offset, 'l_i' is the length of the match, and 'c_i' is the codeword corresponding to
        the symbol in the look-ahead buffer
        """
        codeword = []
        for i in range(min(self.searchBuffSize, len(input))):
            codeword.extend((0, 0, ord(input[i])))
        if len(input) <= self.searchBuffSize:
            return codeword

        pt = self.searchBuffSize

        while pt < len(input):
            offset = self.searchBuffSize
            length = 0
            curOffset = self.searchBuffSize
            curLength = 0
            while curOffset > 0 and pt+curLength < len(input):
                print("input[pt-curOffset+curLength] = %c, input[pt+curLength] = %c"
                      %(input[pt-curOffset+curLength], input[pt+curLength]))
                if input[pt-curOffset+curLength] == input[pt+curLength]:
                    curLength += 1
                else:
                    if curLength > length:
                        offset = curOffset
                        length = curLength
                    curOffset -= (curLength+1)
                    curLength = 0
            pt += length
            if pt == len(input):
                codeword.extend((offset, length, 3)) # ASCII(^C) = 3
            else:
                codeword.extend((offset, length, ord(input[pt+length])))
        return codeword

    def decode(self, codeword):
        """

        :param codeword: a 1-dimensional list of numbers, must be multiple of 3
        :return:
        """
        output = ""
        for i in range(0, len(codeword), 3):
            o, l, c = codeword[i:i+3]
            for j in range(l):
                output += output[-o]
            if c != 3:
                output += chr(c)
        return output


if __name__ == '__main__':
    input = "cabracadabrarrarrad"
    lz77coder = LZ77(8, 7)
    codeword = lz77coder.encode(input)
    print("codeword = ", codeword)

