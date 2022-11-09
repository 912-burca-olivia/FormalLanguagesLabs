from FiniteAutomata import FiniteAutomata

FA = FiniteAutomata.readFromFile('NDFA.in')


class UI:

    def printStates(self):
        print(FA.getStates())

    def printAlphabet(self):
        print(FA.getAlphabet())

    def printTransitions(self):
        print(FA.getTransitions())

    def printFinalStates(self):
        print(FA.getFinalStates())

    def printInitialState(self):
        print(FA.getInitialState())

    def DFA(self):
        print(FA.checkIfDFA())

    def checkSequence(self):
        seq = input()
        print(FA.checkIfSequenceAccepted(seq))

    def __displayMenu(self):
        print("1.Print all the states")
        print("2.Print the initial state")
        print("3.Print the final states")
        print("4.Print the alphabet")
        print("5.Print the transitions")
        print("6.Check if DFA")
        print("7.Check if sequence is accepted")
        print("0. Exit")

    def run(self):
        commands = {'1': self.printStates, '2': self.printInitialState,
                    '3': self.printFinalStates, '4': self.printAlphabet, '5': self.printTransitions,
                    '6': self.DFA, '7': self.checkSequence}
        stopProgram = False
        while not stopProgram:
            self.__displayMenu()
            print("Enter a command: ")
            command = input()
            if command in commands.keys():
                commands[command]()
            elif command == "0":
                stopProgram = True
            else:
                continue


if __name__ == '__main__':
    ui = UI()
    ui.run()
