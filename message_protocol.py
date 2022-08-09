import struct


class MessageProtocol:
    @staticmethod
    def read(conn):
        def _read_message(conn, length):
            data = b""
            while len(data) < length:
                data += conn.recv(length - len(data))
            return data

        length = struct.unpack("!I", _read_message(conn, 4))[0]
        return _read_message(conn, length).decode()

    @staticmethod
    def write(conn, message):
        prefix = struct.pack("!I", len(message))
        conn.send(prefix)
        conn.send(message.encode())
