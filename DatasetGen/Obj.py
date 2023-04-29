class Obj:
    def __init__(self, shape, colour, pattern, position=None, size=None):
        self.shape = shape
        self.colour = colour
        self.pattern = pattern
        self.row = position[0] if position is not None else None
        self.column = position[1] if position is not None else None
        self.size = size if size is not None else None
        self.for_query = False

    def setPosition(self, row, column):
        self.row = row
        self.column = column

    def setSize(self, size):
        self.size = size

    def sameAttr(self, other):
        return self.shape == other.shape and self.colour == other.colour and self.pattern == other.pattern

    def __str__(self):
        return str({
            "shape": self.shape,
            "colour": self.colour,
            "pattern": self.pattern,
            "row": self.row,
            "column": self.column,
            "size": self.size
        })

    def hasAttr(self, attr):
        return self.shape == attr or self.colour == attr

    def __dict__(self):
        return {
            "shape": self.shape,
            "colour": self.colour,
            "pattern": self.pattern,
            "row": self.row,
            "column": self.column,
            "size": self.size,
            "queried": self.for_query
        }
