
import struct
import json
import socket

class Protocol:
    TYPE_TEXT = 1
    TYPE_FILE_METADATA = 2
    TYPE_FILE_CHUNK = 3
    TYPE_KEY_EXCHANGE = 4

    @staticmethod
    def send_packet(sock, packet_type, payload):
        """
        Sends a packet with header: [Type (1 byte)][Length (4 bytes)][Payload]
        """
        if isinstance(payload, str):
            payload = payload.encode('utf-8')
        
        length = len(payload)
        header = struct.pack('!BI', packet_type, length)
        sock.sendall(header + payload)

    @staticmethod
    def recv_packet(sock):
        """
        Receives a packet. Returns (type, payload_bytes).
        """
        # Read header (5 bytes)
        header = Protocol._recv_all(sock, 5)
        if not header:
            return None, None
            
        packet_type, length = struct.unpack('!BI', header)
        
        # Read payload
        payload = Protocol._recv_all(sock, length)
        if not payload:
            return None, None
            
        return packet_type, payload

    @staticmethod
    def _recv_all(sock, n):
        data = b''
        while len(data) < n:
            packet = sock.recv(n - len(data))
            if not packet:
                return None
            data += packet
        return data
