import sys
import traceback

from Grammar import Grammar
import copy


class LL_Parser(object):
    def __init__(self, grammar: Grammar):
        self.__grammar = grammar
        self.__firstTable = {}
        self.__followTable = {}
        self.EPSILON = "eps"
        self.__parseTable = {}
        self.__productionsRhs = []
        self.generateParseTable()

    @property
    def grammar(self):
        return self.__grammar

    def generateParseTable(self):
        rows = list()
        rows.extend(self.__grammar.NonTerminals)
        rows.extend(self.__grammar.Alphabet)
        rows.append("$")

        columns = list()
        columns.extend(self.grammar.Alphabet)
        columns.append("$")

        for row in rows:
            for col in columns:
                self.__parseTable.update((row, col), ("err", -1))

        for col in columns:
            self.__parseTable.update((col, col), ("pop", -1))

        self.__parseTable.update(("$", "$"), ("acc", -1))

        productions = self.__grammar.ProductionsLeftToRight
        self.__productionsRhs = list()

        for key in productions.keys():

            for p in productions[key]:
                if not p[0] == "eps":
                    self.__productionsRhs.append(p)
                else:
                    self.__productionsRhs.extend(["eps", key])

        print(self.__productionsRhs)

        for key in productions.keys():
            for p in productions[key]:
                first = p[0]

                if first in self.__grammar.Alphabet:
                    if self.__parseTable.get((key, first))[0] == "err":
                        self._parseTable.update((key, first), (" " + p, self._productionsRhs.index(p) + 1))
                    else:
                        try:
                            raise Exception("CONFLICT: Pair "+key+","+first)
                        except:
                            traceback.print_exception(*sys.exc_info())
                elif first in self.__grammar.NonTerminals:
                    if len(p) == 1:
                        for symbol in self.__firstTable.get(first):
                            if self.__parseTable.get((key, symbol))[0] == "err":
                                self._parseTable.update((key, symbol), (" " + p, self._productionsRhs.index(p) + 1))
                            else:
                                try:
                                    raise Exception("CONFLICT: Pair " + key + "," + symbol)
                                except:
                                    traceback.print_exception(*sys.exc_info())
                    else:
                        i = 1
                        nextSymbol = p[1]
                        firstSetForProd = self.__firstTable.get(first)

                        while i < len(p) and nextSymbol in self.grammar.NonTerminals:
                            firstForNext = self.__firstTable.get(nextSymbol)
                            if "eps" in firstSetForProd:
                                firstSetForProd.remove("eps")
                                firstSetForProd.extend(firstForNext)

                            i+=1
                            if i < len(p):
                                nextSymbol = p[i]

                        for symbol in firstSetForProd:
                            if symbol == "eps":
                                symbol = "$"
                            if self.__parseTable.get((key, symbol))[0] == "err":
                                self._parseTable.update((key, symbol), (' '.join(p), self._productionsRhs.index(p) + 1))
                            else:
                                try:
                                    raise Exception("CONFILCT: Pair " + key + "," + symbol)
                                except:
                                    traceback.print_exception(*sys.exc_info())
                else:
                    follow = self.__followTable.get(key)
                    for symbol in follow:
                        if symbol == "eps":
                            if self.__parseTable.get((key, "$"))[0] == "err":
                                prod = ["eps", key]
                                self._parseTable.update((key, "$"), ("eps", self._productionsRhs.index(prod) + 1))
                            else:
                                try:
                                    raise Exception("CONFILCT: Pair " + key + "," + symbol)
                                except:
                                    traceback.print_exception(*sys.exc_info())
                        elif self.__parseTable.get((key, symbol))[0] == "err":
                            prod = ["eps", key]
                            self._parseTable.put((key, symbol), ("eps", self._productionsRhs.index(prod) + 1))
                        else:
                            try:
                                raise Exception("CONFILCT: Pair " + key + "," + symbol)
                            except:
                                traceback.print_exception(*sys.exc_info())

    def initializeTable(self, table, isFollow=False):
        for nonterminal in self.__grammar.NonTerminals:
            table.update({nonterminal: set()})
        if isFollow:
            table[self.__grammar.S].add(self.EPSILON)

    def first(self):
        previousFirstTable = {}
        self.initializeTable(previousFirstTable)
        self.initializeTable(self.__firstTable)
        while True:
            for nonterminal in self.__firstTable:
                for productionNumber in self.__grammar.ProductionsLeftToRight[nonterminal]:
                    production = self.__grammar.Productions[productionNumber]
                    productionFirstToken = production.rightHandSide[0]
                    if productionFirstToken in self.__grammar.Alphabet or productionFirstToken == self.EPSILON:
                        self.__firstTable[nonterminal].add(productionFirstToken)
                    else:  # it means that the first token of the production is a nonterminal
                        self.__firstTable[nonterminal].update(previousFirstTable[productionFirstToken])
            if previousFirstTable == self.__firstTable:
                break
            previousFirstTable = copy.deepcopy(self.__firstTable)

    def follow(self):
        previousFollowTable = {}
        self.initializeTable(previousFollowTable, True)
        self.initializeTable(self.__followTable, True)
        while True:
            for nonterminal in self.__followTable:
                if nonterminal in self.__grammar.ProductionsRightToLeft:
                    for productionNumber in self.__grammar.ProductionsRightToLeft[nonterminal]:
                        production = self.__grammar.Productions[productionNumber]
                        # look for the nonterminal in the production rhs tokens
                        for index, token in enumerate(production.rightHandSide):
                            if token == nonterminal:
                                # if there is nothing following the nonterminal,
                                # we take the previous iteration of follow for the leftHandSide
                                if index == len(production.rightHandSide) - 1:
                                    self.__followTable[nonterminal].update(previousFollowTable[production.leftHandSide])
                                else:
                                    followingToken = production.rightHandSide[index + 1]
                                    # if the following token is a terminal, we add it
                                    if followingToken in self.__grammar.Alphabet:
                                        self.__followTable[nonterminal].add(followingToken)
                                    # if the following token is a nonterminal,
                                    # we add the tokens from the corresponding first table,
                                    # but if epsilon is contained, instead of adding epsilon,
                                    # we take the previous iteration of follow for the leftHandSide
                                    else:
                                        for firstToken in self.__firstTable[followingToken]:
                                            if firstToken != self.EPSILON:
                                                self.__followTable[nonterminal].add(firstToken)
                                            else:
                                                self.__followTable[nonterminal].update(
                                                    previousFollowTable[production.leftHandSide])
            if previousFollowTable == self.__followTable:
                break
            previousFollowTable = copy.deepcopy(self.__followTable)

    def printFirst(self):
        print("FIRST:")
        print(self.__firstTable)

    def printFollow(self):
        print("FOLLOW:")
        print(self.__followTable)

    def printParseTable(self):
        print("PARSE TABLE:")
        print(self.__parseTable)

    def getProductionByOrderNr(self, nr):
        production = self.__productionsRhs[nr - 1]
        if "eps" in production:
            return ["eps"]
        return production

    def readSequence(self, fileName):
        sequence = []
        fileContent = open(fileName, "r")
        lines = fileContent.readlines()
        for line in lines:
            symbols = line.split(" ")
            sequence.extend(symbols)
        return sequence

    def parseSequence(self, sequence):
        alpha = []
        beta = []
        result = []
        alpha.append("$")
        i = len(sequence) - 1
        while i >= 0:
            alpha.append(sequence[i])
            i -= 1

        beta.append("$")
        beta.append(self.grammar.S)

        while not (alpha[len(alpha) - 1] == "$" and beta[len(alpha) - 1] == "$"):
            alphaPeek = alpha.pop()
            betaPeek = beta.pop()
            value = self.__parseTable[[alphaPeek, betaPeek]]
            if value[0] != "err":
                if value[0] == "pop":
                    alpha.pop()
                    beta.pop()
                else:
                    beta.pop()
                    if value[0] != "eps":
                        val = value[0].split(" ")
                        i2 = len(val) - 1
                        while i2 >= 0:
                            beta.append(val[i2])
                            i2 = i2 - 1
                    result.append(value[1])

            else:
                print("Syntax error for key [" + alphaPeek + ", " + betaPeek + "]")
                print("Current alpha and beta for sequence parsing: ")
                print(alpha)
                print(beta)
                return result

        return result



