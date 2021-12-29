from core.server import Server


def main():
    server = Server()
    try:
        server.run()
    except KeyboardInterrupt:
        print("Closing...")
        print(f"Please wait {server.repeater.delay} seconds...")
        server.repeater.break_()


if __name__ == "__main__":
    main()
