class Tile:
    def __init__(self, id, *, x=0, y=0):
        self.id = id
        self.x = x
        self.y = y

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id}, x={self.x}, y={self.y})"
