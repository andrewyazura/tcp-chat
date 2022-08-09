import queue
import random
import socket
import threading

import colorama

from message_protocol import MessageProtocol as protocol

_colors = list(vars(colorama.Fore).values())


class ChatServer:
    def __init__(self, host, port, max_connections=0, max_waiting_queue=0):
        self.host = host
        self.port = port

        self.sock = socket.create_server((self.host, self.port))
        self.sock.listen()

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
                    print()
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
        print()

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
        self.connections.pop(address)
        self.broadcast(f"{address} has disconnected.", address)

        print(f"Connection closed: {address}.")
        print(f"Simultaneous connections: {len(self.connections)}.")
        print()

        # TODO: check queue and let next user in

    def check_queue(self):
        if not self.waiting_queue.empty():
            conn = self.waiting_queue.get()
            self.accept_connection(conn, conn.getsockname())


if __name__ == "__main__":
    server = ChatServer("localhost", 8888)
    server.start()
