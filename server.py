import queue
import random
import socket
import threading

import click
import colorama

from message_protocol import MessageProtocol as protocol

_colors = list(vars(colorama.Fore).values())


class ChatServer:
    def __init__(self, host, port, max_connections=0, max_waiting_queue=0):
        self.host = host
        self.port = port

        self.sock = socket.create_server((self.host, self.port))
        self.sock.listen()

        print(f"Started on {self.host}:{self.port}.")

        self.connections = {}
        self.max_connections = max_connections

        self.waiting_queue = queue.Queue(maxsize=max_waiting_queue)
        self.threads = []

    def start(self):
        while True:
            conn, address = self.sock.accept()

            if self.max_connections and len(self.connections) >= self.max_connections:
                protocol.write(conn, "Server is full.")

                try:
                    self.waiting_queue.put(conn)
                    protocol.write(conn, f"Welcome to the queue, {address}!")
                    protocol.write(
                        conn, f"You are {self.waiting_queue.qsize()} in the queue."
                    )

                    print(f"New connection in queue: {address}.")
                    print(f"Users in queue: {self.waiting_queue.qsize()}.")
                    continue

                except queue.Full:
                    protocol.write(conn, "Queue is full too.")
                    protocol.write(conn, "Bye.")
                    conn.close()

            self.accept_connection(conn, address)

    def accept_connection(self, conn, address):
        formatted_address = self.format_address(address)
        self.connections[formatted_address] = conn

        protocol.write(conn, f"Welcome, {formatted_address}!")
        protocol.write(conn, f"There are {len(self.connections)} users connected.")

        print(f"New connection: {formatted_address}.")
        print(f"Simultaneous connections: {len(self.connections)}.")

        thread = threading.Thread(target=self.listen, args=(conn, formatted_address))
        thread.start()
        self.threads.append(thread)

    def format_address(self, address):
        random_color = random.choice(_colors)
        return f"{random_color}{address[0]}:{address[1]}{colorama.Fore.RESET}"

    def listen(self, conn, address):
        while True:
            try:
                message = protocol.read(conn)
                print(f"{address} - {message!r}")

                if message.startswith("/"):
                    command, *args = message[1:].split()

                    if command == "disconnect":
                        self.disconnect(address)
                        break

                self.broadcast(f"{address}: {message}", address)

            except (BrokenPipeError, ConnectionResetError):
                self.disconnect(address)

    def broadcast(self, message, sender):
        try:
            for address, conn in self.connections.items():
                if address == sender:
                    continue

                protocol.write(conn, message)

        except (BrokenPipeError, ConnectionResetError):
            self.disconnect(address)

    def disconnect(self, address):
        self.connections[address].close()
        self.connections.pop(address)

        self.broadcast(f"{address} has disconnected.", address)

        print(f"Connection closed: {address}.")
        print(f"Simultaneous connections: {len(self.connections)}.")

        self.check_queue()

    def check_queue(self):
        if not self.waiting_queue.empty():
            conn = self.waiting_queue.get()
            self.accept_connection(conn, conn.getsockname())


@click.group()
def cli():
    pass


@cli.command()
@click.option("-h", "--host", default="127.0.0.1", help="Hostname or IP address.")
@click.option("-p", "--port", default=8888, help="Port number.")
@click.option("--max-connections", default=0, help="Maximum number of connections.")
@click.option("--max-waiting-queue", default=0, help="Maximum number of waiting queue.")
def start(host, port, max_connections, max_waiting_queue):
    server = ChatServer(host, port, max_connections, max_waiting_queue)
    server.start()


if __name__ == "__main__":
    cli()
