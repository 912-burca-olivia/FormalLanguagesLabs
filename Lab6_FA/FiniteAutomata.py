class FiniteAutomata:

    def __init__(self, Q, E, q0, F, S):
        self._states = Q
        self._alphabet = E
        self._initialState = q0
        self._finalStates = F
        self._transitions = S

    def getStates(self):
        return self._states

    def getAlphabet(self):
        return self._alphabet

    def getInitialState(self):
        return self._initialState

    def getFinalStates(self):
        return self._finalStates

    def getTransitions(self):
        return self._transitions

    @staticmethod
    def readFromFile(fileName):
        """
        This method goes through every line of a file and returns a Finite Automata with a set of
        states, an initial state, a set of final states, an alphabet and a dictionary of transactions,
        in which the key is a pair of starting state and a symbol, and the value is the destination
        state.
        :param fileName: The name of the file
        :return: A Finite Automata
        """
        with open(fileName) as file:
            states = file.readline().strip().split(' ')[2:]
            alphabet = file.readline().strip().split(' ')[2:]
            initialState = file.readline().strip().split(' ')[2:][0]
            finalStates = file.readline().strip().split(' ')[2:]
            file.readline()
            transitions = {}

            for line in file:
                start = line.strip().split('->')[0].strip().replace('(', '').replace(')', '').split(',')[0]
                route = line.strip().split('->')[0].strip().replace('(', '').replace(')', '').split(',')[1]
                destination = line.strip().split('->')[1].strip()

                if (start, route) in transitions.keys():
                    transitions[(start, route)].append(destination)
                else:
                    transitions[(start, route)] = [destination]

            try:
                FiniteAutomata.validate(states, alphabet, initialState, finalStates, transitions)
            except Exception as e:
                print(e)

            return FiniteAutomata(states, alphabet, initialState, finalStates, transitions)

    def validate(self, states, alphabet, q0, F, transitions):
        """
        Validates that the states from the set of final states, the initial state, and the starting states
        and destination states from the transitions are valid and a part of the finite set of states.
        :param states: The states
        :param alphabet: The alphabet
        :param q0: The initial state
        :param F: The final states
        :param transitions: The transitions
        :return:
        """
        if q0 not in states:
            raise Exception("Initial state is not in the finite set of states. ")
        for f in F:
            if f not in states:
                raise Exception("Final state is not in the finite set of states. ")
        for key in transitions.keys():
            start = key[0]
            inputSymbol = key[1]
            if start not in states:
                raise Exception("Start state from transition is not in the finite set of states. ")
            if inputSymbol not in alphabet:
                raise Exception("Input symbol from transition is not in the alphabet. ")
            for destination in transitions[key]:
                if destination not in states:
                    raise Exception("Destination state from transition is not in the finite set of states. ")

    def checkIfDFA(self):
        """
        A FA is DFA if corresponding to an input symbol, there is single resultant state (there is only
         one transition). This method goes through all the keys in the transitions dictionary and
         checks if there is a list with more than one element.
        :return: True if DFA, False otherwise.
        """
        for startStateInputSymbol in self._transitions.keys():
            if len(self._transitions[startStateInputSymbol]) > 1:
                return False
        return True

    def checkIfSequenceAccepted(self, sequence):
        """
        This method uses the Finite Automata to check if a sequence is accepted by it.
        We iterate through the symbols from the sequence and check if it can be reached
        by following the transitions. Also, it must end in a final state.
        :param sequence: The sequence
        :return: True if accepted or False otherwise
        """
        if self.checkIfDFA():
            currentState = self._initialState
            for symbol in sequence:  # we check if we get to a final state
                if (currentState, symbol) in self._transitions.keys():
                    currentState = self._transitions[(currentState, symbol)][0]
                else:
                    return False

            if currentState in self._finalStates:
                return True
            else:
                return False
        else:
            return False


