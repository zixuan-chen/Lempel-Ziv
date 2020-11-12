import os


class LZ77:

    def __init__(self, searchBuffSize, lookAheadBuffSize):
        self.searchBuffSize = searchBuffSize
        self.lookAheadBuffSize = lookAheadBuffSize
        pass

    def encodeFiles(self, filename):
        if not os.path.exists(filename):
            print("file", filename, "not exist!")
        with open(filename, 'r', encoding='utf-8') as f:
            return self.encode(f.read())

    def calculateCodingRate(self, stringLength, numTuples, encoding='unicode'):
        """
        if we use unicode:
            for input string:
                the input bits is 16 * length_of_input_string
            for output string:
                since the search_buffer_size and look_buffer_size can't be greater than 256
                in usual cases. it require 8 bits to store 'o_i' and 'l_i' each
                for 'c_i',  we assign 16 bits for unicode of c_i

                so it takes 8+8+16=32 bits for a tuple (o_i, l_i, c_i)

            so the coding rate = 2 * number_of_tuples / length_of_input_string
        :param stringLength:
        :param numTuples:
        :param codingMethod:
        :return: a float number representing coding rate
        """

        if encoding == 'unicode':
            return 2 * numTuples / stringLength
        else:
            print("unknown coding method")
            return 0


    def encode(self, input):
        """
        :param input: should be a list containing characters
        :return: list of tuples
        i.e  [(o_1, l_1, c_1), (o_2, l_2, c_2), ...., (o_n, l_n, c_n)]
        where 'o_i' is the offset, 'l_i' is the length of the match, and 'c_i' is the codeword corresponding to
        the symbol in the look-ahead buffer
        e.g:
        input = "cabracadabrarrarrad"
        codeword = [0, 0, 99, 0, 0, 97, 0, 0, 98, 0, 0, 114, 0, 0, 97, 0, 0, 99, 0, 0, 97, 0, 0, 100, 7, 4, 114, 3, 5, 100]
        """
        codeword = []
        for i in range(min(self.searchBuffSize, len(input))):
            codeword.append((0, 0, ord(input[i])))
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
                if search == lookAhead:
                    curLength += 1
                else:
                    if curLength > length:
                        offset = curOffset
                        length = curLength
                    curOffset -= 1
                    curLength = 0
            pt += length
            if pt == len(input):
                codeword.append((offset, length, 3))  # ASCII(^C) = 3, means end of file
            else:
                codeword.append((offset, length, ord(input[pt])))
            pt += 1

        codingRate = self.calculateCodingRate(len(input), len(codeword))

        return codeword, codingRate

    def decode(self, codeword):
        """
        :param codeword: a 1-dimensional list of numbers, must be multiple of 3
        :return: a string containing the characters encoded

        e.g:
        codeword = [0, 0, 99, 0, 0, 97, 0, 0, 98, 0, 0, 114, 0, 0, 97, 0, 0, 99, 0, 0, 97, 0, 0, 100, 7, 4, 114, 3, 5, 100]
        output = "cabracadabrarrarrad"
        """
        output = ""
        for tuple in codeword:
            o, l, c = tuple
            for j in range(l):
                output += output[-o]
            if c != 3:
                output += chr(c)
        return output


class LZ78:

    def __init__(self):
        pass

    def encodeFiles(self, filename):
        if not os.path.exists(filename):
            print("file", filename, "not exist!")
        with open(filename, 'r', encoding='utf-8') as f:
            return self.encode(f.read())

    def calculateCodingRate(self, stringLength, numTuples, encoding='unicode'):
        """
        if encoding is unicode:
            for input string:
                the input bits is 16 * length_of_input_string
            for output string:
                we assign 16 bits for o_i and 16 bits for c_i
                so it takes 16+16=32 bits for a tuple (o_i, c_i)

            so the coding rate = 2 * number_of_tuples / length_of_input_string

        :param stringLength:
        :param numTuples:
        :param encoding:
        :return:
        """

        if encoding == 'unicode':
            return 2 * numTuples / stringLength
        else:
            print("unknown coding method")
            return 0

    def encode(self, input):
        """
        :param input: should be a list containing characters
        :return: a 1-dimensional list of numbers
        i.e  [o_i, c_i]
        where 'o_i' is the offset, and 'c_i' is the last symbol of new entry
        e.g:
        input = "cabracadabrarrarrad"
        codeword = [0, 0, 99, 0, 0, 97, 0, 0, 98, 0, 0, 114, 0, 0, 97, 0, 0, 99, 0, 0, 97, 0, 0, 100, 7, 4, 114, 3, 5, 100]
        """
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

        codingRate = self.calculateCodingRate(len(input), len(codeword))

        return codeword, codingRate

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

# test1: test for basic function of LZ77
    print("==================test_case-1=====================")

    input_string1 = "cabracadabrarrarrad"
    print("input string:", input_string1)
    alg1 = LZ77(7, 6)
    print("test algorthm: LZ77(7, 6)")
    codeword1, _ = alg1.encode(input_string1)
    print("codeword of input string: ", codeword1)
    decode_string1 = alg1.decode(codeword1)
    print("decode of codeword: ", decode_string1)

# test2: test for basic function of LZ78
    print("==================test_case-2=====================")

    input_string2 = "wabba wabba wabba wabba woo woo woo"
    print("input string:", input_string2)
    alg2 = LZ78()
    print("test algorthm: LZ78")
    codeword2, _ = alg2.encode(input_string2)
    print("codeword of input string: ", codeword2)
    decode_string2 = alg2.decode(codeword2)
    print("decode of codeword: ", decode_string2)

# test3: test for coding rate of LZ77 and LZ78
    print("==================test_case-3=====================")
    input_path = "testfile.txt"
    f = open(input_path, 'r', encoding='utf-8')
    input_string3 = f.read()
    print("total number of characters: ", len(input_string3))

    alg3 = LZ77(255, 8)

    _, rate2 = alg2.encode(input_string3)
    _, rate3 = alg3.encode(input_string3)

    print("-----coding-rate(unicode)--------")
    print("|LZ77|%4f|" % rate3)
    print("|LZ78|%4f|" % rate2)

    print('==================finished=========================')

