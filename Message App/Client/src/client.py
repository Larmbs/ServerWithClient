import socket
from dataclasses import dataclass, astuple

SERVER_IP = '127.0.0.1'
SERVER_PORT = 9000

@dataclass
class Address:
    ip: str = socket.gethostbyname(socket.gethostname())
    port: int = 8000

    def addr(self):
        return self.ip, self.port

class Client:
    def __init__(self):
        self.serverAddress = Address(ip=SERVER_IP, port=SERVER_PORT)
        self.bufferSize = 1024
        self.format = 'utf-8'
        
        self.connect()
        
    def connect(self):
        try:
            self.UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
            self.TCPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
            self.TCPClientSocket.connect(astuple(self.serverAddress))
        except Exception as e:
            print(e)
        else:
            print("Connection established")

    def send_udp_message(self, message: str):
        self.UDPClientSocket.sendto(self.encode(message), astuple(self.serverAddress))
        received_message, _ = self.UDPClientSocket.recvfrom(self.bufferSize)
        return self.decode(received_message)

    def send_tcp_message(self, message: str):
        try:
            encoded_message = self.encode(message)

            # Send the length of the message as a string (padded with spaces)
            self.TCPClientSocket.send(self.encode(str(len(encoded_message)).ljust(self.bufferSize)))

            # Send the actual message
            self.TCPClientSocket.send(encoded_message)

            # Receive the response length
            response_length_str = self.TCPClientSocket.recv(self.bufferSize).decode(self.format).strip()

            if response_length_str:
                # Convert the string to an integer
                response_length = int(response_length_str)

                # Receive the response message
                received_message = self.TCPClientSocket.recv(response_length)
                return self.decode(received_message)

            else:
                print("Received an empty response length.")
                return "error"

        except ValueError as ve:
            print(f"ValueError in send_tcp_message: {ve}")
            return "error"
        except Exception as e:
            print(f"Error in send_tcp_message: {e}")
            return "error"


    def decode(self, message: bytes):
        return message.decode(self.format)

    def encode(self, message: str):
        return message.encode(self.format)
