from typing import Tuple
from core.server import Server
from submodules.argparser import parser

ARGS: list[Tuple[str, Any]] = parser.parse_args()

def main() -> None:
    server: Server = Server(**dict(ARGS._get_kwargs()))
    try:
        server.run()
    except KeyboardInterrupt:
        print("Closing...")
        print(f"Please wait {server.repeater.delay} seconds...")
        server.repeater.break_()
        server.break_server()


if __name__ == "__main__":
    main()
