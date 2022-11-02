from PIF import PIF
from Scanner import Scanner
from SymbolTable import SymbolTable


class TestScanner:
    def __init__(self):
        self.symbolTable = SymbolTable(100)
        self.pif = PIF()
        self.scanner = Scanner()

    def testFile(self, filename):
        error = ""

        with open(filename, 'r') as file:
            indexLine = 0
            for line in file:
                indexLine += 1
                tokens = self.scanner.tokenize(line.strip())
                for i in range(len(tokens)):
                    if tokens[i] in self.scanner._keywords or tokens[i] in self.scanner._operators or tokens[i] in self.scanner._separators:
                        if tokens[i] == ' ':
                            continue
                        self.pif.add(tokens[i], (-1, -1))
                    elif self.scanner.checkIdentifier(tokens[i]):
                        self.pif.add("id", self.symbolTable.insert(tokens[i]))
                    elif self.scanner.checkConstant(tokens[i]):
                        self.pif.add("const", self.symbolTable.insert(tokens[i]))
                    else:
                        error += 'Lexical error at token - ' + tokens[i] + ' - at line ' + str(
                            indexLine) + "\n"

        with open('outputFiles/st.out', 'w') as writer:
            writer.write(str(self.symbolTable))

        with open('outputFiles/pif.out', 'w') as writer:
            writer.write(str(self.pif))

        if error != "":
            print("No errors found")
        else:
            print(error)

    def testP1(self):
        self.testFile('inputFiles/p1.txt')

    def testP2(self):
        self.testFile('inputFiles/p2.txt')

    def testP3(self):
        self.testFile('inputFiles/p3.txt')

    def testP1Err(self):
        self.testFile('inputFiles/p1err.txt')