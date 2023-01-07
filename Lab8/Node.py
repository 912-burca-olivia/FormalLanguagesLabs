class Node(object):
    def __init__(self):
        self.__parent = None
        self.__value = None
        self.__index = None
        self.__sibling = None
        self.__hasRight = None

    @property
    def parent(self):
        return self.__parent

    @property
    def value(self):
        return self.__value

    @property
    def index(self):
        return self.__index

    @property
    def sibling(self):
        return self.__sibling

    @property
    def hasRight(self):
        return self.__hasRight

    def setParent(self, parent):
        self.__parent = parent

    def setValue(self, value):
        self.__value = value

    def setIndex(self, index):
        self.__index = index

    def setSibling(self, sibling):
        self.__sibling = sibling

    def setHasRight(self, hasRight):
        self.__hasRight = hasRight
