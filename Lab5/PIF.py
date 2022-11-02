class PIF:
    def __init__(self):
        self._pairs = []

    def add(self, token, pos):
        self._pairs.append((token, pos))

    def __str__(self):
        result = ""
        for pair in self._pairs:
            result += pair[0] + " - " + str(pair[1]) + "\n"
        return result