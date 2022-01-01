class Parser(object):
    def __init__(self):
        pass

    def parse(self, raw_slice: bytes) -> tuple:

        b = raw_slice

        id = int.from_bytes(b[:2], "big", signed=False)
        x = int.from_bytes(b[2:6], "big", signed=False)
        y = int.from_bytes(b[6:], "big", signed=False)
        return id, x, y

    def dump(self, raw_tile: tuple) -> bytes:
        id = raw_tile[0]
        x = raw_tile[1]
        y = raw_tile[2]
        return \
            (id).to_bytes(2, "big") + \
            (x).to_bytes(4, "big") + \
            (y).to_bytes(4, "big")
