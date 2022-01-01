from .tile import Tile
from .map_parser import Parser


class Loader(object):
    def __init__(self, filename, parser=Parser()):
        self.raw_map = open(filename, "rb")
        self.parser = parser

    def __iter__(self):
        return self

    def __next__(self):

        raw_data = self.raw_map.read(10)

        try:
            assert(len(raw_data))
        except AssertionError:
            raise StopIteration

        parsed = self.parser.parse(raw_data)

        id, x, y = parsed
        return Tile(id, x=x, y=y)

    def __del__(self):
        self.raw_map.close()
