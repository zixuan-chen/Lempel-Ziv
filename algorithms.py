class LZ77:
    """
    define codeword method C(d) = ASCII(d)
    """

    def __init__(self, searchBuffSize, lookAheadBuffSize):
        self.searchBuffSize = searchBuffSize
        self.lookAheadBuffSize = lookAheadBuffSize
        pass

    def encode(self, input):
        """
        :param input: should be a list containing characters
        :return: a 1-dimensional list of numbers
        i.e  [o_1, l_1, c_1, o_2, l_2, c_2, ...., o_n, l_n, c_n]
        where 'o_i' is the offset, 'l_i' is the length of the match, and 'c_i' is the codeword corresponding to
        the symbol in the look-ahead buffer

        e.g:
        input = "cabracadabrarrarrad"
        codeword = [0, 0, 99, 0, 0, 97, 0, 0, 98, 0, 0, 114, 0, 0, 97, 0, 0, 99, 0, 0, 97, 0, 0, 100, 7, 4, 114, 3, 5, 100]
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
            while curOffset > 0 and pt + curLength < len(input):
                search = input[pt - curOffset + curLength]
                lookAhead = input[pt + curLength]
                if input[pt - curOffset + curLength] == input[pt + curLength]:
                    curLength += 1
                else:
                    if curLength > length:
                        offset = curOffset
                        length = curLength
                    curOffset -= 1
                    curLength = 0
            pt += length
            if pt == len(input):
                codeword.extend((offset, length, 3))  # ASCII(^C) = 3, means end of file
            else:
                codeword.extend((offset, length, ord(input[pt])))
            pt += 1
        return codeword

    def decode(self, codeword):
        """
        :param codeword: a 1-dimensional list of numbers, must be multiple of 3
        :return: a string containing the characters encoded

        e.g:
        codeword = [0, 0, 99, 0, 0, 97, 0, 0, 98, 0, 0, 114, 0, 0, 97, 0, 0, 99, 0, 0, 97, 0, 0, 100, 7, 4, 114, 3, 5, 100]
        output = "cabracadabrarrarrad"
        """
        output = ""
        for i in range(0, len(codeword), 3):
            o, l, c = codeword[i:i + 3]
            for j in range(l):
                output += output[-o]
            if c != 3:
                output += chr(c)
        return output


class LZ78:

    def __init__(self):
        pass

    def encode(self, input):
        codeword = []
        entry = []
        i = 0
        while i < len(input):
            j = len(codeword) - 1
            while j >= 0:
                if i + len(entry[j]) < len(input) and entry[j] == input[i:i + len(entry[j])]:
                    codeword.append([j + 1, ord(input[i + len(entry[j])])])
                    entry.append(entry[j] + input[i + len(entry[j])])
                    break
                j -= 1
            if j == -1:
                codeword.append([0, ord(input[i])])
                entry.append(input[i])
                i += 1
            else:
                i += len(entry[j]) + 1
        return codeword

    def decode(self, codeword):
        output = ""
        entry = []
        for i in range(len(codeword)):
            j, c = codeword[i]
            c = chr(c)
            if j == 0:
                entry.append(c)
                output += c
            else:
                entry.append(entry[j - 1] + c)
                output += entry[j - 1] + c
        return output


if __name__ == '__main__':
    # input = "cabracadabrarrarrad"
    # lz77coder = LZ77(8, 7)
    # codeword = lz77coder.encode(input)
    # print("codeword = ", codeword)
    # output = lz77coder.decode(codeword)
    # print("output = ", output)

    lz78coder = LZ78()
    input = "wabbaywabbaywabbaywabbaywooywooywoo"
    codeword = lz78coder.encode(input)
    print("codeword = ", codeword)
    output = lz78coder.decode(codeword)
    print("output = ", output)
