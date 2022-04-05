from . import Parser
from random import randint


class MapGenerator(object):
    def __init__(self, filename, nx, ny, parser=Parser()):
        """
        nx, ny - count of tiles

        filename - name of file
        """
        self.filename = filename
        self.nx = nx
        self.ny = ny
        self.parser = parser

    def gen(self):
        with open(self.filename, "wb") as map:
            for x in range(self.nx):
                for y in range(self.ny):
                    map.write(self.parser.dump((randint(0, 3), x * 64, y * 64)))
