import socket
import threading

import click

from message_protocol import MessageProtocol as protocol


class ChatClient:
    def __init__(self, host, port):
        self.conn = socket.create_connection((host, port))

    def listen(self):
        while True:
            message = protocol.read(self.conn)
            print(message)

    def send(self):
        while True:
            message = ""

            while not message:
                message = input()

            protocol.write(self.conn, message)


@click.command()
@click.option("-h", "--host", default="127.0.0.1", help="Hostname or IP address.")
@click.option("-p", "--port", default=8888, help="Port number.")
def main(host, port):
    client = ChatClient(host, port)

    threads = [
        threading.Thread(target=client.listen),
        threading.Thread(target=client.send),
    ]

    for thread in threads:
        thread.start()


if __name__ == "__main__":
    main()
