import socket
import threading
from dataclasses import dataclass, astuple
from src.server.connection import TCPConnection, UDPConnection
import sys
import signal


"""Server Client DATA"""
Address_Type = tuple[str, int]

"""Address data class"""
@dataclass
class Address:
    ip:str = socket.gethostbyname(socket.gethostname())
    port:int = 8000
    
    def __repr__(self) -> tuple[str, int]:
        return self.ip, self.port

"""Server class can handle UDP and TCP connections"""
class Server:
    def __init__(self, IP, PORT):
        self.addr = Address(ip=IP, port=PORT)
        self.bufferSize = 1024
        self.format = 'utf-8'
        self.disconnect = "bye"
        
        #UDP part of server
        self.UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.UDPServerSocket.bind(astuple(self.addr))
        
        #TCP part of server
        self.TCPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.TCPServerSocket.bind(astuple(self.addr))
        
        self.running = True
        print("Server up and listening")

    """UDP part of Server"""
    def send_udp_message(self, message:str, addr:Address_Type):
        self.UDPServerSocket.sendto(self.encode_message(message), addr)

    def start_listen_for_udp(self):
        listner = threading.Thread(target=self.listen_for_udp)
        listner.start()
        
    def listen_for_udp(self):
        while self.running:
            message, addr = self.UDPServerSocket.recvfrom(self.bufferSize)
            UDPConnection(self, addr, self.bufferSize, message)

    """TCP part of Server"""
    def send_tcp_message(self, message:str, conn:socket.socket):
        encoded_message = self.encode_message(message)
        conn.send(self.encode_message(str(len(encoded_message)).ljust(self.bufferSize)))
        conn.send(encoded_message)
        
    def start_listen_for_tcp(self):
        listner = threading.Thread(target=self.listen_for_tcp)
        listner.start()
    
    def listen_for_tcp(self):
        self.TCPServerSocket.listen()
        while self.running:
            conn, addr = self.TCPServerSocket.accept()
            TCPConnection(self, conn, addr, self.bufferSize)
    
    """Server processize"""
    def decode_message(self, message:bytes) -> str:
        return message.decode(self.format)
    
    def encode_message(self, message:str) -> bytes:
        return message.encode(self.format)
    
    def stop_server(self, signal, frame):
        print("Server shutting down...")
        self.running = False
        self.UDPServerSocket.close()
        self.TCPServerSocket.close()
        sys.exit(0)

    def run(self):
        signal.signal(signal.SIGINT, self.stop_server)
        
        udp_listener = threading.Thread(target=self.listen_for_udp)
        tcp_listener = threading.Thread(target=self.listen_for_tcp)

        udp_listener.start()
        tcp_listener.start()

        udp_listener.join()
        tcp_listener.join()
    