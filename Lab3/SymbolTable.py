class HashTable:
    def __init__(self, size):
        self.capacity = size
        self.table = []
        for x in range(size):
            self.table.append([])

    def hashFunction(self, key: str):
        return self.asciiValue(key) % self.capacity

    def asciiValue(self, str):
        sum=0
        for char in str:
            sum = sum + ord(char)
        return sum

    def get(self, val):
        pos = self.hashFunction(val)
        if val not in self.table[pos]:
            return -1
        return pos

    def insert(self, value: str):
        pos = self.get(value)
        if pos == -1:
            hashKey = self.hashFunction(value)
            self.table[hashKey].append(value)
            return hashKey

        return pos


class SymbolTable:
    def __init__(self, capacity):
        self.capacity = capacity
        self.hashtable = HashTable(capacity)

    def get(self, value):
        return self.hashtable.get(value)

    def insert(self, value: str):
        return self.hashtable.insert(value)

