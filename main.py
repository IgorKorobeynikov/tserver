from core.server import Server
import argparse

__DESC__ = "TwisteRServer - simple python game server on raw UDP sockets."

# will be rewrited
parser = argparse.ArgumentParser(description=__DESC__)
parser.add_argument("--port", type=int, default=9265, help="Server port")
parser.add_argument("--max_conns", type=int, default=100, help="Count of clients")
parser.add_argument("--chat_size", type=int, default=10, help="Size of chat buffer")
args = parser.parse_args()


def main() -> None:
    server: Server = Server(**dict(args._get_kwargs()))
    try:
        server.run()
    except KeyboardInterrupt:
        print("Closing...")
        print(f"Please wait {server.repeater.delay} seconds...")
        server.repeater.break_()
        server.break_server()


if __name__ == "__main__":
    main()
