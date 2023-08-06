import socket
import struct

from .networking import SocketReader, SocketWriter


MAX_IDS = [
    (code, *struct.unpack_from(code, b'\xff' * 8))
    for code in ['!B', '!H', '!I', '!L', '!Q']
]


def get_id_code(max_id):
    return next(code for code, size in MAX_IDS if size > max_id)


class StructReader(SocketReader):
    def __init__(self, sock, commands, max_id=None):
        self.sock = sock
        max_id = max_id or max(c._id for c in commands)
        self.id_code = get_id_code(max_id)

    @classmethod
    def get_factory(cls, commands, max_id=None):
        def get_struct_reader(sock):
            return cls(sock, commands, max_id)

        return get_struct_reader


class StructWriter(SocketWriter):
    def __init__(self, sock, commands, max_id=None):
        self.sock = sock
        max_id = max_id or max(c._id for c in commands)
        self.id_code = get_id_code(max_id)

    @classmethod
    def get_factory(cls, commands, max_id=None):
        def get_struct_writer(sock):
            return cls(sock, commands, max_id)

        return get_struct_writer
