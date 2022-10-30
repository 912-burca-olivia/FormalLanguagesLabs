import tokens


class ProgramReader:

    def __init__(self, filename):
        self.__filename = filename
        self.__tokens = []

    def openFile(self):
        return open(self.__filename, "r")

    def parseFile(self):
        file = self.openFile()
        currentToken = ""

        for character in file:
            if character not in tokens.separators:
                currentToken += character
            else:
                self.__tokens.append(currentToken)
                currentToken = ""

    def getTokens(self):
        return self.__tokens