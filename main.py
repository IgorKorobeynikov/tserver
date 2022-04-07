from core.server import Server


def main() -> None:
    server: Server = Server()
    try:
        server.run()
    except KeyboardInterrupt:
        print("Closing...")
        print(f"Please wait {server.repeater.delay} seconds...")
        server.repeater.break_()
        server.break_server()


if __name__ == "__main__":
    main()
