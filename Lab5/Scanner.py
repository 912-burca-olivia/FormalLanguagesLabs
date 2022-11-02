import re
from tokens import *


class Scanner:

    def __init__(self) -> None:
        self._keywords = keywords
        self._operators = operators
        self._separators = separators

    def checkIdentifier(self, token):
        return re.match(identifier, token) is not None

    def checkConstant(self, token):
        return re.match(constant, token) is not None

    def findStringConstant(self, line, index):
        stringConstant = ''
        quotes = 0
        while index < len(line) and quotes < 2:
            if line[index] == '\"':
                quotes += 1
            stringConstant += line[index]
            index += 1
        return stringConstant, index

    def checkPartOfOperator(self, char):
        for operator in operators:
            if char in operator:
                return True
        return False

    def findOperator(self, line, index):
        operator = ''
        while index < len(line) and self.checkPartOfOperator(line[index]):
            operator += line[index]
            index += 1
        return operator, index

    def tokenize(self, line):
        token = ''
        index = 0
        tokens = []
        while index < len(line):
            if self.checkPartOfOperator(line[index]):
                if token:
                    tokens.append(token)
                token, index = self.findOperator(line, index)
                tokens.append(token)
                token = ''

            elif line[index] == '\"':
                if token:
                    tokens.append(token)
                token, index = self.findStringConstant(line, index)
                tokens.append(token)
                token = ''

            elif line[index] in separators:
                if token:
                    tokens.append(token)
                token, index = line[index], index + 1
                tokens.append(token)
                token = ''

            else:
                token += line[index]
                index += 1
        if token:
            tokens.append(token)
        return tokens

