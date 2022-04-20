import argparse

__DESC__ = "TwisteRServer - simple python game server on raw UDP sockets."

# will be rewrited
parser = argparse.ArgumentParser(description=__DESC__)
parser.add_argument("--port", type=int, default=9265, help="Server port")
parser.add_argument("--max_conns", type=int, default=100, help="Count of clients")
parser.add_argument("--chat_size", type=int, default=10, help="Size of chat buffer")

