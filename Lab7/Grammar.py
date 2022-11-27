# FIRST(X) for a grammar symbol X is the set of terminals that begin the strings derivable from X.
# Follow(X) to be the set of terminals that can appear immediately to the right of Non-Terminal X
# in some sentential form.

# E = alphabet
# N = non terminals
#



class Production(object):
    def __init__(self, leftHandSide, rightHandSide):
        self.leftHandSide = leftHandSide
        self.rightHandSide = rightHandSide

    def __str__(self):
        return self.leftHandSide + " -> " + " ".join(self.rightHandSide)


class Grammar(object):
    def __init__(self, fileGrammar, onlyProductions=False):
        self.__fileGrammar = fileGrammar
        self.__nonTerminals = []
        self.__alphabet = []
        self.__S = None
        self.__productions = []
        self.__productionsLeftToRight = {}
        self.__productionsRightToLeft = {}
        self.EPSILON = "eps"
        self.__readGrammar(onlyProductions)

    @property
    def NonTerminals(self):
        return self.__nonTerminals

    @property
    def Alphabet(self):
        return self.__alphabet

    @property
    def S(self):
        return self.__S

    @property
    def Productions(self):
        return self.__productions

    @property
    def ProductionsLeftToRight(self):
        return self.__productionsLeftToRight

    @property
    def ProductionsRightToLeft(self):
        return self.__productionsRightToLeft

    @staticmethod
    def stringToList(inputString):
        if len(inputString) < 2:
            raise ValueError("{} is too short to be a list".format(inputString))
        if inputString[0] != "[" or inputString[-1] != "]":
            raise ValueError("{} must be of shape [elem1,elem2,...,elemn]".format(inputString))
        if len(inputString) == 2:
            return []
        elements = inputString[1:-1].split(",")
        return elements

    def checkCFGDeprecated(self, nonterminal, productions):
        if nonterminal not in self.__nonTerminals:
            raise ValueError("{} is not a non-terminal, so this is not a context-free grammar")
        for production in productions:
            productionTokens = production.split(" ")
            for token in productionTokens:
                if token not in self.__nonTerminals and token not in self.__alphabet and token != self.EPSILON:
                    raise ValueError("{} not found".format(token))

    def getProductionRhsTokens(self, nonterminal, production, onlyProductions=False):
        """
        Check if the grammar is CFG and create a list from the production rhs tokens
        :param nonterminal: the lhs (string)
        :param production: the rhs (string)
        :return: the rhs as list
        """
        nonterminal = nonterminal.strip(" ")
        if nonterminal not in self.__nonTerminals:
            if not onlyProductions:
                raise ValueError("{} is not a non-terminal, so this is not a context-free grammar".format(nonterminal))
            else:
                if len(nonterminal) >= 2 and nonterminal[0] == "\"" and nonterminal[-1] == "\"":
                    raise ValueError("{} is not a non-terminal, so this is not a context-free grammar".format(nonterminal))
                else:
                    self.__nonTerminals.append(nonterminal)
        productionTokens = production.strip(" ").split(" ")
        for idx, token in enumerate(productionTokens):
            token = token.strip(" ")
            if len(token) >= 2 and token[0] == "\"" and token[-1] == "\"":
                token = token[1:][:-1]
                if token not in self.__alphabet:
                    self.__alphabet.append(token)
            elif onlyProductions and token not in self.__nonTerminals:
                self.__nonTerminals.append(token)
            if not onlyProductions and token not in self.__nonTerminals and token not in self.__alphabet and token != self.EPSILON:
                raise ValueError("{} not found".format(token))
            productionTokens[idx] = token
        return productionTokens

    @staticmethod
    def addProductionToCorrespondenceTable(dictionaryKey, productionNumber, productionsTable):
        if dictionaryKey not in productionsTable:
            productionsTable.update({dictionaryKey: [productionNumber]})
        else:
            productionsTable[dictionaryKey].append(productionNumber)

    def __readGrammar(self, onlyProductions=False):
        contentGrammar = open(self.__fileGrammar, "r")
        linesGrammar = contentGrammar.readlines()
        productionLines = linesGrammar
        if not onlyProductions:
            if len(linesGrammar) < 4:
                raise ValueError("Not enough content to build Grammar or wrong format")
            self.__nonTerminals = linesGrammar[0].strip("\n").split(":=")[1].strip(" ").split(" ")
            self.__S = self.__nonTerminals[0]
            self.__alphabet = linesGrammar[1].strip("\n").split(":=")[1].strip(" ").split(" ")
            p = linesGrammar[2].strip("\n")
            if p != "P:":
                raise ValueError("Should have P: on the 3rd row")
            productionLines = linesGrammar[3:]
        elif onlyProductions:
            self.__S = productionLines[0].strip("\n").split(":=")[0].strip(" ")
        for line in productionLines:
            nonterminal, productions = line.strip("\n").split(":=")
            nonterminal = nonterminal.strip(" ")
            productions = productions.split(" | ")
            for production in productions:
                productionTokens = self.getProductionRhsTokens(nonterminal, production, onlyProductions)
                self.__productions.append(Production(nonterminal, productionTokens))
                latestProductionNumber = len(self.__productions) - 1
                self.addProductionToCorrespondenceTable(nonterminal, latestProductionNumber, self.__productionsLeftToRight)
                for token in productionTokens:
                    if token in self.__nonTerminals:
                        self.addProductionToCorrespondenceTable(token, latestProductionNumber, self.__productionsRightToLeft)

    def printProductions(self):
        firstRow = "P:\n"
        print(firstRow)
        for nonterminal in self.__productionsLeftToRight:
            for productionNumber in self.__productionsLeftToRight[nonterminal]:
                production = self.__productions[productionNumber]
                print(production)

    def productionsForNonterminal(self, nonterminal):
        for productionNumber in self.__productionsLeftToRight[nonterminal]:
            production = self.__productions[productionNumber]
            print(production)

    def menu(self):
        print("Menu for Grammar elements:\n")
        print("1. Set of nonterminals")
        print("2. Set of terminals")
        print("3. Set of productions")
        print("4. Productions for given nonterminal")
        while True:
            option = int(input("Type in your option: "))
            if option == 1:
                print(self.__nonTerminals)
            elif option == 2:
                print(self.__alphabet)
            elif option == 3:
                self.printProductions()
            elif option == 4:
                nonterminal = input("nonterminal:")
                self.productionsForNonterminal(nonterminal)
            else:
                break


grammar = Grammar("g3.txt")
grammar.menu()