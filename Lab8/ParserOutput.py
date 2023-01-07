from LL1_Parser import LL_Parser
from Node import Node


class ParserOutput(object):
    def __init__(self, parser: LL_Parser, sequence, outputFile):
        self.__parser = parser
        self.__productions = parser.parseSequence(sequence)
        self.__nodeNumber = 1
        self.__hasErrors = self.__productions.count(-1) > 0
        self.__outputFile = outputFile
        self.__nodeList = []
        self.__root = Node()
        self.generateTree()

    @property
    def nodeNumber(self):
        return self.__nodeNumber

    def setNodeNumber(self, nr):
        self.__nodeNumber = nr

    def generateTree(self):
        if self.__hasErrors:
            return
        nodeStack = []
        productionsIndex = 0
        node = Node()
        node.setParent(0)
        node.setSibling(0)
        node.setHasRight(False)
        node.setIndex(self.nodeNumber)
        self.setNodeNumber(self.nodeNumber)
        node.setValue(self.__parser.grammar.S)
        nodeStack.append(node)
        self.__nodeList.append(node)
        self.__root = node

        while productionsIndex < len(self.__productions) and not (len(nodeStack) == 0):
            currentNode = nodeStack[len(nodeStack) - 1]
            if currentNode.value in self.__parser.grammar.Alphabet or currentNode.value == "eps":
                while len(nodeStack) > 0 and not nodeStack[len(nodeStack) - 1].hasRight:
                    nodeStack.pop()
                if len(nodeStack) > 0:
                    nodeStack.pop()
                else:
                    break

                continue

            # children
            production = self.__parser.getProductionByOrderNr(self.__productions[productionsIndex])
            self.setNodeNumber(self.nodeNumber + len(production) - 1)
            i = len(production) - 1
            while i >= 0:
                child = Node()
                child.setParent(currentNode.index)
                child.setValue(production[i])
                child.setIndex(self.nodeNumber)
                if i == 0:
                    child.setSibling(0)
                else:
                    child.setSibling(self.nodeNumber - 1)
                child.setHasRight(i != len(production) - 1)

                self.setNodeNumber(self.nodeNumber - 1)
                nodeStack.append(child)
                self.__nodeList.append(child)

                i = i - 1

            self.setNodeNumber(self.nodeNumber + len(production) + 1)
            productionsIndex = productionsIndex + 1

    def printTree(self):
        try:
            self.__nodeList.sort(key=lambda x: x.index)
            file = open(self.__outputFile)
            file.write("Index | Value | Parent | Sibling" + "\n")
            for node in self.__nodeList:
                file.write(node.index + " | " + node.value + " | " + node.parent + " | " + node.sibling + " \n")
            file.close()

        except:
            print("Something went wrong while writing to the output file")
