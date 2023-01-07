from Grammar import Grammar
from LL1_Parser import LL_Parser
from ParserOutput import ParserOutput

grammar = Grammar("g1.txt")

ll_parser = LL_Parser(grammar)
ll_parser.first()
ll_parser.printFirst()
ll_parser.follow()
ll_parser.printFollow()
ll_parser.generateParseTable()
ll_parser.printParseTable()
sequence = ll_parser.readSequence("seq.txt")
print(ll_parser.parseSequence(sequence))
parserOutput = ParserOutput(ll_parser, sequence, "output.txt")
parserOutput.printTree()